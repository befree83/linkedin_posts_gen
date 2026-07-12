"""
Manages the conversation history to provide contextual awareness.
"""
from typing import List, Dict

class ConversationManager:
    def __init__(self):
        """Initializes an empty conversation history."""
        self.history: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str) -> None:
        """
        Adds a new message to the history.
        
        Args:
            role (str): The role of the messenger ('user' or 'assistant').
            content (str): The content of the message.
        """
        self.history.append({"role": role, "content": content})

    def get_history(self) -> List[Dict[str, str]]:
        """
        Retrieves the full conversation history.
        
        Returns:
            List[Dict[str, str]]: The list of past messages.
        """
        return self.history

    def clear_history(self) -> None:
        """Clears the current conversation history."""
        self.history = []