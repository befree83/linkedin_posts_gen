"""
Runtime configuration bootstrap launcher.
"""
from dotenv import load_dotenv
from core.chatbot import Chatbot

def main():
    load_dotenv()
    try:
        bot = Chatbot()
        bot.run()
    except Exception as e:
        print(f"Failed to start multi-agent network loop: {e}")

if __name__ == "__main__":
    main()