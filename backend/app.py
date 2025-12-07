from contextlib import asynccontextmanager
from typing import Annotated
from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .rag.query import query_book
from .auth import auth_backend, create_db_and_tables, fastapi_users, User, get_async_session, UserBackground
from .schemas import UserBackgroundCreate, UserBackgroundRead
from .personalization.service import get_personalized_content # Import personalization service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before the app starts
    await create_db_and_tables()
    yield
    # After the app stops (if any cleanup is needed)

app = FastAPI(title="Book RAG Chatbot - Gemini", lifespan=lifespan)

class ChatRequest(BaseModel):
    question: str

class PersonalizedContentResponse(BaseModel):
    chapter_id: str
    personalized_content: str

@app.post("/chat")
def chat(req: ChatRequest):
    answer = query_book(req.question)
    return {"answer": answer}

@app.get("/")
def root():
    return {"status": "RAG chatbot running with Gemini API"}

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(User),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(User),
    prefix="/auth",
    tags=["auth"],
)
# app.include_router( # Temporarily comment out as we will define /users/{user_id}/background manually
#     fastapi_users.get_users_router(User),
#     prefix="/users",
#     tags=["users"],
# )

current_active_user = fastapi_users.current_user()

@app.post("/users/{user_id}/background", response_model=UserBackgroundRead, status_code=status.HTTP_201_CREATED)
async def create_or_update_user_background(
    user_id: UUID,
    background_data: UserBackgroundCreate,
    user: Annotated[User, Depends(current_active_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    if user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this user's background")

    # Check if a background entry already exists for this user
    existing_background = await session.execute(
        select(UserBackground).where(UserBackground.user_id == user_id)
    )
    existing_background = existing_background.scalar_one_or_none()

    if existing_background:
        # Update existing background
        for field, value in background_data.model_dump(exclude_unset=True).items():
            setattr(existing_background, field, value)
        session.add(existing_background)
        await session.commit()
        await session.refresh(existing_background)
        return existing_background
    else:
        # Create new background
        new_background = UserBackground(user_id=user_id, **background_data.model_dump())
        session.add(new_background)
        await session.commit()
        await session.refresh(new_background)
        return new_background

@app.get("/users/{user_id}/background", response_model=UserBackgroundRead)
async def get_user_background(
    user_id: UUID,
    user: Annotated[User, Depends(current_active_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    if user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this user's background")

    result = await session.execute(
        select(UserBackground).where(UserBackground.user_id == user_id)
    )
    user_background = result.scalar_one_or_none()

    if user_background is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User background not found")
    
    return user_background

@app.get("/auth/me", response_model=UserBackgroundRead) # Assuming we want to return user's background with /me
async def get_current_user_profile(
    user: Annotated[User, Depends(current_active_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    # Retrieve the user's background along with the user data
    result = await session.execute(
        select(UserBackground).where(UserBackground.user_id == user.id)
    )
    user_background = result.scalar_one_or_none()

    if user_background is None:
        # If no background, return a default or error based on requirements
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User background not found")
    
    return user_background

@app.post("/personalize/chapter/{chapter_id}", response_model=PersonalizedContentResponse)
async def personalize_chapter_content(
    chapter_id: str, # chapter_id will be used to fetch content later
    user: Annotated[User, Depends(current_active_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    # 1. Fetch user profile
    result = await session.execute(
        select(UserBackground).where(UserBackground.user_id == user.id)
    )
    user_profile = result.scalar_one_or_none()

    if user_profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User background not found. Please complete the survey.")
    
    # 2. Fetch chapter content (placeholder for now)
    # In a later task, this will involve querying Qdrant or reading from Docusaurus files
    original_chapter_content = f"This is the original content for chapter {chapter_id}. " \
                                "It talks about basic concepts of AI and robotics. " \
                                "It has some technical terms and examples suitable for general audience."
    
    # 3. Personalize content
    personalized_text = await get_personalized_content(user_profile, original_chapter_content)

    return PersonalizedContentResponse(chapter_id=chapter_id, personalized_content=personalized_text)
