import sys
import os

# Add the root directory to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from packages.orchestrator_core.agent import Agent

def main():
    print("=== Starting MTD Verification: Social Fan-Out ===")
    
    # 1. Instantiate Agent
    agent = Agent()
    
    # 2. Define Test Request
    test_request = "Draft and post the following message to all social platforms: 'The Micro-Task Dispatcher (MTD) is officially in development! Our first goal is cross-posting to X, Threads, and Bluesky. Stay tuned! #aiagents #monorepo'"
    print(f"\nUser Request: {test_request}")
    
    # 3. Run Agent
    print("\n--- Agent Running ---")
    response = agent.run(test_request)
    
    # 4. Output Result
    print("\n--- Final Response ---")
    print(response)
    
    # 5. Simple Assertion
    if "All posts were successfully published" in response:
        print("\n✅ VERIFICATION PASSED")
    else:
        print("\n❌ VERIFICATION FAILED")

if __name__ == "__main__":
    main()
