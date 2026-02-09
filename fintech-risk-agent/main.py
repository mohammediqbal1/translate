import argparse
import uvicorn
from agent.agent import RiskAgent

def main():
    parser = argparse.ArgumentParser(description="Fintech Risk Agent CLI 🤖")
    
    parser.add_argument('mode', nargs='?', choices=['train', 'eval', 'interactive', 'api', 'all'], default='all',
                        help="Mode to run the agent in (default: all)")
    
    args = parser.parse_args()
    
    agent = RiskAgent()
    
    if args.mode == 'train':
        agent.train()
    elif args.mode == 'eval':
        agent.evaluate()
    elif args.mode == 'interactive':
        agent.run_interactive()
    elif args.mode == 'api':
        print("🚀 Starting API Server on http://0.0.0.0:8000")
        uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=True)
    else:
        agent.run_all()

if __name__ == "__main__":
    main()
