# Part 3: Agent Architecture

This section provides complete specifications for all 26 agents in the entrepreneurial AI ecosystem.

---

## Overview

The agent architecture consists of three layers:

1. **Master Orchestrator (1 agent)** - Coordinates the entire system
2. **Category Specialists (20 agents)** - Deep expertise in each entrepreneurial domain
3. **Support Specialists (5 agents)** - Cross-cutting capabilities and advanced coordination

Each agent specification includes:
- Core identity and responsibilities
- Behavioral characteristics
- AI impact level (HIGH/MEDIUM/LOW)
- Phase-specific behaviors (Foundation/Strategy/Development/Launch)
- Cognitive loop adaptations (Formation/Testing/Response)
- Framework connections (Lean Startup, BMC, Customer Development, etc.)
- Required tools and data access
- Native capabilities
- Proactive behaviors
- Example interactions across scenarios
- Coordination patterns with other agents

---

## Master Orchestrator

### [00. Chief of Staff Agent](./part-3-agents/00-chief-of-staff.md)
**Role:** Master Orchestrator
**Nickname:** "The Conductor"
**Primary Function:** Coordinates all specialist agents, maintains holistic business context, detects phases and cognitive states, orchestrates cross-domain decisions

---

## Category Specialists (1-20)

### [01. Vision, Purpose & Alignment Agent](./part-3-agents/01-vision-alignment.md)
**Nickname:** "The North Star Keeper"
**Domain:** Vision, mission, values, founder alignment
**AI Impact:** MEDIUM

### [02. Business Archetype & Capital Strategy Agent](./part-3-agents/02-business-archetype.md)
**Nickname:** "The Architect"
**Domain:** Business model type, funding strategy, capital structure
**AI Impact:** MEDIUM

### [03. Founder & Team Readiness Agent](./part-3-agents/03-founder-team-readiness.md)
**Nickname:** "The Foundation Builder"
**Domain:** Team skills, equity splits, founder agreements, hiring
**AI Impact:** MEDIUM-HIGH

### [04. Market Discovery & Validation Agent](./part-3-agents/04-market-discovery.md)
**Nickname:** "The Customer Whisperer"
**Domain:** Customer research, market sizing, validation, insights
**AI Impact:** HIGH

### [05. Business & Revenue Model Agent](./part-3-agents/05-business-revenue-model.md)
**Nickname:** "The Monetization Strategist"
**Domain:** Revenue models, pricing, unit economics, scalability
**AI Impact:** HIGH

### [06. Market Positioning & Differentiation Agent](./part-3-agents/06-market-positioning.md)
**Nickname:** "The Strategist"
**Domain:** Competitive analysis, positioning, differentiation, market timing
**AI Impact:** HIGH

### [07. Brand Identity & Storytelling Agent](./part-3-agents/07-brand-storytelling.md)
**Nickname:** "The Storyteller"
**Domain:** Brand identity, voice, origin stories, emotional connection
**AI Impact:** MEDIUM

### [08. Ecosystem & Competitive Landscape Agent](./part-3-agents/08-ecosystem-competitive.md)
**Nickname:** "The Intel Chief"
**Domain:** Industry dynamics, competitive intelligence, partnerships, trends
**AI Impact:** HIGH

### [09. Legal, Risk, Compliance & Ethics Agent](./part-3-agents/09-legal-risk-compliance.md)
**Nickname:** "The Protector"
**Domain:** Legal structure, contracts, IP, compliance, risk management
**AI Impact:** MEDIUM-HIGH

### [10. Product & Technology Development Agent](./part-3-agents/10-product-technology.md)
**Nickname:** "The Builder"
**Domain:** Product roadmap, technical architecture, development, MVP
**AI Impact:** HIGH

### [11. Route-to-Market & Go-to-Market Strategy Agent](./part-3-agents/11-gtm-strategy.md)
**Nickname:** "The Growth Architect"
**Domain:** Customer acquisition, marketing, sales, launch strategy
**AI Impact:** HIGH

### [12. People, Culture & Leadership Agent](./part-3-agents/12-people-culture.md)
**Nickname:** "The People Builder"
**Domain:** Recruiting, culture, compensation, leadership development
**AI Impact:** MEDIUM

### [13. Capital & Financing Agent](./part-3-agents/13-capital-financing.md)
**Nickname:** "The CFO"
**Domain:** Fundraising, financial modeling, burn rate, runway
**AI Impact:** HIGH

### [14. Operations, Systems & Data Infrastructure Agent](./part-3-agents/14-operations-systems.md)
**Nickname:** "The Systems Engineer"
**Domain:** Operations, processes, tools, data infrastructure, analytics
**AI Impact:** HIGH

