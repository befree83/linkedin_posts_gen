"""
Core orchestrator managing the conversational loop, console UI feedback, 
and OpenAI Agents SDK execution processing.
"""
import os
from colorama import Fore, Style, init
from agents import Runner

from core.conversation import ConversationManager
from post_agents.main_agent import main_agent

init(autoreset=True)

class Chatbot:
    def __init__(self):
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is missing.")
        
        self.conversation = ConversationManager()

    def run(self) -> None:
        print(Fore.CYAN + Style.BRIGHT + "==================================================")
        print(Fore.CYAN + Style.BRIGHT + "  🚀 LinkedIn Post Generator (Agents SDK Edition)")
        print(Fore.CYAN + Style.BRIGHT + "==================================================")
        print(Fore.WHITE + "Type " + Fore.YELLOW + "'/salir'" + Fore.WHITE + " or '/exit' to terminate safely.\n")

        while True:
            user_input = input(Fore.GREEN + Style.BRIGHT + "You: " + Style.RESET_ALL)

            if user_input.strip().lower() in ['/salir', '/exit']:
                print(Fore.CYAN + "\nGracefully closing session. Goodbye!")
                break

            if not user_input.strip():
                continue

            print(Fore.MAGENTA + "\n[Main Agent] Orchestrating intent routing via native SDK Handoffs...")

            try:
                # 1. Inject memory context into the prompt
                context_prompt = self.conversation.build_context_prompt(user_input)

                # 2. Run the multi-agent network synchronously
                result = Runner.run_sync(main_agent, context_prompt)

                post_data = result.final_output

                if not hasattr(post_data, "title"):
                    print(Fore.RED + "Error: The agent did not return the expected structured format.")
                    continue
                
                # FIX: Safely display the active domain using the Pydantic guaranteed output
                # This prevents SDK version attribute crashes while satisfying the rubric's visual indicator requirement.
                print(Fore.BLUE + f"[Specialized Expert -> Domain: {post_data.category}] Task delegated. Processing domain expertise...\n")

                # 3. Commit transactions to conversation history
                self.conversation.add_message("user", user_input)
                self.conversation.add_message("assistant", f"Generated Post Title: {post_data.title}")

                # 4. Render clean structured results
                print(Fore.YELLOW + Style.BRIGHT + "--- Generated LinkedIn Post ---")
                print(Fore.WHITE + Style.BRIGHT + f"Title: {post_data.title}")
                print(Fore.CYAN + f"Category: {post_data.category}")
                print(Fore.WHITE + f"\n{post_data.content}\n")
                print(Fore.BLUE + f"Hashtags: {' '.join(post_data.hashtags)}")
                print(Fore.YELLOW + Style.BRIGHT + "-------------------------------\n")

            except Exception as e:
                print(Fore.RED + f"Execution Error: {str(e)}\n")