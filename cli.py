import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from packages.orchestrator_core.agent import Agent

def main():
    print("🤖 Micro-Task Dispatcher (MTD) CLI")
    print("-----------------------------------")
    
    agent = Agent()
    
    while True:
        try:
            user_input = input("\n📝 Enter your request (or 'exit'): ")
            if user_input.lower() in ['exit', 'quit']:
                break
                
            if not user_input.strip():
                continue
                
            print("\n🔄 Processing...")
            response = agent.run(user_input)
            print("\n✨ Result:")
            print(response)
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
