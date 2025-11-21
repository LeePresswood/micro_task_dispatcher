from typing import List, Dict, Any, Optional
from packages.orchestrator_core.llm_provider import LLMProvider
from packages.orchestrator_core.types import ToolCall
from packages.orchestrator_core.sub_agent import SubAgent

class Agent:
    """
    The Micro-Task Dispatcher Agent (Orchestrator).
    """
    def __init__(self):
        self.llm = LLMProvider()
        self.sub_agents: Dict[str, SubAgent] = {}
        
    def register_sub_agent(self, sub_agent: SubAgent):
        """Registers a sub-agent with the orchestrator."""
        self.sub_agents[sub_agent.name] = sub_agent

    def plan(self, user_request: str) -> List[ToolCall]:
        """
        Decomposes the user request into a list of tool calls (or sub-agent delegations).
        """
        # Dynamic schema generation from registered sub-agents
        tools_schema = []
        for name, agent in self.sub_agents.items():
            tools_schema.append({
                "name": f"delegate_to_{name}",
                "description": f"Delegate a task to the {name}. {agent.description}",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "request": {"type": "string", "description": "The natural language request to delegate."}
                    },
                    "required": ["request"]
                }
            })

        # If no sub-agents, fall back to empty (or add default tools if we had them)
        if not tools_schema:
             print("Warning: No sub-agents registered.")

        print(f"Planning for request: {user_request}")
        plan = self.llm.generate_plan(user_request, tools_schema)
        
        if not plan:
            print("LLM failed to generate a plan (or no API key). Falling back to empty plan.")
            
        return plan

    def execute(self, plan: List[ToolCall]) -> Dict[str, Any]:
        """
        Executes the plan by calling registered sub-agents.
        """
        results = {}
        for call in plan:
            print(f"Executing: {call.tool_name} with {call.arguments}")
            
            # Check for delegation
            if call.tool_name.startswith("delegate_to_"):
                agent_name = call.tool_name.replace("delegate_to_", "")
                sub_agent = self.sub_agents.get(agent_name)
                
                if sub_agent:
                    try:
                        # Extract the 'request' argument
                        sub_request = call.arguments.get("request")
                        if sub_request:
                            result = sub_agent.run(sub_request)
                            results[call.tool_name] = f"Success: {result}"
                            print(f"[{agent_name}] {result}")
                        else:
                            results[call.tool_name] = "Failed: Missing 'request' argument"
                    except Exception as e:
                        results[call.tool_name] = f"Failed: {e}"
                else:
                    results[call.tool_name] = f"Failed: Unknown sub-agent {agent_name}"
            else:
                results[call.tool_name] = "Failed: Unknown tool (only delegations supported in Phase 3)"
                
        return results

    def synthesize(self, results: Dict[str, Any]) -> str:
        """
        Synthesizes the results into a final response.
        """
        summary = ["Task Execution Summary:"]
        for tool, result in results.items():
            summary.append(f"- {tool}: {result}")
            
        return "\n".join(summary)

    def run(self, user_request: str) -> str:
        """
        Main entry point: Plan -> Execute -> Synthesize.
        """
        print("\nProcessing...")
        plan = self.plan(user_request)
        results = self.execute(plan)
        response = self.synthesize(results)
        print(f"\nResult:\n{response}")
        return response
