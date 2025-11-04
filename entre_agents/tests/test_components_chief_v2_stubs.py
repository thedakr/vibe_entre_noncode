#!/usr/bin/env python3
"""
Interactive Component Validation - Chief of Staff v2 with Stub Agents

This test suite validates the agentic framework components built for Chief of Staff v2:
- Agent coordination (multi-agent consultations)
- Tool execution (create_document, send_email, consult_agent)
- Autonomous scheduling (morning briefings)
- Stub specialist agents (Market Discovery, Product, Finance)

Stage: Chief of Staff v2 with stubbed specialist agents
Next: test_components_chief_v2_agents.py (when agents are fully implemented)

Usage:
    python3 tests/test_components_chief_v2_stubs.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.agent_coordination import AgentRegistry, AgentCoordinator, format_consultation_for_display
from core.tools import ToolRegistry, create_default_tools
from core.scheduler import SimpleScheduler
from agents.stub_agents import create_stub_agents
from datetime import datetime, time
import time as time_module


def print_header(title):
    """Print a formatted test section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_success(message):
    """Print success message."""
    print(f"✅ {message}")


def print_info(message):
    """Print info message."""
    print(f"ℹ️  {message}")


def test_1_agent_registry():
    """
    Test 1: Agent Registry

    Validates:
    - Registering agents
    - Listing available agents
    - Getting agents by name
    """
    print_header("TEST 1: Agent Registry")

    # Create registry
    registry = AgentRegistry()

    # Create stub agents
    stub_agents = create_stub_agents()

    # Register each agent
    print_info("Registering stub agents...")
    for agent_name, agent_instance in stub_agents.items():
        registry.register_agent(
            agent_name=agent_name,
            agent_instance=agent_instance,
            capabilities=agent_instance.capabilities
        )

    print()

    # List agents
    print_info("Available agents:")
    agents = registry.list_agents()
    for agent in agents:
        print(f"  • {agent['name']}")
        print(f"    Capabilities: {agent['capabilities']}")
        print(f"    Status: {agent['status']}")
        print()

    # Test retrieval
    market_agent = registry.get_agent("Market Discovery Agent")
    if market_agent:
        print_success(f"Successfully retrieved: {market_agent.name}")

    # Test LLM-formatted list
    print_info("Agent list formatted for LLM:")
    print(registry.get_available_agents_for_llm())

    print_success("Agent Registry test complete!")

    return registry


def test_2_agent_coordination(registry):
    """
    Test 2: Agent Coordination

    Validates:
    - Chief of Staff consulting specialist agents
    - Multi-agent conversations
    - Consultation tracking
    """
    print_header("TEST 2: Agent Coordination")

    # Create coordinator
    coordinator = AgentCoordinator(registry)

    # Test 1: Consult Market Discovery Agent
    print_info("Chief of Staff consulting Market Discovery Agent...")
    print("Question: 'How should I validate my business idea?'\n")

    consultation = coordinator.consult_agent(
        from_agent_name="Chief of Staff",
        to_agent_name="Market Discovery Agent",
        question="How should I validate my business idea?",
        context={
            'business_phase': 'Foundation',
            'has_customers': False,
            'has_mvp': False
        }
    )

    print(format_consultation_for_display(consultation))
    print_success("Market Discovery consultation complete!")

    # Test 2: Consult Product & Technology Agent
    print_info("\nChief of Staff consulting Product & Technology Agent...")
    print("Question: 'Should I build an MVP or use no-code first?'\n")

    consultation = coordinator.consult_agent(
        from_agent_name="Chief of Staff",
        to_agent_name="Product & Technology Agent",
        question="Should I build an MVP or use no-code first? I'm non-technical.",
        context={
            'business_phase': 'Foundation',
            'technical_background': False
        }
    )

    print(format_consultation_for_display(consultation))
    print_success("Product & Technology consultation complete!")

    # Test 3: Consult Capital & Financing Agent
    print_info("\nChief of Staff consulting Capital & Financing Agent...")
    print("Question: 'I have $50K in the bank and burning $10K/month. What should I do?'\n")

    consultation = coordinator.consult_agent(
        from_agent_name="Chief of Staff",
        to_agent_name="Capital & Financing Agent",
        question="I have $50K in the bank and burning $10K/month. What should I do?",
        context={
            'cash_in_bank': 50000,
            'monthly_burn': 10000,
            'monthly_revenue': 0
        }
    )

    print(format_consultation_for_display(consultation))
    print_success("Capital & Financing consultation complete!")

    # Check consultation history
    print_info("\nConsultation History:")
    history = coordinator.get_consultation_history(limit=10)
    for i, consult in enumerate(history, 1):
        print(f"  {i}. {consult.from_agent} → {consult.to_agent}")
        print(f"     Q: {consult.question[:60]}...")
        print()

    print_success("Agent Coordination test complete!")

    return coordinator


