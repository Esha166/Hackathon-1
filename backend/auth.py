from typing import Optional
from datetime import datetime
import os

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.dialects.postgresql import UUID # Import UUID
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, BigInteger # Import necessary SQLAlchemy types

from dotenv import dotenv_values

# Load environment variables
config = dotenv_values(".env")

# Use DATABASE_URL from .env, default to a PostgreSQL URL if not set for development
DATABASE_URL = config.get("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/testdb")

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTable[UUID], Base): # Change ID type to UUID
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True) # Use UUID for ID, removed default_text
    # Add other fields as needed for your user model, e.g.,
    # first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    # last_name: Mapped[str] = mapped_column(String(255), nullable=True)

    # Establish relationship with UserBackground
    background: Mapped["UserBackground"] = relationship("UserBackground", back_populates="user", uselist=False)

# Define UserBackground model directly in auth.py to resolve circular import
class UserBackground(Base):
    __tablename__ = "user_backgrounds"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True) # BIGSERIAL for Postgres
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True) # user.id will be UUID
    role: Mapped[str] = mapped_column(String(64), nullable=True)
    programming_level: Mapped[str] = mapped_column(String(32), nullable=True)
    hardware_specs: Mapped[str] = mapped_column(Text, nullable=True)
    software_experience: Mapped[str] = mapped_column(Text, nullable=True)
    interest_field: Mapped[str] = mapped_column(String(128), nullable=True)
    preferred_language: Mapped[str] = mapped_column(String(16), nullable=True)
    goals: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    user: Mapped["User"] = relationship("User", back_populates="background")


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session():
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

class UserManager(BaseUserManager[User, UUID]): # Change ID type to UUID
    reset_password_token_secret = config.get("RESET_PASSWORD_TOKEN_SECRET", "supersecretresetpasswordtoken")
    verification_token_secret = config.get("VERIFICATION_TOKEN_SECRET", "supersecretverificationtoken")

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    jwt_secret = config.get("JWT_SECRET", "supersecretjwtkey")
    return JWTStrategy(secret=jwt_secret, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, UUID]( # Change ID type to UUID
    get_user_manager,
    [auth_backend],
)