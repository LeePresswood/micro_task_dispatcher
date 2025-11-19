from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ToolCall:
    """Represents a planned call to a specific tool."""
    tool_name: str
    arguments: Dict[str, Any]

class Agent:
    """
    The Micro-Task Dispatcher (MTD) Agent.
    Responsible for planning, executing, and synthesizing tasks.
    """

    def __init__(self):
        """Initialize the agent."""
        from packages.orchestrator_core.llm_provider import LLMProvider
        self.llm = LLMProvider()

    def plan(self, user_request: str) -> List[ToolCall]:
        """
        Decompose the user request into a list of tool calls.
        
        Args:
            user_request: The natural language request from the user.
            
        Returns:
            A list of ToolCall objects representing the execution plan.
        """
        print(f"Planning for request: {user_request}")
        
        # Define the available tools schema (Hardcoded for now, could be dynamic)
        tools_schema = [
            {
                "tool_name": "post_to_threads",
                "description": "Post a message to Threads.",
                "arguments": {"message": "The text content to post."}
            },
            {
                "tool_name": "post_to_bluesky",
                "description": "Post a message to Bluesky.",
                "arguments": {"message": "The text content to post."}
            },
            {
                "tool_name": "post_to_x",
                "description": "Post a message to X (Twitter).",
                "arguments": {"message": "The text content to post."}
            }
        ]
        
        # Use LLM to generate plan
        plan = self.llm.generate_plan(user_request, tools_schema)
        
        if not plan:
            print("LLM failed to generate a plan (or no API key). Falling back to empty plan.")
            
        return plan

    def execute(self, plan: List[ToolCall]) -> Dict[str, Any]:
        """
        Execute the planned tool calls.
        
        Args:
            plan: The list of tool calls to execute.
            
        Returns:
            A dictionary mapping tool names to their results.
        """
        results = {}
        
        # Dynamic import to avoid circular deps or early import issues
        # In a real app, we'd have a ToolRegistry
        from packages.micro_tools.social import social_tools
        
        tool_map = {
            "post_to_threads": social_tools.post_to_threads,
            "post_to_bluesky": social_tools.post_to_bluesky,
            "post_to_x": social_tools.post_to_x
        }

        for tool_call in plan:
            print(f"Executing: {tool_call.tool_name} with {tool_call.arguments}")
            
            if tool_call.tool_name in tool_map:
                func = tool_map[tool_call.tool_name]
                try:
                    # Unpack arguments
                    result = func(**tool_call.arguments)
                    results[tool_call.tool_name] = result
                except Exception as e:
                    results[tool_call.tool_name] = {"error": str(e)}
            else:
                results[tool_call.tool_name] = {"error": "Tool not found"}
                
        return results

    def synthesize(self, results: Dict[str, Any]) -> str:
        """
        Synthesize the results into a final response.
        
        Args:
            results: The dictionary of tool execution results.
            
        Returns:
            A natural language summary of the operation.
        """
        lines = ["Task Execution Summary:"]
        success_count = 0
        for tool, result in results.items():
            # Handle SocialPostResult object or dict error
            if hasattr(result, 'success') and result.success:
                lines.append(f"- {tool}: Success (ID: {result.message_id})")
                success_count += 1
            else:
                lines.append(f"- {tool}: Failed ({result})")
        
        if success_count == len(results) and len(results) > 0:
            lines.append("\nAll posts were successfully published!")
        else:
            lines.append("\nSome posts failed.")
            
        return "\n".join(lines)

    def run(self, user_request: str) -> str:
        """
        Run the full agent loop: Plan -> Execute -> Synthesize.
        """
        plan = self.plan(user_request)
        results = self.execute(plan)
        response = self.synthesize(results)
        return response