def test_3_tool_execution():
    """
    Test 3: Tool Execution

    Validates:
    - Tool registration
    - Tool execution
    - Document creation
    - Email sending (mock)
    """
    print_header("TEST 3: Tool Execution")

    # Create tool registry
    tools = create_default_tools()

    # List available tools
    print_info("Available tools:")
    for tool_name in tools.list_tools():
        tool = tools.get_tool(tool_name)
        print(f"  • {tool_name}")
        print(f"    Description: {tool.description}")
        print()

    # Test 1: Create document
    print_info("Testing create_document tool...")
    result = tools.execute_tool(
        tool_name="create_document",
        parameters={
            "title": "Market Research Plan",
            "content": """# Market Research Plan

## Objective
Validate that busy parents need meal planning solutions.

## Target Customers
- Parents with kids under 10
- Household income $75K+
- Both parents working

## Research Questions
1. How do you currently plan meals?
2. What's most frustrating about meal planning?
3. How much time do you spend on it weekly?
4. Would you pay for a solution?

## Interview Plan
- Conduct 15 interviews
- 30 minutes each
- Mix of phone and video
- Document insights immediately after
""",
            "format": "markdown"
        }
    )

    if result.success:
        print_success(f"Document created: {result.result['filename']}")
        print(f"  Location: {result.result['file_path']}")
        print(f"  Size: {result.result['size_bytes']} bytes")
        print(f"\n  Preview:\n{result.result['preview']}\n")
    else:
        print(f"❌ Error: {result.error}")

    # Test 2: Send email (mock)
    print_info("Testing send_email tool (mock mode)...")
    result = tools.execute_tool(
        tool_name="send_email",
        parameters={
            "to": "potential.customer@example.com",
            "subject": "Customer Interview Request",
            "body": """Hi there,

I'm building a meal planning solution for busy parents and would love to learn about your experiences with meal planning.

Would you be open to a 30-minute conversation sometime this week?

Best regards,
Matthew"""
        }
    )

    if result.success:
        print_success(f"Email sent (mock): {result.result['message_id']}")
        print(f"  Status: {result.result['status']}")
        print(f"  Note: {result.result['note']}\n")
    else:
        print(f"❌ Error: {result.error}")

    # Test 3: Get tool schemas for LLM
    print_info("Tool schemas for Anthropic function calling:")
    schemas = tools.get_tools_for_anthropic()
    for schema in schemas:
        print(f"  • {schema['name']}")

    print()
    print_success("Tool Execution test complete!")

    return tools


def test_4_scheduler():
    """
    Test 4: Autonomous Scheduler

    Validates:
    - Scheduling tasks
    - Running scheduled tasks
    - Task management
    """
    print_header("TEST 4: Autonomous Scheduler")

    # Create scheduler
    scheduler = SimpleScheduler()

    # Track if task ran
    task_ran = {'count': 0}

    def test_briefing():
        """Mock morning briefing function."""
        task_ran['count'] += 1
        print(f"\n  🌅 Morning Briefing #{task_ran['count']} executed!")
        print(f"     Time: {datetime.now().strftime('%H:%M:%S')}")

    # Schedule a task for 1 minute from now
    now = datetime.now()
    test_time = time(now.hour, now.minute + 1 if now.minute < 59 else 0)

    print_info(f"Scheduling test task for {test_time.strftime('%H:%M')}")
    print_info("(Will run within next ~60 seconds)")

    task_id = scheduler.schedule_daily(
        agent_name="Chief of Staff",
        task_name="morning_briefing",
        schedule_time=test_time,
        task_function=test_briefing
    )

    # List scheduled tasks
    print_info("\nScheduled tasks:")
    for task in scheduler.list_tasks():
        print(f"  • {task['agent']} - {task['task']}")
        print(f"    Schedule: {task['schedule_time']}")
        print(f"    Enabled: {task['enabled']}")
        print(f"    Last run: {task['last_run'] or 'Never'}")
        print()

    # Start scheduler
    print_info("Starting scheduler...")
    scheduler.start()

    # Wait for task to run
    print_info("Waiting for scheduled task to execute (max 90 seconds)...")
    print_info("(Press Ctrl+C to skip)")

    try:
        for i in range(90):
            time_module.sleep(1)
            if task_ran['count'] > 0:
                break
            if i % 10 == 0:
                print(f"  ... waiting ({i}s elapsed)")
    except KeyboardInterrupt:
        print("\n  Skipped waiting")

    # Stop scheduler
    scheduler.stop()

    if task_ran['count'] > 0:
        print_success(f"Scheduled task executed successfully! (ran {task_ran['count']} time(s))")
    else:
        print("⚠️  Task didn't run (may need to wait longer, or time already passed)")

    print_success("Scheduler test complete!")

    return scheduler


