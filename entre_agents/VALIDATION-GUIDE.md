# Chief of Staff Agent - Validation Guide

This guide walks through validating that the Chief of Staff agent is working correctly and behaving according to its specification.

---

## ✅ VALIDATION CHECKLIST

### Phase 1: Technical Validation (5-10 minutes)
- [ ] Dependencies install successfully
- [ ] Configuration loads from .env
- [ ] Database initializes correctly
- [ ] LLM client connects to Anthropic API
- [ ] CLI starts without errors
- [ ] Messages save to database
- [ ] Streaming responses work

### Phase 2: Functional Validation (15-20 minutes)
- [ ] Basic conversation works
- [ ] Context is maintained across messages
- [ ] Morning briefing generates appropriately
- [ ] Evening recap generates appropriately
- [ ] Status command shows correct information
- [ ] Cognitive state detection works
- [ ] Phase-appropriate responses

### Phase 3: Quality Validation (20-30 minutes)
- [ ] Tone matches specification (professional yet warm)
- [ ] Responses are concise by default
- [ ] Agent maintains strategic perspective
- [ ] Framework knowledge is accurate
- [ ] Proactive insights are valuable
- [ ] Recommendations are actionable

---

## PHASE 1: TECHNICAL VALIDATION

### Step 1: Environment Setup

```bash
cd entre_agents

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Expected Result:** All packages install without errors.

**Troubleshooting:**
- If `anthropic` fails: Ensure Python 3.8+
- If `psycopg2` fails: This is optional (only needed for PostgreSQL)

### Step 2: Configuration

```bash
# Copy template
cp .env.example .env

# Edit .env and add your API key
# ANTHROPIC_API_KEY=sk-ant-...
```

**Test Configuration:**
```bash
python -c "from src.core.config import Config; c = Config(); c.validate(); print('Config valid!')"
```

**Expected Result:** "Config valid!"

**Troubleshooting:**
- "ANTHROPIC_API_KEY not found" → Check .env file exists and has the key
- "Configuration validation failed" → Review .env against .env.example

### Step 3: Database Initialization

```bash
python -c "from src.core.config import Config; from src.core.database import DatabaseAdapter; c = Config(); db = DatabaseAdapter(c.get_database_connection_string(), c.database_type); print('Database initialized!')"
```

**Expected Result:**
- "Database initialized!"
- File created: `data/ventre.db`

**Verify Tables:**
```bash
sqlite3 data/ventre.db ".tables"
```

**Expected Output:**
```
agent_state        business_context   conversations      decisions
```

### Step 4: LLM Client Connection

```bash
python -c "from src.core.config import Config; from src.core.llm_client import LLMClient; c = Config(); llm = LLMClient(c.anthropic_api_key, 'anthropic'); print('LLM client initialized!')"
```

**Expected Result:** "LLM client initialized!"

**Troubleshooting:**
- ImportError: Run `pip install anthropic`
- API key error: Verify key format starts with `sk-ant-`

### Step 5: Start CLI

```bash
python src/cli.py
```

**Expected Output:**
```
============================================================
  VEntre AI Agent System - Chief of Staff
  Your AI-partnered entrepreneurship companion
============================================================

Chief of Staff is ready. Type 'quit', 'exit', or 'q' to end.
Type '/briefing' for morning briefing, '/recap' for evening recap.
Type '/status' to see current business context.
Type '/help' for more commands.
------------------------------------------------------------

You:
```

**✅ PASS CRITERIA:** CLI starts, shows banner, waits for input

---

## PHASE 2: FUNCTIONAL VALIDATION

### Test 1: Basic Conversation

**Input:**
```
You: Hello, I'm just getting started with my business idea.
```

**Expected Behavior:**
- Response appears (streaming or all at once)
- Agent acknowledges it's a new entrepreneur
- Response mentions Foundation phase
- Warm, professional tone
- Ends with a question or next step

**✅ PASS CRITERIA:**
- Response received within 10 seconds
- Tone is professional yet warm
- Mentions current business phase

**Example Good Response:**
```
Chief of Staff: Hello! Welcome to your entrepreneurial journey. I can see you're just
getting started - that's exciting!

