"""
Implements the routing logic using native OpenAI Agents SDK handoffs.
"""
from agents import Agent
# Updated to import from the post_agents directory
from post_agents.specialized_agents import tech_agent, marketing_agent, general_agent

main_agent = Agent(
    name="Main Routing Agent",
    instructions=(
        "You are a smart router. Analyze the user intent and delegate the task "
        "to the correct specialized department. Always use your handoff tools "
        "to transfer control to either the Technology Agent, Marketing Agent, or General Communications Agent."
    ),
    handoffs=[tech_agent, marketing_agent, general_agent]
)