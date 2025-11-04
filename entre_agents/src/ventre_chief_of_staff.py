#!/usr/bin/env python3
"""
Command-line interface for VEntre agents.
Provides interactive chat with the Chief of Staff agent.
"""

import sys
import argparse
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.config import Config
from core.database import DatabaseAdapter
from core.llm_client import LLMClient
from agents.chief_of_staff import ChiefOfStaff


def print_banner():
    """Print welcome banner."""
    print("=" * 60)
    print("  VEntre AI Agent System - Chief of Staff")
    print("  Your AI-partnered entrepreneurship companion")
    print("=" * 60)
    print()


def interactive_chat(agent: ChiefOfStaff, stream: bool = True):
    """
    Run interactive chat loop with the Chief of Staff.

    Args:
        agent: ChiefOfStaff instance
        stream: Whether to stream responses
    """
    print("Chief of Staff is ready. Type 'quit', 'exit', or 'q' to end.")
    print("Type '/briefing' for morning briefing, '/recap' for evening recap.")
    print("Type '/status' to see current business context.")
    print("Type '/help' for more commands.")
    print("-" * 60)
    print()

    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! Keep building great things.")
                break

            elif user_input.lower() == '/briefing':
                print("\n" + "="*60)
                print("MORNING BRIEFING")
                print("="*60)
                print(agent.get_morning_briefing())
                print()
                continue

            elif user_input.lower() == '/recap':
                print("\n" + "="*60)
                print("EVENING RECAP")
                print("="*60)
                print(agent.get_evening_recap())
                print()
                continue

            elif user_input.lower() == '/status':
                status = agent.get_status()
                print("\n" + "="*60)
                print("CURRENT STATUS")
                print("="*60)
                print(f"Agent: {status['agent_name']} ({status['nickname']})")
                print(f"Entrepreneur: {status['entrepreneur_id']}")
                print(f"Business Phase: {status['business_phase']}")
                print(f"Cognitive State: {status['cognitive_state']}")
                print(f"Total Messages: {status['total_messages']}")
                print()
                continue

            elif user_input.lower() == '/help':
                print("\nAvailable commands:")
                print("  /briefing - Get morning briefing")
                print("  /recap    - Get evening recap")
                print("  /status   - Show current business context")
                print("  /help     - Show this help message")
                print("  quit/exit - End conversation")
                print()
                continue

            # Regular chat message
            print("\nChief of Staff: ", end='', flush=True)
            response = agent.chat(user_input, stream=stream)

            if not stream:
                print(response)

            print()

        except KeyboardInterrupt:
            print("\n\nGoodbye! Keep building great things.")
            break

        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again or type 'quit' to exit.")
            print()


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="VEntre AI Agent System - Chief of Staff"
    )
    parser.add_argument(
        '--no-stream',
        action='store_true',
        help='Disable response streaming'
    )
    parser.add_argument(
        '--entrepreneur-id',
        type=str,
        help='Entrepreneur ID (overrides config)'
    )
    parser.add_argument(
        '--briefing',
        action='store_true',
        help='Get morning briefing and exit'
    )
    parser.add_argument(
        '--recap',
        action='store_true',
        help='Get evening recap and exit'
    )

    args = parser.parse_args()

    try:
        # Load configuration
        config = Config()

        # Override entrepreneur ID if provided
        if args.entrepreneur_id:
            config.entrepreneur_id = args.entrepreneur_id

        # Validate configuration
        try:
            config.validate()
        except ValueError as e:
            print(f"Configuration Error: {e}")
            print("\nPlease ensure:")
            print("1. You've copied .env.example to .env")
            print("2. You've added your API keys to .env")
            print("3. All required fields are set")
            sys.exit(1)

        # Initialize components
        db = DatabaseAdapter(
            connection_string=config.get_database_connection_string(),
            db_type=config.database_type
        )

        llm = LLMClient(
            api_key=config.anthropic_api_key if config.llm_provider == "anthropic" else config.openai_api_key,
            provider=config.llm_provider,
            model=config.llm_model
        )

        agent = ChiefOfStaff(config=config, db=db, llm=llm)

        # Handle one-shot commands
        if args.briefing:
            print(agent.get_morning_briefing())
            return

        if args.recap:
            print(agent.get_evening_recap())
            return

        # Start interactive chat
        print_banner()
        interactive_chat(agent, stream=not args.no_stream)

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)

    except Exception as e:
        print(f"\nFatal Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