Since you're at the very beginning, we're in what I call the Foundation phase. This is
all about exploring your idea and validating the problem before building anything.

What's the business idea you're exploring? I'd love to understand what problem you're
trying to solve.
```

### Test 2: Context Maintenance

**Input Sequence:**
```
You: I'm thinking about a meal planning app for busy parents.

[Wait for response]

You: What should I do first?
```

**Expected Behavior:**
- Second response references the meal planning app
- Doesn't ask "what's your idea" again
- Provides specific next steps for THIS idea
- Appropriate for Foundation phase

**✅ PASS CRITERIA:**
- Agent remembers previous message
- Recommendations are specific to meal planning app
- Suggests customer discovery/validation activities

### Test 3: Cognitive State Detection

**Test 3a: Formation Mode**
```
You: I'm brainstorming different approaches. What if we focused on weekly meal prep
instead of daily planning? Or maybe we could do meal kits? I wonder if subscription
model would work...
```

**Expected Behavior:**
- Recognizes exploratory language ("what if", "I wonder")
- Encourages divergent thinking
- Doesn't prematurely narrow options
- May explicitly acknowledge "formation mode"

**✅ PASS CRITERIA:** Response supports exploration, doesn't force decisions

**Test 3b: Testing Mode**
```
You: I interviewed 10 parents yesterday about their meal planning challenges.
Want to analyze the results with me?
```

**Expected Behavior:**
- Recognizes testing/validation activity
- Offers structured analysis support
- Asks about patterns or insights
- May acknowledge "testing mode"

**✅ PASS CRITERIA:** Response shifts to analytical, validation-focused support

**Test 3c: Response Mode**
```
You: Based on the interviews, I've decided to focus on weekly meal prep for
working parents with kids under 10. That's our target segment.
```

**Expected Behavior:**
- Recognizes decision-making
- Validates the decision with data
- Asks about next steps
- May acknowledge "response mode"

**✅ PASS CRITERIA:** Response supports conviction, asks about implementation

### Test 4: Morning Briefing

**Command:**
```
/briefing
```

**Expected Output:**
- Warm greeting
- Current phase mentioned (Foundation)
- 2-3 priorities listed
- Specific to current context
- Encouraging tone
- 3-5 paragraphs

**✅ PASS CRITERIA:**
- Contains greeting, phase, priorities, encouragement
- Concise (not overwhelming)
- Actionable

**Example Structure:**
```
Good morning! Here's your context for today:

PHASE: Foundation - we're exploring and validating your meal planning app idea

TODAY'S PRIORITIES:
🎯 Complete those customer interviews...
🎯 Document insights from yesterday...
⚠️ Remember: validate before building!

