"""
Defines the Pydantic schema for structured outputs and initializes 
the specialized downstream agents using the official OpenAI Agents SDK.
"""
from typing import List
from pydantic import BaseModel, Field
from agents import Agent

class LinkedInPost(BaseModel):
    """Pydantic model ensuring structured, guaranteed outputs from the SDK."""
    title: str = Field(description="An engaging header or title for the LinkedIn post.")
    content: str = Field(description="The main body text of the post, formatted for LinkedIn.")
    hashtags: List[str] = Field(description="A list of relevant hashtags (e.g., ['#Innovation', '#Tech']).")
    category: str = Field(description="The thematic category of the post.")

tech_agent = Agent(
    name="Technology Agent",
    instructions=(
        "You are a Senior Tech Influencer. "
        "Write engaging LinkedIn posts about software engineering, AI, and IT trends."
    ),
    output_type=LinkedInPost
)

marketing_agent = Agent(
    name="Marketing Agent",
    instructions=(
        "You are a Marketing Guru. "
        "Write compelling LinkedIn posts about growth hacking, sales, branding, and SEO."
    ),
    output_type=LinkedInPost
)

general_agent = Agent(
    name="General Communications Agent",
    instructions=(
        "You are a professional Copywriter. "
        "Write high-quality LinkedIn posts on general professional subjects."
    ),
    output_type=LinkedInPost
)