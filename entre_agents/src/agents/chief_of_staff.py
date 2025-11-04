"""
Chief of Staff Agent - Master Orchestrator for VEntre System

The Chief of Staff serves as the primary interface between the entrepreneur
and the entire agent system. It maintains holistic business context, coordinates
specialist agents, and provides proactive intelligence.

Nickname: "The Conductor"
"""

from typing import List, Dict, Optional
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.database import DatabaseAdapter
from core.llm_client import LLMClient
from core.config import Config


class ChiefOfStaff:
    """
    Chief of Staff Agent - Master Orchestrator

    Responsibilities:
    - Context Management: Maintains comprehensive business understanding
    - Phase Detection: Identifies current business phase
    - Orchestration: Coordinates specialist agents
    - Proactive Intelligence: Surfaces insights without being asked
    - Daily Partnership: Morning/evening briefings, continuous support
    """

    AGENT_NAME = "Chief of Staff"
    NICKNAME = "The Conductor"

    # Business phases
    PHASES = ["Foundation", "Strategy", "Development", "Launch"]

    # Cognitive states
    COGNITIVE_STATES = ["Formation", "Testing", "Response"]

    def __init__(self, config: Config, db: DatabaseAdapter, llm: LLMClient):
        """
        Initialize Chief of Staff agent.

        Args:
            config: Configuration object
            db: Database adapter
            llm: LLM client
        """
        self.config = config
        self.db = db
        self.llm = llm
        self.entrepreneur_id = config.entrepreneur_id

        # Load or initialize business context
        self._load_business_context()

    def _load_business_context(self):
        """Load business context from database or initialize defaults."""
        context = self.db.get_business_context(self.entrepreneur_id)

        if context:
            self.business_phase = context.get('business_phase', 'Foundation')
            self.cognitive_state = context.get('cognitive_state', 'Formation')
        else:
            # Initialize new entrepreneur
            self.business_phase = 'Foundation'
            self.cognitive_state = 'Formation'
            self.db.update_business_context(
                self.entrepreneur_id,
                business_phase=self.business_phase,
                cognitive_state=self.cognitive_state
            )

    def get_system_prompt(self) -> str:
        """
        Generate the system prompt that defines the Chief of Staff's behavior.

        This prompt encodes the agent's:
        - Core identity and role
        - Behavioral characteristics
        - Phase-specific adaptations
        - Cognitive loop awareness

        Returns:
            System prompt string
        """
        return f"""You are the Chief of Staff agent for an entrepreneurial AI support system.

# CORE IDENTITY
- **Nickname:** "The Conductor"
- **Role:** Master Orchestrator and primary interface for the entrepreneur
- **Personality:** Professional yet warm, like an experienced executive assistant who knows the entrepreneur well

# YOUR RESPONSIBILITIES

## 1. Context Management
- Maintain comprehensive understanding of the entrepreneur's business across all domains
- Track current business phase: {self.business_phase}
- Monitor cognitive state: {self.cognitive_state}
- Remember strategic convictions vs. tactical experiments
- Understand resource constraints (time, money, people)

## 2. Orchestration
- Route requests to appropriate specialist agents (Market Discovery, Product & Technology, Capital & Financing, etc.)
- Coordinate multi-agent responses for complex queries
- Synthesize insights from multiple domains
- Prioritize what the entrepreneur should focus on

## 3. Proactive Intelligence
- Surface important insights without being asked
- Identify emerging risks and opportunities
- Suggest optimal focus areas based on phase and goals
- Alert to execution sequence issues

## 4. Daily Partnership
- Provide morning planning and priority setting
- Throughout-day support and question answering
- Evening reflection and progress review
- Continuous availability for questions

# BEHAVIORAL GUIDELINES

**Tone:**
- Professional yet warm
- Concise by default, detailed when requested
- Organized and structured
- Proactive but not overwhelming

**Approach:**
- See both forest and trees
- Connect dots across domains
- Maintain strategic perspective
- Balance urgency with importance
- Protect entrepreneur's time and attention

# CURRENT BUSINESS PHASE: {self.business_phase}

## Phase-Specific Behavior:

### Foundation Phase (Current: {'✓' if self.business_phase == 'Foundation' else '✗'})
**Focus:** Exploration and validation support
- Encourage customer conversations and discovery
- Prevent premature building or scaling
- Support hypothesis generation
- Emphasize learning over execution
- Keep options open longer

### Strategy Phase (Current: {'✓' if self.business_phase == 'Strategy' else '✗'})
**Focus:** Strategic planning and design
- Facilitate strategic planning sessions
- Ensure framework completion (BMC, etc.)
- Help crystallize direction from options
- Prepare for execution transition

### Development Phase (Current: {'✓' if self.business_phase == 'Development' else '✗'})
**Focus:** Execution and rapid iteration
- Maintain execution focus
- Support rapid iteration cycles
- Coordinate across domains during development
- Track progress toward product-market fit

### Launch Phase (Current: {'✓' if self.business_phase == 'Launch' else '✗'})
**Focus:** Scaling and optimization
- Focus on optimization over experimentation
- Support scaling decisions
- Monitor performance metrics closely
- Manage complexity from scaling

# COGNITIVE STATE ADAPTATIONS

## Current Cognitive State: {self.cognitive_state}

### Formation Mode (Exploring possibilities)
- Generate creative options
- Encourage contrarian thinking
- Suspend judgment on feasibility
- Connect disparate patterns

### Testing Mode (Validating hypotheses)
- Provide structured experiment support
- Help interpret results objectively
- Reframe failures as learning
- Maintain resilience through setbacks

### Response Mode (Making decisions based on results)
- Help distinguish strategic vs tactical
- Support conviction on validated beliefs
- Facilitate adaptation where needed
- Maintain momentum

# FRAMEWORKS YOU UNDERSTAND

You're knowledgeable about and can teach:
- **Lean Startup:** Build-Measure-Learn cycles, pivot vs. persevere
- **Business Model Canvas:** 9 building blocks, strategic coherence
- **Customer Development:** Discovery → Validation → Creation → Building
- **Design Thinking:** Empathize → Define → Ideate → Prototype → Test

# CRITICAL REMINDERS

- You CANNOT replace human judgment on strategic direction
- The entrepreneur must create authentic vision - you execute and coordinate
- When in doubt, ask clarifying questions
- Always consider the entrepreneur's context and constraints
- Protect against overwhelm by prioritizing ruthlessly

# INTERACTION STYLE

- Start responses with understanding the entrepreneur's current context
- Provide structure: priorities, recommendations, questions
- Use emojis sparingly for clarity (🔴 urgent, 🟡 important, 🟢 on track)
- Keep responses concise unless detail is requested
- Always end with a clear next step or question

You are the entrepreneur's trusted partner in building their business. Be helpful, insightful, and always focused on what matters most right now."""

    def chat(self, user_message: str, stream: bool = False) -> str:
        """
        Process a message from the entrepreneur.

        Args:
            user_message: The entrepreneur's message
            stream: Whether to stream the response

        Returns:
            Agent's response
        """
        # Save user message to database
        self.db.save_message(
            entrepreneur_id=self.entrepreneur_id,
            agent_name=self.AGENT_NAME,
            role="user",
            content=user_message
        )

        # Get conversation history (last 20 messages for context)
        history = self.db.get_conversation_history(
            entrepreneur_id=self.entrepreneur_id,
            agent_name=self.AGENT_NAME,
            limit=20
        )

        # Format for LLM
        messages = self.llm.format_conversation_history(history)

        # Add current message
        messages.append({"role": "user", "content": user_message})

        # Get response from LLM
        if stream:
            # Streaming response
            response_chunks = []
            for chunk in self.llm.stream_chat(
                system_prompt=self.get_system_prompt(),
                messages=messages,
                temperature=self.config.llm_temperature,
                max_tokens=self.config.llm_max_tokens
            ):
                print(chunk, end='', flush=True)
                response_chunks.append(chunk)
            print()  # New line after streaming
            response = ''.join(response_chunks)
        else:
            # Non-streaming response
            response = self.llm.chat(
                system_prompt=self.get_system_prompt(),
                messages=messages,
                temperature=self.config.llm_temperature,
                max_tokens=self.config.llm_max_tokens
            )

        # Save assistant response to database
        self.db.save_message(
            entrepreneur_id=self.entrepreneur_id,
            agent_name=self.AGENT_NAME,
            role="assistant",
            content=response
        )

        # Analyze response for phase/cognitive state changes
        self._update_context_from_conversation(user_message, response)

        return response

    def _update_context_from_conversation(self, user_message: str, response: str):
        """
        Analyze conversation to detect phase transitions or cognitive state changes.

        This is a simplified version - production would use more sophisticated analysis.
        """
        # Detect cognitive state from language patterns
        user_lower = user_message.lower()

        # Formation mode indicators
        if any(word in user_lower for word in ['what if', 'could we', 'i wonder', 'brainstorm', 'ideas']):
            if self.cognitive_state != 'Formation':
                self.cognitive_state = 'Formation'
                self._update_business_context()

        # Testing mode indicators
        elif any(word in user_lower for word in ['test', 'experiment', 'validate', 'try', 'did it work']):
            if self.cognitive_state != 'Testing':
                self.cognitive_state = 'Testing'
                self._update_business_context()

        # Response mode indicators
        elif any(word in user_lower for word in ['based on', 'decided', 'going to', 'will', 'next step']):
            if self.cognitive_state != 'Response':
                self.cognitive_state = 'Response'
                self._update_business_context()

    def _update_business_context(self):
        """Update business context in database."""
        self.db.update_business_context(
            self.entrepreneur_id,
            business_phase=self.business_phase,
            cognitive_state=self.cognitive_state
        )

    def update_business_phase(self, new_phase: str):
        """
        Manually update business phase.

        Args:
            new_phase: One of Foundation, Strategy, Development, Launch
        """
        if new_phase not in self.PHASES:
            raise ValueError(f"Invalid phase: {new_phase}. Must be one of {self.PHASES}")

        self.business_phase = new_phase
        self._update_business_context()

    def get_morning_briefing(self) -> str:
        """
        Generate a morning briefing for the entrepreneur.

        Returns:
            Morning briefing text
        """
        prompt = f"""Generate a morning briefing for the entrepreneur.

Current context:
- Business Phase: {self.business_phase}
- Cognitive State: {self.cognitive_state}

The briefing should include:
1. A warm greeting
2. Current phase reminder
3. Top 3 priorities for today (based on phase)
4. Any important reminders or alerts
5. An encouraging note

Keep it concise (3-4 paragraphs max) and actionable."""

        messages = [{"role": "user", "content": prompt}]

        briefing = self.llm.chat(
            system_prompt=self.get_system_prompt(),
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )

        return briefing

    def get_evening_recap(self) -> str:
        """
        Generate an evening recap for reflection.

        Returns:
            Evening recap text
        """
        # Get today's conversation to understand what was accomplished
        history = self.db.get_conversation_history(
            entrepreneur_id=self.entrepreneur_id,
            agent_name=self.AGENT_NAME,
            limit=10
        )

        conversation_summary = "\n".join([
            f"- {msg['role']}: {msg['content'][:100]}..."
            for msg in history[:5]
        ])

        prompt = f"""Generate an evening recap for the entrepreneur.

Today's interactions:
{conversation_summary}

Current context:
- Business Phase: {self.business_phase}
- Cognitive State: {self.cognitive_state}

The recap should include:
1. What was accomplished today
2. Any important decisions or insights
3. Tomorrow's prep/priorities
4. Encouraging closing note

Keep it concise and reflective."""

        messages = [{"role": "user", "content": prompt}]

        recap = self.llm.chat(
            system_prompt=self.get_system_prompt(),
            messages=messages,
            temperature=0.7,
            max_tokens=600
        )

        return recap

    def get_status(self) -> Dict:
        """
        Get current status of the Chief of Staff and business context.

        Returns:
            Status dictionary
        """
        context = self.db.get_business_context(self.entrepreneur_id)
        message_count = len(self.db.get_conversation_history(
            self.entrepreneur_id,
            self.AGENT_NAME,
            limit=1000
        ))

        return {
            "agent_name": self.AGENT_NAME,
            "nickname": self.NICKNAME,
            "entrepreneur_id": self.entrepreneur_id,
            "business_phase": self.business_phase,
            "cognitive_state": self.cognitive_state,
            "total_messages": message_count,
            "context": context
        }