[Encouraging closing]
```

### Test 5: Evening Recap

**Prerequisites:** Have a few messages in conversation history

**Command:**
```
/recap
```

**Expected Output:**
- References today's conversation
- Acknowledges progress
- Previews tomorrow
- Reflective tone
- Encouraging close

**✅ PASS CRITERIA:**
- Mentions actual topics discussed
- Feels personalized (not generic)
- Forward-looking

### Test 6: Status Command

**Command:**
```
/status
```

**Expected Output:**
```
============================================================
CURRENT STATUS
============================================================
Agent: Chief of Staff (The Conductor)
Entrepreneur: default_user (or your custom ID)
Business Phase: Foundation
Cognitive State: Formation (or current state)
Total Messages: [number]
```

**✅ PASS CRITERIA:** All fields populated correctly

### Test 7: Database Persistence

**Test Steps:**
1. Have a conversation (3-4 messages)
2. Type `quit` to exit
3. Restart CLI: `python src/cli.py`
4. Type `/status` to check message count
5. Start new conversation

**Expected Behavior:**
- Message count increases from previous session
- New conversation can reference previous context
- Database file grows: `ls -lh data/ventre.db`

**✅ PASS CRITERIA:**
- History persists across sessions
- Agent can reference earlier conversations

---

## PHASE 3: QUALITY VALIDATION

### Test 8: Tone & Personality

**Evaluation Criteria:**

**Professional Yet Warm:** ✅ / ❌
- Uses "you/your" (not "one should")
- Acknowledges emotions/context
- Not robotic or overly formal
- Not too casual or unprofessional

**Concise by Default:** ✅ / ❌
- Most responses are 3-5 short paragraphs
- Gets to the point quickly
- Doesn't over-explain unless asked

**Organized & Structured:** ✅ / ❌
- Uses bullet points or numbered lists
- Clear sections (priorities, recommendations, etc.)
- Easy to scan

**Example Test:**
```
You: I'm feeling overwhelmed with everything I need to do.
```

**Good Response Indicators:**
- Acknowledges the feeling (empathy)
- Provides structure (prioritizes ruthlessly)
- Cuts through noise (identifies top 3 things)
- Encouraging but realistic

**Bad Response Indicators:**
- Generic platitudes
- Adds more to todo list
- Overly long explanation
- Ignores emotional context

### Test 9: Strategic Perspective

**Scenario Test:**
```
You: I'm thinking about adding a marketplace feature where meal prep chefs can
sell services. Should I build that into v1?
```

**Expected Behavior:**
- Recognizes this is likely premature (Foundation phase)
- Asks about validation of core problem first
- Doesn't dismiss idea, but suggests sequencing
- References execution order principles
- Respects autonomy (doesn't dictate)

**✅ PASS CRITERIA:**
- Helps think strategically about sequencing
- Doesn't just say "yes" or "no"
- Asks clarifying questions
- Maintains big picture view

### Test 10: Framework Knowledge

**Test Different Frameworks:**

**Lean Startup:**
```
You: What's the Build-Measure-Learn cycle?
```
**Expected:** Clear 2-3 sentence explanation, relevant to their context

**Business Model Canvas:**
```
You: Should I work on my business model canvas?
```
**Expected:** Explains what BMC is, when it's useful (Strategy phase), what it includes

**Customer Development:**
```
You: How many customer interviews should I do?
```
**Expected:** References Customer Development methodology, suggests 10-30 for patterns

**✅ PASS CRITERIA:**
- Accurate framework knowledge
- Explains in accessible language
- Applies to entrepreneur's context
- Offers to teach more if interested

### Test 11: Proactive Intelligence

**Test Scenario:**
```
You: I've decided to quit my job and work on this full-time.
```

**Expected Proactive Behavior:**
- Asks about runway/financial cushion
- Suggests CFO Agent consultation (even though not built yet)
- Probes strategic conviction vs. tactical timeline
- Balances support with reality check

**✅ PASS CRITERIA:**
- Asks important questions unprompted
- Brings up considerations entrepreneur may not have thought of
- Doesn't just agree, provides perspective

### Test 12: Phase-Appropriate Guidance

**Foundation Phase Test:**
```
You: I want to start coding the app this weekend.
```

**Expected Response:**
- Gently redirects to validation first
- Explains why sequencing matters
- Suggests lightweight validation approaches
- Doesn't forbid, but educates on risks
- May reference execution sequencing

**✅ PASS CRITERIA:**
- Appropriate hesitation about premature building
- Educational rather than prescriptive
- Respects autonomy while guiding

---

## STRESS TESTS

### Test 13: Long Context

**Steps:**
1. Have a 20-message conversation about your business
2. Refer back to something from message #2
3. See if agent remembers

**Example:**
```
[After 18 messages]
You: Remember when I mentioned the meal planning idea at the start? What did
I say about my target market?
```

**✅ PASS CRITERIA:** Agent accurately references earlier conversation

### Test 14: Rapid Questions

**Test:**
```
You: What should I do?
[Wait for response]
You: Why?
[Wait for response]
You: How long will that take?
```

**Expected Behavior:**
- Maintains context across rapid-fire questions
- "That" refers to correct thing from previous response
- Doesn't get confused

**✅ PASS CRITERIA:** Coherent multi-turn conversation

### Test 15: Edge Cases

**Unclear Input:**
```
You: umm not sure
```
**Expected:** Asks clarifying question

**Off-Topic:**
```
You: What's the weather like?
```
**Expected:** Redirects to business focus, but politely

**Empty Message:**
Just press Enter
**Expected:** CLI handles gracefully (skips empty input)

---

## VALIDATION SCORING

### Minimum Viable Validation (MVP)

**Must Pass (Critical):**
- [ ] Technical: CLI starts and responds
- [ ] Technical: Database saves messages
- [ ] Functional: Basic conversation works
- [ ] Functional: Context maintained across messages
- [ ] Quality: Tone is professional yet warm
- [ ] Quality: Responses are relevant and helpful

**If 6/6 above pass:** ✅ Agent is minimally viable, can proceed to build Agent #2

### Full Validation (Recommended)

**All 15 Tests Pass:**
- ✅ Agent is production-quality
- ✅ Ready for real entrepreneur use
- ✅ Proceed confidently to next agents

**12-14 Tests Pass:**
- ⚠️ Agent is good but has minor issues
- Note which tests failed
- Can proceed to Agent #2, but flag issues for later improvement

**<12 Tests Pass:**
- ❌ Agent needs refinement
- Review failures and debug
- Focus on critical functionality first

---

## COMMON ISSUES & FIXES

### Issue: Responses are too verbose

**Diagnosis:** System prompt may need adjustment
**Fix:** Reduce temperature in .env: `LLM_TEMPERATURE=0.5`

### Issue: Agent doesn't remember conversation

**Check:**
```bash
sqlite3 data/ventre.db "SELECT COUNT(*) FROM conversations;"
```
If 0, messages aren't saving. Check database.py save_message() method.

### Issue: Cognitive state never changes

**Diagnosis:** Detection logic may be too strict
**Check:** Add debug print in `_update_context_from_conversation()`
**Note:** This is expected to be simple in v1, can improve later

### Issue: Streaming doesn't work

**Workaround:** Use `--no-stream` flag
**Debug:** Check firewall/network settings

### Issue: "Too many tokens" error

**Diagnosis:** Conversation history too long
**Fix:** Reduce history limit in chief_of_staff.py (line with `limit=20`)

---

## RECORDING YOUR VALIDATION

Create a simple log as you test:

```
CHIEF OF STAFF VALIDATION LOG
Date: ___________
Tester: ___________