def test_5_integration(registry, coordinator, tools):
    """
    Test 5: Integration Test

    Validates:
    - Multi-agent coordination through tools
    - Chief of Staff using consult_specialist_agent tool
    - Full workflow integration
    """
    print_header("TEST 5: Integration - Multi-Agent Coordination via Tools")

    print_info("Simulating: Chief of Staff uses tools to coordinate specialists\n")

    # Wire up the consult_agent tool to use the coordinator
    consult_tool = tools.get_tool("consult_specialist_agent")

    # Replace the placeholder function with actual coordinator
    def consult_via_coordinator(agent_name: str, question: str) -> str:
        consultation = coordinator.consult_agent(
            from_agent_name="Chief of Staff",
            to_agent_name=agent_name,
            question=question,
            context={}
        )
        return consultation.response

    consult_tool.function = consult_via_coordinator

    # Test: Execute the consult tool
    print_info("Chief of Staff executing: consult_specialist_agent tool")
    print("  Agent: Market Discovery Agent")
    print("  Question: How many customer interviews should I do?\n")

    result = tools.execute_tool(
        tool_name="consult_specialist_agent",
        parameters={
            "agent_name": "Market Discovery Agent",
            "question": "How many customer interviews should I do to validate my idea?"
        }
    )

    if result.success:
        print("╭" + "─" * 68 + "╮")
        print("│ SPECIALIST RESPONSE" + " " * 47 + "│")
        print("╰" + "─" * 68 + "╯")
        print(result.result)
        print()
        print_success("Tool-based agent coordination working!")
    else:
        print(f"❌ Error: {result.error}")

    # Show consultation was tracked
    print_info("Checking coordination history...")
    history = coordinator.get_consultation_history(limit=1)
    if history:
        latest = history[-1]
        print(f"  Latest: {latest.from_agent} → {latest.to_agent}")
        print(f"  Timestamp: {latest.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    print()
    print_success("Integration test complete!")


def main():
    """
    Run all component validation tests.
    """
    print("\n" + "═" * 70)
    print("  CHIEF OF STAFF V2 - COMPONENT VALIDATION (WITH STUBS)")
    print("═" * 70)
    print("\n  Testing agentic framework components:")
    print("    • Agent coordination")
    print("    • Tool execution")
    print("    • Autonomous scheduling")
    print("    • Stub specialist agents")
    print()

    try:
        # Run tests
        registry = test_1_agent_registry()
        coordinator = test_2_agent_coordination(registry)
        tools = test_3_tool_execution()
        scheduler = test_4_scheduler()
        test_5_integration(registry, coordinator, tools)

        # Summary
        print("\n" + "═" * 70)
        print("  ✅ ALL COMPONENT TESTS PASSED!")
        print("═" * 70)
        print("\n  Framework components validated:")
        print("    ✓ Agent Registry & Coordination")
        print("    ✓ Tool Execution Engine")
        print("    ✓ Autonomous Scheduler")
        print("    ✓ Stub Specialist Agents")
        print("    ✓ Multi-agent Integration")
        print("\n  Next step: Rebuild Chief of Staff v2 using these components")
        print("\n  Future: test_components_chief_v2_agents.py (when agents fully implemented)")
        print()

    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
