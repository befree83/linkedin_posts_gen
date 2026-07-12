# LinkedIn Post Generator Chatbot

A highly modular, terminal-based multi-agent application powered by Python and the OpenAI API. It allows users to generate structured LinkedIn posts based on different topics by leveraging a Main Routing Agent and Specialized Agents.

## Architecture
- **Main Agent**: Analyzes user intent and delegates the task to the correct specialized agent using OpenAI Tool Calling.
- **Specialized Agents**: Craft the final response following a strict Pydantic structure (Title, Content, Hashtags, Category) using OpenAI Structured Outputs.
- **Conversation Manager**: Keeps track of context across the session.

## Setup Instructions

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate