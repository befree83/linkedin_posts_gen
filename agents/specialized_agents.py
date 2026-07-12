"""
Defines the Pydantic schema for structured outputs and the Specialized Agent logic.
"""
from typing import List, Dict
from pydantic import BaseModel, Field
from openai import OpenAI

class LinkedInPost(BaseModel):
    """Pydantic model ensuring structured, guaranteed outputs from the LLM."""
    title: str = Field(description="An engaging header or title for the LinkedIn post.")
    content: str = Field(description="The main body text of the post, formatted for LinkedIn.")
    hashtags: List[str] = Field(description="A list of relevant hashtags (e.g., ['#Innovation', '#Tech']).")
    category: str = Field(description="The thematic category of the post (e.g., 'Technology', 'Marketing').")

class SpecializedAgent:
    def __init__(self, name: str, system_prompt: str, client: OpenAI):
        """
        Initializes a specialized agent.
        
        Args:
            name (str): The display name of the agent.
            system_prompt (str): The instructions dictating the agent's expertise.
            client (OpenAI): The authenticated OpenAI client.
        """
        self.name = name
        self.system_prompt = system_prompt
        self.client = client

    def generate_post(self, user_prompt: str, history: List[Dict[str, str]]) -> LinkedInPost:
        """
        Generates a structured LinkedIn post using the OpenAI Parse API.
        
        Args:
            user_prompt (str): The specific request from the user.
            history (List[Dict[str, str]]): The conversation history for context.
            
        Returns:
            LinkedInPost: A validated Pydantic object containing the generated post data.
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Inject conversation history for context awareness
        messages.extend(history)
        
        # Append current task
        messages.append({"role": "user", "content": user_prompt})

        # Using the beta parse method guarantees adherence to the Pydantic model
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=messages,
            response_format=LinkedInPost,
            temperature=0.7
        )

        return response.choices[0].message.parsed