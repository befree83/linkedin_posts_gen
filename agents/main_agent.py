"""
Implements the routing logic (Main Agent) using OpenAI Tool Calling.
"""
import json
from openai import OpenAI
from agents.specialized_agents import SpecializedAgent

class MainAgent:
    def __init__(self, client: OpenAI, tech_agent: SpecializedAgent, marketing_agent: SpecializedAgent, general_agent: SpecializedAgent):
        """
        Initializes the Main Agent with references to the specialized downstream agents.
        """
        self.client = client
        self.tech_agent = tech_agent
        self.marketing_agent = marketing_agent
        self.general_agent = general_agent

    def delegate(self, user_prompt: str) -> SpecializedAgent:
        """
        Analyzes the prompt and routes it to the correct agent via Tool Calling.
        
        Args:
            user_prompt (str): The user's input request.
            
        Returns:
            SpecializedAgent: The chosen agent to handle the task.
        """
        # Define the tool structure for the LLM to use for routing
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "route_to_department",
                    "description": "Routes the user's LinkedIn post request to the most appropriate specialized department.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "department": {
                                "type": "string",
                                "enum": ["tech", "marketing", "general"],
                                "description": "The target department (tech for software/AI, marketing for sales/growth, general for others)."
                            }
                        },
                        "required": ["department"]
                    }
                }
            }
        ]

        messages = [
            {
                "role": "system", 
                "content": "You are a smart router. Analyze the user prompt and decide which department should handle the LinkedIn post generation."
            },
            {"role": "user", "content": user_prompt}
        ]

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "route_to_department"}},
            temperature=0.0 # Deterministic routing
        )

        try:
            # Extract the department choice from the tool call arguments
            tool_call = response.choices[0].message.tool_calls[0]
            args = json.loads(tool_call.function.arguments)
            department = args.get("department", "general")
        except (IndexError, json.JSONDecodeError, AttributeError):
            # Fallback in case of unexpected LLM output
            department = "general"

        # Return the actual Agent object instance
        if department == "tech":
            return self.tech_agent
        elif department == "marketing":
            return self.marketing_agent
        else:
            return self.general_agent