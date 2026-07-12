"""
Core logic for the terminal chatbot interface and application lifecycle.
"""
import os
from colorama import Fore, Style, init
from openai import OpenAI

from core.conversation import ConversationManager
from agents.main_agent import MainAgent
from agents.specialized_agents import SpecializedAgent

# Initialize colorama for cross-platform terminal colors
init(autoreset=True)

class Chatbot:
    def __init__(self):
        """Initializes the clients, memory, and multi-agent ecosystem."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing from environment variables.")

        self.client = OpenAI(api_key=api_key)
        self.conversation = ConversationManager()

        # Instantiate specialized agents with distinct system prompts
        self.tech_agent = SpecializedAgent(
            name="Technology Agent",
            system_prompt="You are a Senior Tech Influencer. Write engaging LinkedIn posts about software, AI, and IT trends.",
            client=self.client
        )
        self.marketing_agent = SpecializedAgent(
            name="Marketing Agent",
            system_prompt="You are a Marketing Guru. Write compelling LinkedIn posts about growth, sales, branding, and SEO.",
            client=self.client
        )
        self.general_agent = SpecializedAgent(
            name="General Communications Agent",
            system_prompt="You are an expert Copywriter. Write professional, high-quality LinkedIn posts on general topics.",
            client=self.client
        )

        # Instantiate the main routing agent
        self.main_agent = MainAgent(
            client=self.client,
            tech_agent=self.tech_agent,
            marketing_agent=self.marketing_agent,
            general_agent=self.general_agent
        )

    def run(self) -> None:
        """Starts the continuous interactive terminal loop."""
        print(Fore.CYAN + Style.BRIGHT + "==================================================")
        print(Fore.CYAN + Style.BRIGHT + "  🚀 Welcome to the LinkedIn Post Generator API")
        print(Fore.CYAN + Style.BRIGHT + "==================================================")
        print(Fore.WHITE + "Type " + Fore.YELLOW + "'/salir'" + Fore.WHITE + " or '/exit' to close the app.\n")

        while True:
            user_input = input(Fore.GREEN + Style.BRIGHT + "You: " + Style.RESET_ALL)

            # Exit condition handling
            if user_input.strip().lower() in ['/salir', '/exit']:
                print(Fore.CYAN + "\nEnding session. Keep building great things! Goodbye.")
                break

            if not user_input.strip():
                continue

            print(Fore.MAGENTA + "\n[Main Agent] Analyzing your request to find the best expert...")
            
            try:
                # 1. Main Agent delegates the task
                selected_agent = self.main_agent.delegate(user_input)
                print(Fore.BLUE + f"[{selected_agent.name}] Task received. Drafting your post...\n")

                # 2. Specialized Agent generates the structured response
                post = selected_agent.generate_post(user_input, self.conversation.get_history())

                # 3. Update conversation history
                self.conversation.add_message("user", user_input)
                self.conversation.add_message("assistant", f"Generated Post: {post.title} (Category: {post.category})")

                # 4. Display the structured output
                print(Fore.YELLOW + Style.BRIGHT + "--- Generated LinkedIn Post ---")
                print(Fore.WHITE + Style.BRIGHT + f"Title: {post.title}")
                print(Fore.CYAN + f"Category: {post.category}")
                print(Fore.WHITE + f"\n{post.content}\n")
                print(Fore.BLUE + f"Hashtags: {' '.join(post.hashtags)}")
                print(Fore.YELLOW + Style.BRIGHT + "-------------------------------\n")

            except Exception as e:
                print(Fore.RED + f"An error occurred during processing: {str(e)}\n")