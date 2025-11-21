import sys
import os
import time

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from packages.orchestrator_core.agent import Agent
from packages.micro_tools.social.social_agent import SocialAgent

def test_hierarchical(agent, request):
    print(f"\nRequest: \"{request}\"")
    response = agent.run(request)
    
    # Simple check: Did it mention success?
    if "Success" in response:
        print("   SUCCESS")
        return True
    else:
        print(f"   FAILED. Response: {response}")
        return False

def main():
    print("=== Verification: Hierarchical Architecture ===")
    
    try:
        # 1. Initialize Orchestrator
        orchestrator = Agent()
        
        # 2. Initialize and Register SocialAgent
        social_agent = SocialAgent()
        orchestrator.register_sub_agent(social_agent)
        print("Registered SocialManager")
        
    except Exception as e:
        print(f"Failed to initialize: {e}")
        return

    # 3. Test Delegation
    tests = [
        "Announce 'Project X' on all social platforms."
    ]
    
    passed = 0
    for req in tests:
        if test_hierarchical(orchestrator, req):
            passed += 1
        time.sleep(1)
            
    print(f"\n=== Result: {passed}/{len(tests)} Tests Passed ===")

if __name__ == "__main__":
    main()