TECHNICAL VALIDATION:
[✓] Dependencies installed
[✓] Configuration loaded
[✓] Database initialized
[✓] LLM connected
[✓] CLI started
[ ] Messages saved
[ ] Streaming works

FUNCTIONAL VALIDATION:
[✓] Basic conversation
[✓] Context maintained
[✓] Morning briefing
[ ] Evening recap
[ ] Status command
[ ] Cognitive state detection
[ ] Phase-appropriate responses

QUALITY VALIDATION:
[ ] Tone matches spec
[ ] Concise responses
[ ] Strategic perspective
[ ] Framework knowledge
[ ] Proactive insights
[ ] Actionable recommendations

OVERALL: MVP PASS / FULL PASS / NEEDS WORK

NOTES:
- Response quality is excellent
- Tone could be slightly warmer
- Framework explanations are clear
- Ready to proceed to Agent #2

```

---

## SUCCESS CRITERIA

**Minimum Success:**
- Agent responds coherently
- Conversation flows naturally
- Context is maintained
- Helpful and relevant

**Full Success:**
- All above PLUS:
- Tone matches Chief of Staff spec exactly
- Proactively surfaces insights
- Framework knowledge is accurate
- Phase and cognitive state adaptations work
- Briefings and recaps are valuable

---

## NEXT STEPS AFTER VALIDATION

### If Validation Passes:
1. Document any minor issues found
2. Note any prompt adjustments needed
3. Celebrate! 🎉
4. Move on to building Agent #2 (Market Discovery)

### If Validation Fails:
1. Document specific failures
2. Debug issues systematically
3. Adjust code/prompts as needed
4. Re-run validation tests
5. Iterate until MVP criteria met

---

**Validation should take 30-60 minutes total.**

**Start with Phase 1 (technical), then Phase 2 (functional), then Phase 3 (quality).**

**Document your findings and share feedback for improvements!**
