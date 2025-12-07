from typing import Dict, Any
from backend.schemas import UserBackgroundRead
from backend.rag.query import get_gemini_answer # Using the existing Gemini LLM interaction

async def get_personalized_content(user_profile: UserBackgroundRead, chapter_content: str) -> str:
    """
    Generates personalized content for a chapter based on the user's profile.
    """
    
    # Construct a detailed prompt for the Gemini LLM
    prompt_parts = [
        "You are an expert content personalizer for a technical textbook on Physical AI and Humanoid Robotics.",
        "Your goal is to adapt the provided chapter content to best suit a specific user's background.",
        "Focus on adjusting analogies, examples, and technical depth.",
        "Maintain the core learning objectives and do NOT change any assessment questions or fundamental facts.",
        "Here is the user's background information:",
        f"- Role: {user_profile.role}",
        f"- Programming Level: {user_profile.programming_level}",
        f"- Field of Interest: {user_profile.interest_field}",
        f"- Software Experience: {user_profile.software_experience}",
        f"- Hardware Specs: {user_profile.hardware_specs}",
        f"- Preferred Language: {user_profile.preferred_language}",
        f"- Future Goals: {user_profile.goals}",
        "\nHere is the original chapter content to personalize:",
        "```",
        chapter_content,
        "```",
        "\nBased on the user's background, please rewrite and personalize the chapter content. "
        "Return ONLY the personalized content, with no introductory or concluding remarks."
    ]
    
    full_prompt = "\n".join(prompt_parts)
    
    personalized_content = get_gemini_answer(full_prompt)
    
    return personalized_content

# Example usage (for testing purposes, run separately or through FastAPI endpoint)
async def main():
    dummy_user_profile = UserBackgroundRead(
        id=1,
        user_id="a1b2c3d4-e5f6-7890-1234-567890abcdef",
        role="Beginner",
        programming_level="None",
        hardware_specs="Basic Laptop, no GPU",
        software_experience="None",
        interest_field="Robotics",
        preferred_language="English",
        goals="Understand basic robotics concepts",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    
    sample_chapter_content = """
    # Introduction to Control Systems
    Control systems are fundamental to robotics. They allow robots to perform tasks autonomously.
    A simple example is a thermostat in a house. It senses temperature and turns the heater on or off.
    """
    
    personalized = await get_personalized_content(dummy_user_profile, sample_chapter_content)
    print("\n--- Personalized Content ---")
    print(personalized)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
