# VEntre AI Agent System

AI-partnered entrepreneurship support system featuring intelligent agents that help entrepreneurs build successful businesses.

## Overview

The VEntre system consists of multiple AI agents that work together to support entrepreneurs through their journey:

**Currently Implemented:**
- ✅ **Chief of Staff** - Master orchestrator and primary interface

**Planned Agents:**
- 🔜 **Market Discovery Agent** - Customer research and validation
- 🔜 **Product & Technology Agent** - MVP scoping and technical guidance
- 🔜 **Capital & Financing Agent** - Financial modeling and fundraising

## Architecture

```
VEntre System
├── Chief of Staff (Orchestrator)
│   ├── Context Management
│   ├── Phase Detection
│   ├── Agent Coordination
│   └── Proactive Intelligence
│
├── Specialist Agents (Coming Soon)
│   ├── Market Discovery
│   ├── Product & Technology
│   └── Capital & Financing
│
└── Core Infrastructure
    ├── Database Layer (SQLite/PostgreSQL)
    ├── LLM Client (Anthropic Claude)
    └── Configuration Management
```

## Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/))

### 2. Installation

```bash
# Clone the repository (if not already done)
cd entre_agents

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# Required: ANTHROPIC_API_KEY=your_key_here
```

### 4. Run the Chief of Staff

```bash
# Start interactive chat
python src/cli.py

# Get morning briefing
python src/cli.py --briefing

# Get evening recap
python src/cli.py --recap
```

## Configuration

All configuration is done via the `.env` file. See `.env.example` for all available options.

### Required Settings

```env
# Anthropic Claude API Key (REQUIRED)
ANTHROPIC_API_KEY=your_api_key_here
```

### Optional Settings

```env
# Database (defaults to SQLite)
DATABASE_TYPE=sqlite
DATABASE_PATH=data/ventre.db

# For cloud/production (PostgreSQL)
# DATABASE_TYPE=postgresql
# DATABASE_URL=postgresql://user:pass@localhost/db

# LLM Settings
LLM_PROVIDER=anthropic
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=4096

# Your entrepreneur identifier
ENTREPRENEUR_ID=your_username
```

## Usage Examples

### Interactive Chat

```bash
python src/cli.py
```

```
You: What should I focus on today?

Chief of Staff: Good morning! Here's your context for today:

PHASE: Foundation - we're exploring and validating
FOCUS: You're in formation mode - generating possibilities

TODAY'S PRIORITIES:
🎯 Complete 3 customer discovery interviews
🎯 Document insights from yesterday's conversations
⚠️ Resist urge to start coding (validate first!)

What's your #1 priority today?
```

### Morning Briefing

```bash
python src/cli.py --briefing
```

### Evening Recap

```bash
python src/cli.py --recap
```

### CLI Commands

While in interactive mode, you can use these commands:

- `/briefing` - Get morning briefing
- `/recap` - Get evening recap
- `/status` - Show current business context
- `/help` - Show available commands
- `quit` or `exit` - End session

## Understanding Business Phases

The Chief of Staff tracks your business phase and adapts its guidance:

### Foundation Phase
**Focus:** Exploration and validation
- Encourage customer conversations
- Prevent premature building
- Emphasize learning over execution

### Strategy Phase
**Focus:** Strategic planning and design
- Facilitate strategic planning
- Complete frameworks (BMC, etc.)
- Crystallize direction from options

### Development Phase
**Focus:** Execution and rapid iteration
- Maintain execution focus
- Support rapid iteration
- Track progress toward product-market fit

### Launch Phase
**Focus:** Scaling and optimization
- Optimize over experiment
- Support scaling decisions
- Monitor performance metrics

## Understanding Cognitive States

The agent adapts to your cognitive mode:

### Formation Mode
- You're exploring possibilities
- Generating creative options
- Agent encourages divergent thinking

### Testing Mode
- You're validating hypotheses
- Running experiments
- Agent provides structured support

### Response Mode
- You're making decisions based on results
- Integrating learnings
- Agent helps distinguish strategic vs tactical

## Database

The system uses a database-agnostic design:

**Local Development (SQLite):**
- No setup required
- Database file created automatically in `data/ventre.db`
- Perfect for single-user local use

**Cloud/Production (PostgreSQL):**
- Set `DATABASE_TYPE=postgresql` in `.env`
- Provide `DATABASE_URL` connection string
- Supports concurrent users

## Project Structure

```
entre_agents/
├── src/
│   ├── core/
│   │   ├── database.py       # Database abstraction layer
│   │   ├── llm_client.py     # LLM API wrapper
│   │   └── config.py         # Configuration management
│   │
│   ├── agents/
│   │   └── chief_of_staff.py # Chief of Staff agent
│   │
│   └── cli.py                 # Command-line interface
│
├── docs/
│   ├── v2/                    # Agent specifications
│   └── RobKen/                # Historical materials
│
├── config/
├── tests/
├── .env.example               # Example configuration
├── .gitignore
├── requirements.txt
└── README.md
```

## Development

### Adding New Agents

To add a new specialist agent:

1. Create agent file in `src/agents/your_agent.py`
2. Follow the pattern in `chief_of_staff.py`
3. Define system prompt based on agent spec in `docs/v2/`
4. Add to CLI or API interface

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/
flake8 src/
```

## API Keys & Costs

### Anthropic Claude API

- **Get Key:** https://console.anthropic.com/
- **Pricing:** ~$3-15 per 1M tokens (varies by model)
- **Recommended Model:** Claude 3.5 Sonnet (best balance of capability/cost)

### Expected Costs

**Light Usage** (10-20 messages/day):
- ~$0.50-2/day
- ~$15-60/month

**Heavy Usage** (100+ messages/day):
- ~$2-10/day
- ~$60-300/month

## Troubleshooting

### "ANTHROPIC_API_KEY not found in environment"

1. Make sure you've created `.env` file from `.env.example`
2. Add your API key: `ANTHROPIC_API_KEY=sk-ant-...`
3. Restart the application

### "Configuration validation failed"

Check that all required fields in `.env` are set correctly.

### Database errors

- **SQLite:** Ensure the `data/` directory is writable
- **PostgreSQL:** Verify your `DATABASE_URL` connection string is correct

### Import errors

Make sure you've installed all dependencies:

```bash
pip install -r requirements.txt
```

## Security Notes

- ⚠️ **NEVER commit `.env` file** (contains API keys)
- ⚠️ API keys are sensitive - keep them secure
- ⚠️ Database file may contain business data - protect it
- ✅ `.gitignore` is configured to exclude sensitive files

## Next Steps

1. **Get your API key** from Anthropic
2. **Configure `.env`** with your key
3. **Start chatting** with the Chief of Staff
4. **Explore features** like morning briefings and status tracking

## Support & Documentation

- **Full Documentation:** See `docs/v2/` for detailed agent specifications
- **Historical Context:** See `docs/RobKen/` for original Quatere/Foundry materials
- **Issues:** Report bugs or request features via GitHub issues

## License

[To be determined]

---

Built with ❤️ for entrepreneurs who are building the future.
