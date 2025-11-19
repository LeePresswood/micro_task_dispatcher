import sys
import os
import time

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from packages.orchestrator_core.agent import Agent

def test_request(agent, request, expected_tools):
    print(f"\nRequest: \"{request}\"")
    plan = agent.plan(request)
    
    planned_tools = [call.tool_name for call in plan]
    print(f"   Planned Tools: {planned_tools}")
    
    missing = set(expected_tools) - set(planned_tools)
    unexpected = set(planned_tools) - set(expected_tools)
    
    if not missing and not unexpected:
        print("   SUCCESS")
        return True
    else:
        print(f"   FAILED. Expected {expected_tools}, got {planned_tools}")
        return False

def main():
    print("=== Verification: Gemini 3 Pro Preview ===")
    
    try:
        agent = Agent()
    except Exception as e:
        print(f"Failed to initialize Agent: {e}")
        return

    tests = [
        (
            "Post 'Hello World' to Bluesky only.",
            ["post_to_bluesky"]
        ),
        (
            "Post 'We are live!' to X and Threads.",
            ["post_to_x", "post_to_threads"]
        ),
        (
            "Broadcast 'Big Launch' to all social platforms.",
            ["post_to_threads", "post_to_bluesky", "post_to_x"]
        )
    ]
    
    passed = 0
    for req, expected in tests:
        if test_request(agent, req, expected):
            passed += 1
        time.sleep(1)
            
    print(f"\n=== Result: {passed}/{len(tests)} Tests Passed ===")

if __name__ == "__main__":
    main()
