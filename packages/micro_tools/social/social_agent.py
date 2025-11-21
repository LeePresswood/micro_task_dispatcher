from typing import List, Dict, Any
from packages.orchestrator_core.sub_agent import SubAgent
from packages.orchestrator_core.llm_provider import LLMProvider
from packages.micro_tools.social.social_tools import post_to_x, post_to_bluesky, post_to_threads

class SocialAgent(SubAgent):
    """
    Specialized agent for handling social media interactions.
    """
    def __init__(self):
        self.llm = LLMProvider()
        self.tools = {
            "post_to_x": post_to_x,
            "post_to_bluesky": post_to_bluesky,
            "post_to_threads": post_to_threads
        }
        # Schema for the LLM to understand available tools
        self.tools_schema = [
            {
                "name": "post_to_x",
                "description": "Post a message to X (formerly Twitter).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "description": "The text content of the post."}
                    },
                    "required": ["message"]
                }
            },
            {
                "name": "post_to_bluesky",
                "description": "Post a message to Bluesky.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "description": "The text content of the post."}
                    },
                    "required": ["message"]
                }
            },
            {
                "name": "post_to_threads",
                "description": "Post a message to Threads.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "description": "The text content of the post."}
                    },
                    "required": ["message"]
                }
            }
        ]

    @property
    def name(self) -> str:
        return "SocialManager"

    @property
    def description(self) -> str:
        return "Handles all social media posting and interactions. Use this for any request involving X, Bluesky, or Threads."

    def run(self, request: str) -> str:
        print(f"   [SocialManager] Received request: '{request}'")
        
        # 1. Plan
        plan = self.llm.generate_plan(request, self.tools_schema)
        if not plan:
            return "Failed to generate a plan for social media tasks."

        # 2. Execute
        results = []
        for tool_call in plan:
            tool_func = self.tools.get(tool_call.tool_name)
            if tool_func:
                print(f"   [SocialManager] Executing: {tool_call.tool_name}")
                try:
                    result = tool_func(**tool_call.arguments)
                    results.append(f"{tool_call.tool_name}: Success")
                except Exception as e:
                    results.append(f"{tool_call.tool_name}: Failed ({e})")
            else:
                results.append(f"{tool_call.tool_name}: Unknown tool")

        # 3. Synthesize (Simple summary for now)
        return f"SocialManager executed {len(results)} tasks: {', '.join(results)}"