### [15. Customer Success, Retention & Experience Agent](./part-3-agents/15-customer-success.md)
**Nickname:** "The Retention Champion"
**Domain:** Onboarding, support, retention, customer satisfaction
**AI Impact:** HIGH

### [16. Growth & Scaling Agent](./part-3-agents/16-growth-scaling.md)
**Nickname:** "The Scaler"
**Domain:** Growth strategies, PMF, expansion, scaling operations
**AI Impact:** HIGH

### [17. Innovation, Learning & Adaptability Agent](./part-3-agents/17-innovation-learning.md)
**Nickname:** "The R&D Lead"
**Domain:** Experimentation, R&D, learning systems, pivoting
**AI Impact:** MEDIUM-HIGH

### [18. Founder Longevity & Resilience Agent](./part-3-agents/18-founder-longevity.md)
**Nickname:** "The Resilience Coach"
**Domain:** Founder wellbeing, stress management, work-life balance
**AI Impact:** LOW-MEDIUM

### [19. Impact & Sustainability Agent](./part-3-agents/19-impact-sustainability.md)
**Nickname:** "The Purpose Guardian"
**Domain:** ESG, social impact, sustainability, responsible business
**AI Impact:** MEDIUM

### [20. Exit & Legacy Strategy Agent](./part-3-agents/20-exit-legacy.md)
**Nickname:** "The Transition Planner"
**Domain:** Exit pathways, succession, legacy, liquidity planning
**AI Impact:** MEDIUM

---

## Support Specialists (21-25)

### [21. Methodology Coach Agent](./part-3-agents/21-methodology-coach.md)
**Nickname:** "The Framework Teacher"
**Domain:** Teaching Lean Startup, BMC, Customer Development, Design Thinking
**AI Impact:** HIGH

### [22. Cognitive Loop Support Agent](./part-3-agents/22-cognitive-loop-support.md)
**Nickname:** "The Mindset Guide"
**Domain:** Detecting and supporting cognitive states (Formation/Testing/Response)
**AI Impact:** MEDIUM

### [23. Execution Sequencer Agent](./part-3-agents/23-execution-sequencer.md)
**Nickname:** "The Path Guide"
**Domain:** Activity sequencing, dependency management, preventing premature optimization
**AI Impact:** HIGH

### [24. Cross-Domain Integration Agent](./part-3-agents/24-cross-domain-integration.md)
**Nickname:** "The Connector"
**Domain:** Coordinating across agents, synthesizing multi-domain decisions
**AI Impact:** HIGH

### [25. Strategic Conviction Keeper Agent](./part-3-agents/25-strategic-conviction.md)
**Nickname:** "The Compass"
**Domain:** Tracking core beliefs vs tactical experiments, pivot vs persevere
**AI Impact:** MEDIUM

---

## Agent Interaction Patterns

### Coordination Hierarchy

```
                     Chief of Staff (Orchestrator)
                              |
            __________________|___________________
           |                  |                   |
    Category Specialists  Support Specialists  Context Systems
    (Domain Experts)      (Cross-cutting)      (State, Memory)
           |                  |
    Coordinate for      Enable advanced
    domain-specific     capabilities
    decisions           (sequencing, integration)
```

### Communication Flows

**Human → Agent:**
- Direct requests to Chief of Staff
- Specific questions to category specialists
- System observes all work and communication

**Agent → Human:**
- Proactive insights and alerts
- Responses to queries
- Daily/weekly summaries
- Cross-domain decision support

**Agent → Agent:**
- Consultation on cross-domain decisions
- Information sharing
- Conflict resolution
- Coordinated recommendations

---

## Using This Section

Each agent specification file follows a consistent format:

1. **Header** - Name, nickname, core identity
2. **Core Responsibilities** - What the agent does
3. **Behavioral Characteristics** - Personality and approach
4. **AI Impact Level** - HIGH/MEDIUM/LOW with reasoning
5. **Phase-Specific Behaviors** - How agent adapts across business phases
6. **Cognitive Loop Adaptations** - How agent responds to Formation/Testing/Response modes
7. **Framework Connections** - Links to entrepreneurial frameworks
8. **Required Tools** - Data sources and integrations needed
9. **Native Capabilities** - Built-in AI capabilities
10. **Proactive Behaviors** - When and how agent surfaces insights
11. **Example Interactions** - Detailed conversation examples
12. **Coordination Patterns** - How agent works with others

**For Implementers:**
Read each agent specification to understand required capabilities, tool integrations, and coordination protocols.

**For Entrepreneurs:**
Understand what each agent can help with and when to consult them.

**For Designers:**
Use specifications to design user interfaces and interaction patterns.

---

**Next:** Begin with [Chief of Staff Agent](./part-3-agents/00-chief-of-staff.md) or jump to any specific agent above.

**Continue to:** [Part 4: Agent Behavioral Models & Required Tools](./part-4-behavioral-models-tools.md)
