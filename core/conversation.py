"""
Manages the global transactional conversation history across agent boundaries.
"""
from typing import List, Dict

class ConversationManager:
    def __init__(self):
        self.history: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})

    def get_history(self) -> List[Dict[str, str]]:
        return self.history

    def build_context_prompt(self, current_input: str) -> str:
        """
        Combines the chat history with the current user input to maintain 
        context across simple text-based Agent Runner executions.
        """
        if not self.history:
            return current_input
            
        prompt = "--- Conversation History ---\n"
        for msg in self.history:
            prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
        prompt += f"--- End of History ---\n\nCurrent Request: {current_input}"
        return prompt