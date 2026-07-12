# LinkedIn Post Generator (OpenAI Agents SDK)

A multi-agent application powered by Python and the official `openai-agents` SDK. It allows users to generate structured LinkedIn posts based on different topics by leveraging a Main Routing Agent and Specialized Agents using native SDK handoffs.

## Architecture
- **Main Agent**: Analyzes user intent and delegates the task to the correct specialized agent using the native `handoffs` array from the OpenAI Agents SDK.
- **Specialized Agents**: Craft the final response following a strict Pydantic structure (Title, Content, Hashtags, Category) using the `output_type` property.
- **Conversation Manager**: Keeps track of context across the session to provide memory.

## Setup Instructions

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate