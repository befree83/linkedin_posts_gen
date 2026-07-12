"""
Entry point for the LinkedIn Post Generator Chatbot.
"""
import os
from dotenv import load_dotenv
from core.chatbot import Chatbot

def main():
    # Load environment variables from the .env file
    load_dotenv()
    
    try:
        # Initialize and run the main chatbot loop
        bot = Chatbot()
        bot.run()
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to initialize chatbot. Details: {str(e)}")

if __name__ == "__main__":
    main()