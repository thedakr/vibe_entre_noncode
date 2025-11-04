# Part 9: Technical Architecture - Implementation Guide

**Purpose:** This document provides the complete technical specification for implementing the AI Agent Framework v2.0 as a working system.

**Audience:** Software architects, engineering teams, technical founders building the MVP

**What This Covers:**
- System architecture and component design
- Technology stack recommendations with justifications
- Data architecture and schemas
- Implementation patterns and code structures
- Deployment and operations
- Security and privacy architecture
- Development roadmap with sequencing
- Alternative approaches and trade-offs

---

## Table of Contents

1. [System Architecture Overview](#system-architecture-overview)
2. [Technology Stack](#technology-stack)
3. [Core Components](#core-components)
4. [Data Architecture](#data-architecture)
5. [Agent Implementation Patterns](#agent-implementation-patterns)
6. [Integration Architecture](#integration-architecture)
7. [Deployment & Operations](#deployment--operations)
8. [Security & Privacy](#security--privacy)
9. [Development Roadmap](#development-roadmap)
10. [Alternative Approaches](#alternative-approaches)

---

## System Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ENTREPRENEUR                                 │
│                    (Terminal / Web UI / Desktop App)                 │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ CLI Client   │  │  Web Dashboard│  │ Desktop Notifications   │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   ORCHESTRATION LAYER                                │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              Chief of Staff Agent (Orchestrator)             │  │
│  │  - Routes requests to specialists                            │  │
│  │  - Synthesizes multi-agent responses                         │  │
│  │  - Manages conversation flow                                 │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    SPECIALIST AGENTS LAYER                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────────┐ │
│  │  Market    │  │  Product   │  │  Capital   │  │  Strategic   │ │
│  │ Discovery  │  │    Agent   │  │   Agent    │  │  Conviction  │ │
│  └────────────┘  └────────────┘  └────────────┘  └──────────────┘ │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────────┐ │
│  │ Methodology│  │   [Future  │  │   [Future  │  │   [Future    │ │
│  │   Coach    │  │   Agents]  │  │   Agents]  │  │   Agents]    │ │
│  └────────────┘  └────────────┘  └────────────┘  └──────────────┘ │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    INTELLIGENCE LAYER                                │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │  LLM Interface   │  │  Prompt Manager  │  │  Response       │  │
│  │  (Claude/GPT)    │  │  (System Prompts)│  │  Synthesizer    │  │
│  └──────────────────┘  └──────────────────┘  └─────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   OPERATIONAL SYSTEMS LAYER                          │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Context State Manager                                       │  │
│  │  - Business phase detection                                  │  │
│  │  - Business type detection                                   │  │
│  │  - Cognitive state tracking                                  │  │
│  │  - Single source of truth for all context                    │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Proactive Intelligence Engine                               │  │
│  │  - Background monitoring loop                                │  │
│  │  - Signal detection & filtering                              │  │
│  │  - Insight surfacing logic                                   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Strategic Conviction Tracker                                │  │
│  │  - Conviction vs. tactical separation                        │  │
│  │  - Evolution tracking over time                              │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Execution Sequencer                                         │  │
│  │  - Activity dependency mapping                               │  │
│  │  - Violation detection                                       │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Memory & Learning System                                    │  │
│  │  - Short/medium/long-term memory                             │  │
│  │  - Preference learning                                       │  │
│  │  - Outcome tracking                                          │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    OBSERVATION LAYER                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │  File System     │  │  Activity        │  │  Calendar/      │  │
│  │  Monitor         │  │  Tracker         │  │  Email Monitor  │  │
│  │  (watchdog)      │  │  (app usage)     │  │  (optional)     │  │
│  └──────────────────┘  └──────────────────┘  └─────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │  PostgreSQL      │  │  Redis           │  │  Vector Store   │  │
│  │  (context,       │  │  (cache,         │  │  (embeddings,   │  │
│  │   decisions,     │  │   real-time      │  │   semantic      │  │
│  │   history)       │  │   state)         │  │   search)       │  │
│  └──────────────────┘  └──────────────────┘  └─────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    INTEGRATION LAYER                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │  Financial APIs  │  │  Product/Dev     │  │  Marketing/     │  │
│  │  (Stripe, Plaid, │  │  Tools (GitHub,  │  │  Analytics      │  │
│  │   QuickBooks)    │  │  Linear, etc.)   │  │  (Mixpanel)     │  │
│  └──────────────────┘  └──────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

**Example: User Opens Financial Spreadsheet**

```
1. OBSERVATION
   ├─ File Monitor detects: /finances/runway-projection.xlsx opened
   └─ Activity Tracker logs: User active in Excel

2. CONTEXT INFERENCE
   ├─ Context State Manager receives event
   ├─ Infers domain: Financial modeling
   ├─ Checks current phase: Development phase
   └─ Checks cognitive state: Response mode (making decisions)

3. AGENT ACTIVATION
   ├─ Chief of Staff receives context + event
   ├─ Routes to: Capital & Financing Agent
   └─ Agent loads: Entrepreneur profile, recent financial data

4. PROACTIVE DECISION
   ├─ Capital Agent checks: Should I engage proactively?
   ├─ Detects: Burn rate increased 15% last month (significant signal)
   ├─ Filters: High-impact insight, actionable, timely
   └─ Decision: YES, engage proactively

5. RESPONSE GENERATION
   ├─ Agent retrieves: Runway data, burn rate trends
   ├─ Constructs prompt: System prompt (CFO role) + context + insight
   ├─ Calls LLM: Claude API with entrepreneur preferences
   └─ Generates message: "I see you're updating runway projections..."

6. DELIVERY
   ├─ Chief of Staff receives agent response
   ├─ Checks: Not interrupting focus time (10am, ok to notify)
   ├─ Sends to UI: Desktop notification
   └─ Logs interaction: Memory system records proactive engagement

7. USER RESPONSE (Optional)
   ├─ User clicks notification → Opens conversation
   ├─ User asks: "What's driving the burn increase?"
   ├─ Capital Agent retrieves detailed breakdown
   └─ Conversation continues...
```

---

## Technology Stack

### Core Technology Decisions

#### **1. Programming Language: Python**

**Why Python:**
- Rich AI/ML ecosystem (LangChain, LlamaIndex, transformers)
- Easy LLM API integration (OpenAI, Anthropic SDKs)
- Rapid development for MVP
- Large talent pool
- Strong async support (asyncio)

**Alternatives Considered:**
- TypeScript/Node.js: Good for web, but weaker AI ecosystem
- Go: Fast, but immature AI libraries
- Rust: Performance, but slower development

**Decision: Python 3.11+** for MVP, consider polyglot architecture later (Go for high-performance services)

---

#### **2. Agent Framework: Custom-Built with LangChain Components**

**Options Evaluated:**

| Framework | Pros | Cons | Verdict |
|-----------|------|------|---------|
| **LangChain** | Mature, extensive tooling, LLM abstractions | Can be overengineered, steep learning curve | ✅ Use selectively (LLM interface, memory, tools) |
| **AutoGen** (Microsoft) | Multi-agent orchestration, conversation patterns | Opinionated structure, less flexible | ⚠️ Reference for patterns, don't adopt wholesale |
| **CrewAI** | Simple multi-agent setup | Young, limited features | ❌ Too immature for production |
| **Custom** | Full control, optimized for our architecture | More upfront work, reinvent wheels | ✅ Build custom orchestration, use LangChain components |

**Decision: Hybrid Approach**
- **Custom orchestration layer** (Chief of Staff, agent coordination)
- **LangChain components** for:
  - LLM interface abstraction (easy to switch Claude ↔ GPT ↔ local models)
  - Memory management (ConversationBufferMemory, VectorStoreMemory)
  - Tool integration (function calling, API wrappers)
- **Custom agent implementations** (behavioral adaptation logic)

**Rationale:**
- Our architecture is novel (phase/cognitive adaptation, conviction tracking)
- LangChain is too opinionated for our orchestration needs
- But LangChain components save time on common patterns (memory, LLM calls)

---

#### **3. LLM Provider: Multi-Model Strategy**

**Primary: Claude 3.5 Sonnet (Anthropic)**

**Why Claude:**
- Strong reasoning for strategic/business advice
- Better at nuanced entrepreneurial guidance
- 200K context window (can include full business context)
- Function calling for tool use

**Secondary: GPT-4 Turbo (OpenAI)**

**Why GPT-4:**
- Fallback if Claude API issues
- Good for code generation (Product Agent)
- Faster for simple tasks

**Future: Local Models (Optional)**

**Why Local:**
- Privacy for sensitive financial data
- Cost optimization at scale
- Offline capability

**Models to Consider:**
- Llama 3 70B (Meta) - Good general reasoning
- Mixtral 8x7B - Fast, cost-effective
- Code Llama - For Product Agent code generation

**Implementation Pattern:**
```python
class LLMRouter:
    def __init__(self):
        self.primary = AnthropicClient(model="claude-3-5-sonnet-20241022")
        self.fallback = OpenAIClient(model="gpt-4-turbo")
        self.local = OllamaClient(model="llama3:70b")  # Optional

    def generate(self, prompt, task_type, privacy_level):
        # Route based on task and privacy requirements
        if privacy_level == "high":
            return self.local.generate(prompt)
        elif task_type == "code_generation":
            return self.fallback.generate(prompt)  # GPT-4 better at code
        else:
            return self.primary.generate(prompt)  # Claude default
```

**Decision: Claude primary, GPT-4 fallback, design for multi-model flexibility**

---

#### **4. Database Architecture: Polyglot Persistence**

**PostgreSQL (Primary Database)**

**For:**
- Context state (current business state)
- Decision history (all major decisions + rationale)
- Entrepreneur profile (preferences, patterns)
- Agent interaction logs
- Conviction tracking (strategic convictions + evidence)

**Why PostgreSQL:**
- ACID compliance (critical for decision history)
- Excellent JSON support (JSONB for flexible schemas)
- Time-series capabilities (for tracking evolution)
- Mature, reliable

**Schema Design:**
```sql
-- Core tables
CREATE TABLE entrepreneurs (
    id UUID PRIMARY KEY,
    name TEXT,
    profile JSONB,  -- Preferences, patterns, communication style
    created_at TIMESTAMP
);

CREATE TABLE business_context (
    id UUID PRIMARY KEY,
    entrepreneur_id UUID REFERENCES entrepreneurs(id),
    phase TEXT,  -- Foundation, Strategy, Development, Launch
    business_type JSONB,  -- {primary: "Physical Product", subtype: "Artisan"}
    convictions JSONB,  -- Strategic convictions array
    resources JSONB,  -- {runway: 6, team_size: 1, revenue: 531}
    updated_at TIMESTAMP
);

CREATE TABLE decisions (
    id UUID PRIMARY KEY,
    entrepreneur_id UUID REFERENCES entrepreneurs(id),
    decision TEXT,
    rationale TEXT,
    conviction_level FLOAT,  -- 0.0 to 1.0
    category TEXT,  -- strategic or tactical
    outcome JSONB,  -- Track what happened after decision
    created_at TIMESTAMP
);

CREATE TABLE agent_interactions (
    id UUID PRIMARY KEY,
    entrepreneur_id UUID REFERENCES entrepreneurs(id),
    agent_name TEXT,
    interaction_type TEXT,  -- proactive, on_demand, coordinated
    context JSONB,
    response TEXT,
    feedback JSONB,  -- User satisfaction, accepted/rejected advice
    created_at TIMESTAMP
);
```

**Redis (Cache & Real-Time State)**

**For:**
- Current conversation state (active chat sessions)
- Real-time agent coordination (which agents are active)
- Fast context lookups (avoid DB hits for every message)
- Rate limiting (LLM API calls)
- Background job queue (proactive monitoring tasks)

**Why Redis:**
- Sub-millisecond latency
- Pub/Sub for agent coordination
- TTL for automatic cleanup
- Simple data structures

**Usage Patterns:**
```python
# Current conversation state
redis.setex(
    f"conversation:{entrepreneur_id}:{session_id}",
    ttl=3600,  # 1 hour
    value=json.dumps({
        "messages": [...],
        "active_agents": ["market_discovery", "capital"],
        "context_snapshot": {...}
    })
)

# Agent coordination
redis.publish("agent:capital", json.dumps({
    "event": "runway_alert",
    "entrepreneur_id": "123",
    "urgency": "high"
}))
```

**Qdrant or Pinecone (Vector Database)**

**For:**
- Semantic search over past decisions
- Embedding-based context retrieval
- Pattern matching across entrepreneurs (later: community learning)

**Why Vector DB:**
- Find similar past situations ("When have I faced this before?")
- Retrieve relevant historical context
- Cross-entrepreneur pattern recognition

**Example Queries:**
```python
# Find similar past decisions
similar_decisions = vector_db.search(
    query_embedding=embed("Should I pivot pricing model?"),
    filter={"entrepreneur_id": "123", "category": "pricing"},
    top_k=5
)

# Retrieve relevant convictions
relevant_convictions = vector_db.search(
    query_embedding=embed("Customer segment confusion"),
    filter={"entrepreneur_id": "123", "type": "strategic_conviction"},
    top_k=3
)
```

**Decision: PostgreSQL + Redis + Qdrant**

---

#### **5. File/Activity Monitoring**

**watchdog (Python Library)**

**For:**
- File system monitoring (create, modify, delete, move)
- Directory watching with permissions

**Example:**
```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class BusinessFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            domain = self.infer_domain(file_path)
            # Trigger agent activation
            self.context_manager.process_file_event(file_path, domain)

observer = Observer()
observer.schedule(BusinessFileHandler(), path="/Users/entrepreneur/business", recursive=True)
observer.start()
```

**Platform-Specific App Monitoring:**

**macOS:**
- `NSWorkspace` API - Track active applications
- Accessibility API (with permission) - Monitor app focus/window titles

**Windows:**
- Win32 API (`GetForegroundWindow()`) - Active window tracking
- Process monitoring (`psutil`)

**Linux:**
- `xdotool` - Window management
- `wmctrl` - Workspace tracking

**Decision: Start with file monitoring (watchdog), add app tracking phase 2**

---

#### **6. Background Service Management**

**Options:**

| Approach | Use Case | Implementation |
|----------|----------|----------------|
| **systemd** (Linux) | Production server deployment | Unit file, auto-restart, logging |
| **launchd** (macOS) | macOS desktop deployment | plist file, daemon mode |
| **Docker + docker-compose** | Cross-platform, containerized | Container orchestration |
| **Python daemon** | Simple, development | `python-daemon` library |

**MVP Decision: Docker + docker-compose**

**Why:**
- Cross-platform (macOS, Linux, Windows)
- Easy local development
- Production-ready
- Isolates dependencies

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  orchestrator:
    build: ./services/orchestrator
    depends_on:
      - postgres
      - redis
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - DATABASE_URL=postgresql://user:pass@postgres:5432/agent_framework
      - REDIS_URL=redis://redis:6379
    volumes:
      - /Users/entrepreneur/business:/workspace:ro  # Read-only file access
    restart: unless-stopped

  proactive_engine:
    build: ./services/proactive_engine
    depends_on:
      - postgres
      - redis
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/agent_framework
      - REDIS_URL=redis://redis:6379

  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=secure_password

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  qdrant:
    image: qdrant/qdrant:latest
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  postgres_data:
  redis_data:
  qdrant_data:
```

---

#### **7. API Framework: FastAPI**

**Why FastAPI:**
- Modern async Python framework
- Auto-generated OpenAPI docs
- Type safety (Pydantic models)
- WebSocket support (for real-time agent streaming)
- Fast development

**API Structure:**
```python
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

app = FastAPI()

class ConversationRequest(BaseModel):
    entrepreneur_id: str
    message: str
    context_override: dict = None

@app.post("/api/v1/conversation")
async def converse(request: ConversationRequest):
    # Route to Chief of Staff
    response = await chief_of_staff.process_message(
        entrepreneur_id=request.entrepreneur_id,
        message=request.message
    )
    return {"response": response}

@app.websocket("/api/v1/stream")
async def stream_conversation(websocket: WebSocket):
    # Real-time streaming responses
    await websocket.accept()
    async for chunk in chief_of_staff.stream_response():
        await websocket.send_json({"chunk": chunk})
```

---

### Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Language** | Python 3.11+ | Core implementation |
| **Agent Framework** | Custom + LangChain components | Orchestration + utilities |
| **LLM Provider** | Claude 3.5 Sonnet (primary), GPT-4 (fallback) | Agent intelligence |
| **Primary DB** | PostgreSQL 15 | Context, decisions, history |
| **Cache/Queue** | Redis 7 | Real-time state, coordination |
| **Vector DB** | Qdrant | Semantic search, embeddings |
| **File Monitoring** | watchdog | File system events |
| **API Framework** | FastAPI | REST API + WebSockets |
| **Deployment** | Docker + docker-compose | Containerization |
| **Background Jobs** | Celery + Redis | Async task processing |

---

## Core Components

### 1. Context State Manager

**Responsibility:** Single source of truth for all business context

**Implementation:**

```python
# services/context_manager/state_manager.py

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import json

class BusinessPhase(Enum):
    FOUNDATION = "foundation"
    STRATEGY = "strategy"
    DEVELOPMENT = "development"
    LAUNCH = "launch"

class CognitiveState(Enum):
    FORMATION = "formation"
    TESTING = "testing"
    RESPONSE = "response"

@dataclass
class BusinessContext:
    entrepreneur_id: str
    phase: BusinessPhase
    phase_confidence: float
    business_type: Dict
    cognitive_state: Dict[str, CognitiveState]  # Per initiative
    resources: Dict  # {runway: 6, team_size: 1, mrr: 350}
    strategic_convictions: List[Dict]
    recent_activities: List[Dict]
    preferences: Dict  # Communication style, risk tolerance, etc.

class ContextStateManager:
    def __init__(self, db_client, redis_client):
        self.db = db_client
        self.redis = redis_client
        self.phase_detector = PhaseDetector()
        self.business_type_detector = BusinessTypeDetector()
        self.cognitive_detector = CognitiveStateDetector()

    async def get_context(self, entrepreneur_id: str) -> BusinessContext:
        """Get current context, from cache if available"""
        # Try cache first
        cached = await self.redis.get(f"context:{entrepreneur_id}")
        if cached:
            return BusinessContext(**json.loads(cached))

        # Load from database
        context_data = await self.db.fetch_one(
            "SELECT * FROM business_context WHERE entrepreneur_id = $1",
            entrepreneur_id
        )

        context = BusinessContext(**context_data)

        # Cache for 5 minutes
        await self.redis.setex(
            f"context:{entrepreneur_id}",
            300,
            json.dumps(context.__dict__)
        )

        return context

    async def update_context(self, entrepreneur_id: str, updates: Dict):
        """Update context with new data"""
        context = await self.get_context(entrepreneur_id)

        # Apply updates
        for key, value in updates.items():
            setattr(context, key, value)

        # Re-detect phase if significant changes
        if self._should_redetect_phase(updates):
            new_phase, confidence = await self.phase_detector.detect(context)
            context.phase = new_phase
            context.phase_confidence = confidence

        # Persist to database
        await self.db.execute(
            """
            UPDATE business_context
            SET phase = $1, business_type = $2, resources = $3, updated_at = NOW()
            WHERE entrepreneur_id = $4
            """,
            context.phase.value,
            json.dumps(context.business_type),
            json.dumps(context.resources),
            entrepreneur_id
        )

        # Invalidate cache
        await self.redis.delete(f"context:{entrepreneur_id}")

        return context

    async def process_activity(self, entrepreneur_id: str, activity: Dict):
        """Process new activity (file change, decision, etc.)"""
        context = await self.get_context(entrepreneur_id)

        # Add to recent activities
        context.recent_activities.append({
            "timestamp": datetime.now().isoformat(),
            "type": activity["type"],
            "data": activity["data"]
        })

        # Keep only last 50 activities
        context.recent_activities = context.recent_activities[-50:]

        # Infer business type if needed
        if not context.business_type:
            business_type = await self.business_type_detector.infer(
                context.recent_activities
            )
            context.business_type = business_type

        # Detect cognitive state for this activity
        if activity["type"] in ["decision", "experiment", "reflection"]:
            cognitive_state = await self.cognitive_detector.detect(
                activity, context
            )
            initiative = activity.get("initiative", "default")
            context.cognitive_state[initiative] = cognitive_state

        await self.update_context(entrepreneur_id, {
            "recent_activities": context.recent_activities,
            "business_type": context.business_type,
            "cognitive_state": context.cognitive_state
        })

        return context
```

**Phase Detection Implementation:**

```python
# services/context_manager/phase_detector.py

class PhaseDetector:
    """Detects business phase using multi-signal scoring (Part 5)"""

    def __init__(self):
        self.signal_weights = {
            "transaction_volume": 0.30,
            "product_state": 0.25,
            "channel_maturity": 0.20,
            "team_structure": 0.15,
            "revenue_consistency": 0.10
        }

    async def detect(self, context: BusinessContext) -> tuple[BusinessPhase, float]:
        """Returns (phase, confidence_score)"""

        scores = {
            BusinessPhase.FOUNDATION: 0.0,
            BusinessPhase.STRATEGY: 0.0,
            BusinessPhase.DEVELOPMENT: 0.0,
            BusinessPhase.LAUNCH: 0.0
        }

        # Signal 1: Transaction Volume
        txn_volume = context.resources.get("total_sales", 0)
        if txn_volume < 50:
            scores[BusinessPhase.FOUNDATION] += self.signal_weights["transaction_volume"]
        elif txn_volume < 200:
            scores[BusinessPhase.STRATEGY] += self.signal_weights["transaction_volume"]
        elif txn_volume < 1000:
            scores[BusinessPhase.DEVELOPMENT] += self.signal_weights["transaction_volume"]
        else:
            scores[BusinessPhase.LAUNCH] += self.signal_weights["transaction_volume"]

        # Signal 2: Product State
        product_state = self._analyze_product_state(context.recent_activities)
        if product_state == "experimentation":
            scores[BusinessPhase.FOUNDATION] += self.signal_weights["product_state"]
        elif product_state == "crystallizing":
            scores[BusinessPhase.STRATEGY] += self.signal_weights["product_state"]
        elif product_state == "iterating":
            scores[BusinessPhase.DEVELOPMENT] += self.signal_weights["product_state"]
        elif product_state == "optimizing":
            scores[BusinessPhase.LAUNCH] += self.signal_weights["product_state"]

        # Signal 3: Channel Maturity
        channels = context.resources.get("active_channels", [])
        if len(channels) == 0:
            scores[BusinessPhase.FOUNDATION] += self.signal_weights["channel_maturity"]
        elif len(channels) <= 2 and not self._has_scaled_channel(channels):
            scores[BusinessPhase.STRATEGY] += self.signal_weights["channel_maturity"]
        elif len(channels) >= 2 and self._has_scaled_channel(channels):
            scores[BusinessPhase.DEVELOPMENT] += self.signal_weights["channel_maturity"]
        else:
            scores[BusinessPhase.LAUNCH] += self.signal_weights["channel_maturity"]

        # Signal 4: Team Structure
        team_size = context.resources.get("team_size", 1)
        if team_size == 1:
            scores[BusinessPhase.FOUNDATION] += self.signal_weights["team_structure"] * 0.5
            scores[BusinessPhase.STRATEGY] += self.signal_weights["team_structure"] * 0.5
        elif team_size <= 5:
            scores[BusinessPhase.DEVELOPMENT] += self.signal_weights["team_structure"]
        else:
            scores[BusinessPhase.LAUNCH] += self.signal_weights["team_structure"]

        # Signal 5: Revenue Consistency
        revenue_consistency = self._calculate_revenue_consistency(context)
        if revenue_consistency < 0.3:
            scores[BusinessPhase.FOUNDATION] += self.signal_weights["revenue_consistency"]
        elif revenue_consistency < 0.6:
            scores[BusinessPhase.STRATEGY] += self.signal_weights["revenue_consistency"]
        elif revenue_consistency < 0.85:
            scores[BusinessPhase.DEVELOPMENT] += self.signal_weights["revenue_consistency"]
        else:
            scores[BusinessPhase.LAUNCH] += self.signal_weights["revenue_consistency"]

        # Determine winning phase
        detected_phase = max(scores, key=scores.get)
        confidence = scores[detected_phase]

        return detected_phase, confidence

    def _analyze_product_state(self, activities: List[Dict]) -> str:
        """Analyze recent activities to determine product development state"""
        # Look for keywords in activity descriptions
        experimentation_keywords = ["testing", "trying", "experimenting", "exploring"]
        crystallizing_keywords = ["focusing", "choosing", "selecting", "deciding"]
        iterating_keywords = ["improving", "optimizing", "refining", "fixing"]
        optimizing_keywords = ["scaling", "automating", "streamlining", "measuring"]

        recent_text = " ".join([
            act.get("description", "").lower()
            for act in activities[-20:]  # Last 20 activities
        ])

        if any(kw in recent_text for kw in experimentation_keywords):
            return "experimentation"
        elif any(kw in recent_text for kw in crystallizing_keywords):
            return "crystallizing"
        elif any(kw in recent_text for kw in iterating_keywords):
            return "iterating"
        elif any(kw in recent_text for kw in optimizing_keywords):
            return "optimizing"
        else:
            return "experimentation"  # Default
```

---

### 2. Agent Base Architecture

**Base Agent Class:**

```python
# services/agents/base_agent.py

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class AgentResponse:
    agent_name: str
    message: str
    confidence: float
    tools_used: List[str]
    follow_up_questions: List[str]
    metadata: Dict

class BaseAgent(ABC):
    """Base class for all specialist agents"""

    def __init__(
        self,
        name: str,
        domain: str,
        ai_impact_level: str,
        context_manager: ContextStateManager,
        llm_client: LLMRouter,
        db_client,
        vector_store
    ):
        self.name = name
        self.domain = domain
        self.ai_impact_level = ai_impact_level
        self.context = context_manager
        self.llm = llm_client
        self.db = db_client
        self.vector_store = vector_store

    async def process_request(
        self,
        entrepreneur_id: str,
        user_input: str,
        conversation_history: List[Dict]
    ) -> AgentResponse:
        """Main entry point for processing user requests"""

        # 1. Get current context
        context = await self.context.get_context(entrepreneur_id)

        # 2. Adapt behavior to phase and cognitive state
        system_prompt = await self.adapt_to_context(context)

        # 3. Retrieve relevant memory
        relevant_context = await self.retrieve_relevant_memory(
            entrepreneur_id, user_input
        )

        # 4. Generate response
        response = await self.generate_response(
            system_prompt=system_prompt,
            user_input=user_input,
            conversation_history=conversation_history,
            relevant_context=relevant_context,
            business_context=context
        )

        # 5. Log interaction
        await self.log_interaction(entrepreneur_id, user_input, response)

        return response

    @abstractmethod
    async def adapt_to_context(self, context: BusinessContext) -> str:
        """Generate system prompt adapted to phase/cognitive state"""
        pass

    @abstractmethod
    async def check_proactive_triggers(
        self,
        entrepreneur_id: str,
        context: BusinessContext
    ) -> Optional[AgentResponse]:
        """Check if agent should proactively surface insights"""
        pass

    async def retrieve_relevant_memory(
        self,
        entrepreneur_id: str,
        query: str
    ) -> List[Dict]:
        """Retrieve relevant past interactions and decisions"""

        # Embed the query
        query_embedding = await self.vector_store.embed(query)

        # Semantic search over past decisions
        similar_decisions = await self.vector_store.search(
            embedding=query_embedding,
            filter={"entrepreneur_id": entrepreneur_id, "domain": self.domain},
            top_k=5
        )

        return similar_decisions

    async def generate_response(
        self,
        system_prompt: str,
        user_input: str,
        conversation_history: List[Dict],
        relevant_context: List[Dict],
        business_context: BusinessContext
    ) -> AgentResponse:
        """Generate LLM response with full context"""

        # Construct messages
        messages = [
            {"role": "system", "content": system_prompt}
        ]

        # Add relevant memory as context
        if relevant_context:
            context_summary = self._format_relevant_context(relevant_context)
            messages.append({
                "role": "system",
                "content": f"Relevant past context:\n{context_summary}"
            })

        # Add conversation history
        messages.extend(conversation_history)

        # Add current user input
        messages.append({"role": "user", "content": user_input})

        # Call LLM
        llm_response = await self.llm.generate(
            messages=messages,
            task_type=self._get_task_type(),
            privacy_level=self._get_privacy_level(business_context)
        )

        return AgentResponse(
            agent_name=self.name,
            message=llm_response["content"],
            confidence=self._calculate_confidence(llm_response),
            tools_used=[],
            follow_up_questions=self._extract_follow_ups(llm_response),
            metadata={"tokens": llm_response.get("usage", {})}
        )

    async def log_interaction(
        self,
        entrepreneur_id: str,
        user_input: str,
        response: AgentResponse
    ):
        """Log interaction for learning and memory"""
        await self.db.execute(
            """
            INSERT INTO agent_interactions
            (entrepreneur_id, agent_name, user_input, response, metadata, created_at)
            VALUES ($1, $2, $3, $4, $5, NOW())
            """,
            entrepreneur_id,
            self.name,
            user_input,
            response.message,
            json.dumps(response.metadata)
        )
```

**Example: Capital Agent Implementation:**

```python
# services/agents/capital_agent.py

class CapitalAgent(BaseAgent):
    """Capital & Financing Agent (The CFO)"""

    def __init__(self, *args, **kwargs):
        super().__init__(
            name="Capital & Financing Agent",
            domain="finance",
            ai_impact_level="HIGH",
            *args,
            **kwargs
        )
        self.burn_threshold = 0.15  # Alert if burn increases >15%

    async def adapt_to_context(self, context: BusinessContext) -> str:
        """Adapt system prompt to phase and business type"""

        base_prompt = """You are the Capital & Financing Agent (nickname: "The CFO").
You are an expert in financial modeling, unit economics, runway management, and fundraising.
You provide data-driven financial guidance to entrepreneurs.
"""

        # Phase-specific adaptations
        if context.phase == BusinessPhase.FOUNDATION:
            phase_behavior = """
FOUNDATION PHASE BEHAVIOR:
- You are in TEACHING MODE - explain financial concepts (unit economics, COGS, margin, etc.)
- Focus on: Unit economics, break-even analysis, pricing validation
- Be encouraging - it's OK to lose money while learning
- Distinguish sweat equity from actual costs
- Help build basic financial tracking habits
"""
        elif context.phase == BusinessPhase.STRATEGY:
            phase_behavior = """
STRATEGY PHASE BEHAVIOR:
- Focus on: Path to profitability, channel economics, margin optimization
- Provide strategic financial insights (which channel is most profitable?)
- Help with growth planning and resource allocation
- Introduce: Cohort analysis, CAC:LTV ratios
"""
        elif context.phase == BusinessPhase.DEVELOPMENT:
            phase_behavior = """
DEVELOPMENT PHASE BEHAVIOR:
- Focus on: Burn rate, runway, fundraising urgency
- Monitor: Monthly burn multiple (burn ÷ net new MRR)
- Alert: Cash crises proactively
- Provide: Scenario modeling (cut burn vs. raise capital vs. accelerate revenue)
"""
        else:  # LAUNCH
            phase_behavior = """
LAUNCH PHASE BEHAVIOR:
- Focus on: Scaling economics, capital efficiency, financial operations
- Provide: Advanced metrics (gross margin %, rule of 40, burn multiple)
- Support: Fundraising strategy, financial forecasting
"""

        # Business type adaptations
        if context.business_type.get("primary") == "Physical Product":
            type_behavior = """
PHYSICAL PRODUCT FOCUS:
- Emphasize: COGS, inventory management, production costs
- Track: Unit economics (cost per unit, margin per unit)
- Consider: Bulk purchasing, production efficiency, shipping costs
- Metrics: Gross margin %, contribution margin
"""
        elif context.business_type.get("primary") == "SaaS":
            type_behavior = """
SAAS FOCUS:
- Emphasize: MRR, ARR, churn rate, CAC, LTV
- Track: Burn multiple, months to payback CAC
- Consider: Pricing models, seat-based vs usage-based
- Metrics: Rule of 40, net dollar retention
"""
        else:
            type_behavior = ""

        # Cognitive state adaptation (if in Response mode for financial decision)
        cognitive_note = ""
        if context.cognitive_state.get("financial_decision") == CognitiveState.RESPONSE:
            cognitive_note = """
RESPONSE MODE DETECTED:
The entrepreneur is making a financial decision based on test results.
- Help them interpret data objectively
- Present options with clear trade-offs
- Support decision-making, don't make the decision for them
- Prevent analysis paralysis
"""

        return base_prompt + phase_behavior + type_behavior + cognitive_note

    async def check_proactive_triggers(
        self,
        entrepreneur_id: str,
        context: BusinessContext
    ) -> Optional[AgentResponse]:
        """Check for proactive financial alerts"""

        # Trigger 1: Runway alert
        runway_months = context.resources.get("runway_months")
        if runway_months and runway_months < 3:
            return await self._generate_runway_alert(entrepreneur_id, runway_months)

        # Trigger 2: Burn rate spike
        burn_history = await self._get_burn_history(entrepreneur_id)
        if self._detect_burn_spike(burn_history):
            return await self._generate_burn_spike_alert(entrepreneur_id, burn_history)

        # Trigger 3: Pricing anomaly (selling below cost)
        if await self._detect_pricing_anomaly(entrepreneur_id, context):
            return await self._generate_pricing_alert(entrepreneur_id)

        return None

    async def _generate_runway_alert(
        self,
        entrepreneur_id: str,
        runway_months: float
    ) -> AgentResponse:
        """Generate proactive runway alert"""

        # Get detailed financial data
        financial_data = await self.db.fetch_one(
            "SELECT * FROM financial_metrics WHERE entrepreneur_id = $1 ORDER BY created_at DESC LIMIT 1",
            entrepreneur_id
        )

        burn_rate = financial_data["monthly_burn"]
        revenue = financial_data.get("mrr", 0)

        message = f"""🚨 RUNWAY ALERT:

At current burn (${burn_rate:,.0f}/month), you have {runway_months:.1f} months of runway remaining.

CONTEXT:
- Current MRR: ${revenue:,.0f}
- Monthly burn: ${burn_rate:,.0f}
- Bank balance: ${financial_data['balance']:,.0f}

RECOMMENDATION:
Fundraising typically takes 3-6 months. You need to either:
1. Start fundraising conversations NOW, or
2. Cut burn to extend runway

Want me to model scenarios for both options?
"""

        return AgentResponse(
            agent_name=self.name,
            message=message,
            confidence=0.95,
            tools_used=["financial_data_query"],
            follow_up_questions=[
                "Show me burn reduction scenarios",
                "What fundraising amount should I target?",
                "How long does fundraising typically take?"
            ],
            metadata={"trigger": "runway_alert", "urgency": "high"}
        )
```

---

### 3. Chief of Staff (Orchestrator)

**Orchestration Logic:**

```python
# services/orchestrator/chief_of_staff.py

class ChiefOfStaff:
    """Master orchestrator agent - coordinates all specialists"""

    def __init__(
        self,
        context_manager: ContextStateManager,
        specialists: Dict[str, BaseAgent],
        llm_client: LLMRouter
    ):
        self.context = context_manager
        self.specialists = specialists
        self.llm = llm_client

    async def process_message(
        self,
        entrepreneur_id: str,
        message: str,
        conversation_history: List[Dict] = None
    ) -> str:
        """Main orchestration logic"""

        if conversation_history is None:
            conversation_history = []

        # 1. Determine which specialist(s) to activate
        routing_decision = await self.route_request(
            entrepreneur_id, message, conversation_history
        )

        # 2. If single specialist, route directly
        if len(routing_decision["agents"]) == 1:
            agent_name = routing_decision["agents"][0]
            agent = self.specialists[agent_name]
            response = await agent.process_request(
                entrepreneur_id, message, conversation_history
            )
            return response.message

        # 3. If multiple specialists, coordinate
        elif len(routing_decision["agents"]) > 1:
            responses = await self.coordinate_multi_agent_response(
                entrepreneur_id,
                message,
                routing_decision["agents"],
                conversation_history
            )
            return responses

        # 4. If no specialist (general conversation), handle directly
        else:
            return await self.handle_general_conversation(
                entrepreneur_id, message, conversation_history
            )

    async def route_request(
        self,
        entrepreneur_id: str,
        message: str,
        conversation_history: List[Dict]
    ) -> Dict:
        """Determine which agent(s) should respond"""

        # Get business context
        context = await self.context.get_context(entrepreneur_id)

        # Use LLM to classify intent and route
        routing_prompt = f"""You are the Chief of Staff orchestrator.
Your job is to route entrepreneur requests to the appropriate specialist agent(s).

AVAILABLE SPECIALISTS:
- market_discovery: Customer research, validation, market analysis
- product: Product development, MVP scoping, technical decisions
- capital: Financial modeling, unit economics, fundraising
- conviction: Strategic conviction tracking, pivot vs persevere decisions
- methodology: Teaching entrepreneurial frameworks (Lean Startup, BMC, etc.)

CURRENT CONTEXT:
- Business Phase: {context.phase.value}
- Business Type: {context.business_type.get('primary', 'Unknown')}
- Recent Activities: {[a['type'] for a in context.recent_activities[-5:]]}

CONVERSATION HISTORY:
{self._format_history(conversation_history[-3:])}

ENTREPRENEUR MESSAGE:
"{message}"

TASK: Determine which specialist(s) should respond.
Return JSON: {{"agents": ["agent_name", ...], "reasoning": "why these agents"}}

If the request spans multiple domains, include multiple agents.
If it's general conversation, return empty agents array.
"""

        routing_response = await self.llm.generate(
            messages=[{"role": "user", "content": routing_prompt}],
            response_format="json"
        )

        return json.loads(routing_response["content"])

    async def coordinate_multi_agent_response(
        self,
        entrepreneur_id: str,
        message: str,
        agent_names: List[str],
        conversation_history: List[Dict]
    ) -> str:
        """Coordinate responses from multiple agents"""

        # Get responses from each specialist in parallel
        specialist_responses = await asyncio.gather(*[
            self.specialists[agent_name].process_request(
                entrepreneur_id, message, conversation_history
            )
            for agent_name in agent_names
        ])

        # Check for conflicts
        conflict = await self._detect_conflicts(specialist_responses)

        if conflict:
            # Synthesize conflicting perspectives
            return await self._synthesize_conflicting_advice(
                specialist_responses, conflict
            )
        else:
            # Combine complementary insights
            return await self._combine_insights(specialist_responses)

    async def _detect_conflicts(
        self,
        responses: List[AgentResponse]
    ) -> Optional[Dict]:
        """Detect if agents give contradictory advice"""

        # Use LLM to analyze if recommendations conflict
        conflict_check_prompt = f"""Analyze these recommendations from different specialists:

{self._format_responses(responses)}

Do these recommendations CONFLICT (recommend opposite actions)?

Return JSON: {{"conflict": true/false, "description": "what conflicts"}}
"""

        conflict_result = await self.llm.generate(
            messages=[{"role": "user", "content": conflict_check_prompt}],
            response_format="json"
        )

        conflict_data = json.loads(conflict_result["content"])

        return conflict_data if conflict_data["conflict"] else None

    async def _synthesize_conflicting_advice(
        self,
        responses: List[AgentResponse],
        conflict: Dict
    ) -> str:
        """Present conflicting perspectives with trade-offs"""

        synthesis_prompt = f"""You are the Chief of Staff. Multiple specialists provided conflicting advice:

{self._format_responses(responses)}

CONFLICT DETECTED:
{conflict['description']}

Your job: Present BOTH perspectives with trade-offs, let entrepreneur decide.

Format:
1. Acknowledge the conflict
2. Present Specialist A's perspective + rationale
3. Present Specialist B's perspective + rationale
4. Outline trade-offs of each approach
5. Ask entrepreneur which aligns with their priorities
"""

        synthesis = await self.llm.generate(
            messages=[{"role": "user", "content": synthesis_prompt}]
        )

        # Log conflict for learning
        await self._log_conflict(responses, conflict)

        return synthesis["content"]

    async def _combine_insights(
        self,
        responses: List[AgentResponse]
    ) -> str:
        """Combine complementary insights from multiple agents"""

        combination_prompt = f"""You are the Chief of Staff. Multiple specialists provided complementary insights:

{self._format_responses(responses)}

Your job: Synthesize these into a coherent, actionable response.

Guidelines:
- Don't just concatenate - integrate the insights
- Show how different perspectives connect
- Provide clear next steps
- Keep it concise (3-5 paragraphs max)
"""

        combined = await self.llm.generate(
            messages=[{"role": "user", "content": combination_prompt}]
        )

        return combined["content"]
```

---

### 4. Proactive Intelligence Engine

**Background Monitoring System:**

```python
# services/proactive_engine/monitor.py

import asyncio
from datetime import datetime, timedelta
from typing import List, Optional

class ProactiveEngine:
    """Continuously monitors for proactive engagement opportunities"""

    def __init__(
        self,
        context_manager: ContextStateManager,
        specialists: Dict[str, BaseAgent],
        notification_service: NotificationService
    ):
        self.context = context_manager
        self.specialists = specialists
        self.notifications = notification_service
        self.check_interval = 300  # 5 minutes
        self.is_running = False

    async def start(self):
        """Start the proactive monitoring loop"""
        self.is_running = True
        while self.is_running:
            try:
                await self.check_all_entrepreneurs()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Proactive engine error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error

    async def check_all_entrepreneurs(self):
        """Check for proactive opportunities across all entrepreneurs"""

        # Get list of active entrepreneurs
        entrepreneurs = await self.db.fetch_all(
            "SELECT id FROM entrepreneurs WHERE status = 'active'"
        )

        # Check each entrepreneur in parallel
        await asyncio.gather(*[
            self.check_entrepreneur(e["id"])
            for e in entrepreneurs
        ])

    async def check_entrepreneur(self, entrepreneur_id: str):
        """Check if any agent should proactively engage with this entrepreneur"""

        # Get current context
        context = await self.context.get_context(entrepreneur_id)

        # Check focus time (don't interrupt)
        if self._is_focus_time(entrepreneur_id):
            return

        # Check each specialist for proactive triggers
        insights = []
        for agent_name, agent in self.specialists.items():
            insight = await agent.check_proactive_triggers(
                entrepreneur_id, context
            )
            if insight:
                insights.append(insight)

        # Filter and prioritize insights
        filtered_insights = self._filter_insights(insights, context)

        # Surface top insight (if any)
        if filtered_insights:
            await self._surface_insight(
                entrepreneur_id,
                filtered_insights[0]  # Top priority
            )

    def _filter_insights(
        self,
        insights: List[AgentResponse],
        context: BusinessContext
    ) -> List[AgentResponse]:
        """Filter insights to surface only high-impact, actionable items"""

        if not insights:
            return []

        # Filter rules (from Part 4: Proactive Intelligence Model)
        filtered = []

        for insight in insights:
            # Rule 1: Confidence threshold
            if insight.confidence < 0.7:
                continue

            # Rule 2: Check if already surfaced recently
            if self._recently_surfaced(insight, context):
                continue

            # Rule 3: Must be actionable
            if not insight.follow_up_questions:
                continue

            # Rule 4: Check urgency metadata
            urgency = insight.metadata.get("urgency", "medium")
            if urgency == "low" and len(insights) > 1:
                continue  # Skip low urgency if other insights exist

            filtered.append(insight)

        # Prioritize by urgency + confidence
        filtered.sort(
            key=lambda x: (
                {"high": 3, "medium": 2, "low": 1}.get(x.metadata.get("urgency"), 2),
                x.confidence
            ),
            reverse=True
        )

        # Limit to top 1-2 insights per check
        return filtered[:2]

    async def _surface_insight(
        self,
        entrepreneur_id: str,
        insight: AgentResponse
    ):
        """Surface insight to entrepreneur via notification"""

        # Format notification
        notification = {
            "entrepreneur_id": entrepreneur_id,
            "agent": insight.agent_name,
            "message": insight.message,
            "actions": insight.follow_up_questions,
            "timestamp": datetime.now().isoformat(),
            "urgency": insight.metadata.get("urgency", "medium")
        }

        # Send notification (desktop, email, or in-app)
        await self.notifications.send(notification)

        # Log proactive engagement
        await self.db.execute(
            """
            INSERT INTO proactive_engagements
            (entrepreneur_id, agent_name, insight, surfaced_at)
            VALUES ($1, $2, $3, NOW())
            """,
            entrepreneur_id,
            insight.agent_name,
            json.dumps(insight.__dict__)
        )

    def _is_focus_time(self, entrepreneur_id: str) -> bool:
        """Check if entrepreneur is in focus time (don't interrupt)"""

        # Get preferences
        preferences = self.context.get_preferences(entrepreneur_id)
        focus_hours = preferences.get("focus_hours", [])

        current_hour = datetime.now().hour

        return current_hour in focus_hours
```

---

### 5. File System Monitor

**Activity Detection & Domain Inference:**

```python
# services/observation/file_monitor.py

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class BusinessFileHandler(FileSystemEventHandler):
    """Monitors business files and infers activity domain"""

    def __init__(
        self,
        entrepreneur_id: str,
        context_manager: ContextStateManager,
        chief_of_staff: ChiefOfStaff
    ):
        self.entrepreneur_id = entrepreneur_id
        self.context = context_manager
        self.orchestrator = chief_of_staff

        # Domain inference patterns
        self.domain_patterns = {
            "finance": [
                r"/finances?/",
                r".*runway.*\.xlsx",
                r".*p&l.*\.xlsx",
                r".*budget.*",
                r".*unit.*economics.*"
            ],
            "product": [
                r"/code/",
                r".*\.py$",
                r".*\.js$",
                r"/features?/",
                r".*roadmap.*"
            ],
            "market": [
                r"/research/",
                r".*customer.*interview.*",
                r".*survey.*",
                r".*feedback.*"
            ],
            "strategy": [
                r".*business.*plan.*",
                r".*strategy.*",
                r".*okr.*",
                r".*goals.*"
            ]
        }

    def on_modified(self, event):
        """File was modified"""
        if event.is_directory:
            return

        asyncio.create_task(
            self.process_file_event(event.src_path, "modified")
        )

    def on_created(self, event):
        """File was created"""
        if event.is_directory:
            return

        asyncio.create_task(
            self.process_file_event(event.src_path, "created")
        )

    async def process_file_event(self, file_path: str, event_type: str):
        """Process file event and potentially trigger agent"""

        # Infer domain from file path
        domain = self.infer_domain(file_path)

        if not domain:
            return  # Not business-relevant

        # Update context
        await self.context.process_activity(
            self.entrepreneur_id,
            {
                "type": "file_activity",
                "domain": domain,
                "file_path": file_path,
                "event_type": event_type
            }
        )

        # Check if agent should proactively engage
        context = await self.context.get_context(self.entrepreneur_id)

        # Get relevant agent
        agent_name = self.domain_to_agent(domain)
        if agent_name in self.orchestrator.specialists:
            agent = self.orchestrator.specialists[agent_name]

            # Check for proactive engagement
            insight = await agent.check_proactive_triggers(
                self.entrepreneur_id,
                context
            )

            if insight:
                await self.notify_entrepreneur(insight)

    def infer_domain(self, file_path: str) -> Optional[str]:
        """Infer business domain from file path"""
        import re

        for domain, patterns in self.domain_patterns.items():
            for pattern in patterns:
                if re.search(pattern, file_path, re.IGNORECASE):
                    return domain

        return None

    def domain_to_agent(self, domain: str) -> str:
        """Map domain to agent name"""
        mapping = {
            "finance": "capital",
            "product": "product",
            "market": "market_discovery",
            "strategy": "conviction"
        }
        return mapping.get(domain, "chief_of_staff")


class FileMonitorService:
    """Manages file monitoring for an entrepreneur"""

    def __init__(self):
        self.observers = {}

    def start_monitoring(
        self,
        entrepreneur_id: str,
        watch_path: str,
        context_manager: ContextStateManager,
        orchestrator: ChiefOfStaff
    ):
        """Start monitoring a directory"""

        if entrepreneur_id in self.observers:
            self.stop_monitoring(entrepreneur_id)

        handler = BusinessFileHandler(
            entrepreneur_id,
            context_manager,
            orchestrator
        )

        observer = Observer()
        observer.schedule(handler, watch_path, recursive=True)
        observer.start()

        self.observers[entrepreneur_id] = observer

        logger.info(f"Started monitoring {watch_path} for {entrepreneur_id}")

    def stop_monitoring(self, entrepreneur_id: str):
        """Stop monitoring for an entrepreneur"""
        if entrepreneur_id in self.observers:
            self.observers[entrepreneur_id].stop()
            self.observers[entrepreneur_id].join()
            del self.observers[entrepreneur_id]
```

---

## Data Architecture

### Database Schemas

**PostgreSQL Tables:**

```sql
-- Entrepreneurs
CREATE TABLE entrepreneurs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    profile JSONB DEFAULT '{}',  -- Communication preferences, risk tolerance, etc.
    onboarded_at TIMESTAMP DEFAULT NOW(),
    status TEXT DEFAULT 'active',  -- active, paused, churned
    created_at TIMESTAMP DEFAULT NOW()
);

-- Business Context (current state)
CREATE TABLE business_context (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entrepreneur_id UUID REFERENCES entrepreneurs(id) ON DELETE CASCADE,
    phase TEXT NOT NULL,  -- foundation, strategy, development, launch
    phase_confidence FLOAT DEFAULT 0.5,
    business_type JSONB DEFAULT '{}',  -- {primary: "SaaS", subtype: "B2B"}
    cognitive_state JSONB DEFAULT '{}',  -- {initiative_name: "formation/testing/response"}
    resources JSONB DEFAULT '{}',  -- {runway: 6, team_size: 1, mrr: 350, total_sales: 187}
    strategic_convictions JSONB DEFAULT '[]',
    recent_activities JSONB DEFAULT '[]',
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(entrepreneur_id)  -- One context per entrepreneur
);

-- Decisions (historical record)
CREATE TABLE decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entrepreneur_id UUID REFERENCES entrepreneurs(id) ON DELETE CASCADE,
    decision TEXT NOT NULL,
    rationale TEXT,
    category TEXT NOT NULL,  -- strategic, tactical
    conviction_level FLOAT,  -- 0.0 to 1.0
    initiative TEXT,  -- Which initiative this decision relates to
    evidence JSONB DEFAULT '{}',  -- Supporting evidence at time of decision
    outcome JSONB,  -- What happened after (filled in later)
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_decisions_entrepreneur ON decisions(entrepreneur_id, created_at DESC);
CREATE INDEX idx_decisions_category ON decisions(entrepreneur_id, category);

-- Agent Interactions
CREATE TABLE agent_interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entrepreneur_id UUID REFERENCES entrepreneurs(id) ON DELETE CASCADE,
    agent_name TEXT NOT NULL,
    interaction_type TEXT NOT NULL,  -- proactive, on_demand, coordinated
    user_input TEXT,
    agent_response TEXT NOT NULL,
    context JSONB,  -- Business context at time of interaction
    feedback JSONB,  -- {helpful: true, rating: 4, accepted_advice: true}
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_interactions_entrepreneur ON agent_interactions(entrepreneur_id, created_at DESC);
CREATE INDEX idx_interactions_agent ON agent_interactions(agent_name, created_at DESC);

-- Proactive Engagements (tracking what we surfaced)
CREATE TABLE proactive_engagements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entrepreneur_id UUID REFERENCES entrepreneurs(id) ON DELETE CASCADE,
    agent_name TEXT NOT NULL,
    trigger TEXT NOT NULL,  -- runway_alert, burn_spike, pricing_anomaly, etc.
    insight JSONB NOT NULL,
    surfaced_at TIMESTAMP DEFAULT NOW(),
    response_status TEXT,  -- clicked, dismissed, ignored
    response_at TIMESTAMP
);

CREATE INDEX idx_proactive_entrepreneur ON proactive_engagements(entrepreneur_id, surfaced_at DESC);

-- Financial Metrics (time-series)
CREATE TABLE financial_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entrepreneur_id UUID REFERENCES entrepreneurs(id) ON DELETE CASCADE,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    revenue DECIMAL(12, 2),
    mrr DECIMAL(12, 2),
    arr DECIMAL(12, 2),
    expenses DECIMAL(12, 2),
    burn_rate DECIMAL(12, 2),
    runway_months FLOAT,
    balance DECIMAL(12, 2),
    metrics JSONB DEFAULT '{}',  -- {cac: 150, ltv: 450, churn: 0.05}
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_financial_entrepreneur_period ON financial_metrics(entrepreneur_id, period_end DESC);

-- Conviction Tracking
CREATE TABLE convictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entrepreneur_id UUID REFERENCES entrepreneurs(id) ON DELETE CASCADE,
    statement TEXT NOT NULL,
    category TEXT NOT NULL,  -- strategic, tactical
    conviction_strength FLOAT NOT NULL,  -- 0.0 to 1.0
    evidence JSONB DEFAULT '[]',  -- Array of supporting evidence
    contradictions JSONB DEFAULT '[]',  -- Array of contradicting evidence
    evolution JSONB DEFAULT '[]',  -- History of how conviction changed over time
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_convictions_entrepreneur ON convictions(entrepreneur_id, category);

-- Activity Log (file changes, app usage, etc.)
CREATE TABLE activity_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entrepreneur_id UUID REFERENCES entrepreneurs(id) ON DELETE CASCADE,
    activity_type TEXT NOT NULL,  -- file_activity, app_usage, calendar_event
    domain TEXT,  -- finance, product, market, strategy
    details JSONB NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_activity_entrepreneur_time ON activity_log(entrepreneur_id, timestamp DESC);
CREATE INDEX idx_activity_domain ON activity_log(entrepreneur_id, domain, timestamp DESC);
```

### Vector Store Schema (Qdrant)

**Collections:**

```python
# Collection for decision embeddings
decisions_collection = {
    "name": "decisions",
    "vectors": {
        "size": 1536,  # OpenAI ada-002 embedding size
        "distance": "Cosine"
    },
    "payload_schema": {
        "entrepreneur_id": "keyword",
        "decision_text": "text",
        "category": "keyword",
        "conviction_level": "float",
        "outcome": "text",
        "timestamp": "datetime"
    }
}

# Collection for interaction history
interactions_collection = {
    "name": "interactions",
    "vectors": {
        "size": 1536,
        "distance": "Cosine"
    },
    "payload_schema": {
        "entrepreneur_id": "keyword",
        "agent_name": "keyword",
        "user_input": "text",
        "agent_response": "text",
        "helpful": "bool",
        "timestamp": "datetime"
    }
}

# Collection for convictions
convictions_collection = {
    "name": "convictions",
    "vectors": {
        "size": 1536,
        "distance": "Cosine"
    },
    "payload_schema": {
        "entrepreneur_id": "keyword",
        "statement": "text",
        "category": "keyword",
        "strength": "float",
        "evidence_count": "integer",
        "timestamp": "datetime"
    }
}
```

**Embedding Strategy:**

```python
# services/memory/embeddings.py

class EmbeddingService:
    """Generate and manage embeddings for semantic search"""

    def __init__(self, vector_store_client, embedding_model="text-embedding-ada-002"):
        self.vector_store = vector_store_client
        self.model = embedding_model

    async def embed_decision(self, decision: Dict):
        """Embed a decision for later retrieval"""

        # Create rich text representation
        text = f"""
Decision: {decision['decision']}
Rationale: {decision['rationale']}
Category: {decision['category']}
Evidence: {json.dumps(decision.get('evidence', {}))}
"""

        # Generate embedding
        embedding = await self.generate_embedding(text)

        # Store in vector database
        await self.vector_store.upsert(
            collection="decisions",
            points=[{
                "id": decision['id'],
                "vector": embedding,
                "payload": {
                    "entrepreneur_id": decision['entrepreneur_id'],
                    "decision_text": decision['decision'],
                    "category": decision['category'],
                    "conviction_level": decision.get('conviction_level'),
                    "timestamp": decision['created_at']
                }
            }]
        )

    async def search_similar_decisions(
        self,
        entrepreneur_id: str,
        query: str,
        top_k: int = 5
    ) -> List[Dict]:
        """Find similar past decisions"""

        query_embedding = await self.generate_embedding(query)

        results = await self.vector_store.search(
            collection="decisions",
            query_vector=query_embedding,
            filter={
                "must": [{"key": "entrepreneur_id", "match": {"value": entrepreneur_id}}]
            },
            limit=top_k
        )

        return results
```

---

## Agent Implementation Patterns

### Prompt Engineering Strategy

**System Prompt Structure:**

```python
# services/agents/prompts.py

class PromptBuilder:
    """Builds adaptive system prompts for agents"""

    def build_agent_prompt(
        self,
        agent_config: Dict,
        context: BusinessContext,
        conversation_history: List[Dict]
    ) -> str:
        """
        Construct system prompt with:
        1. Base agent identity
        2. Phase-specific behavior
        3. Business type adaptations
        4. Cognitive state adaptations
        5. Recent context
        """

        prompt_parts = []

        # Part 1: Base Identity
        prompt_parts.append(f"""You are the {agent_config['name']}.
Nickname: "{agent_config['nickname']}"
Domain: {agent_config['domain']}
AI Impact Level: {agent_config['ai_impact_level']}

{agent_config['core_identity']}
""")

        # Part 2: Phase-Specific Behavior
        phase_behavior = agent_config['phase_behaviors'].get(
            context.phase.value,
            agent_config['phase_behaviors']['default']
        )
        prompt_parts.append(f"\nCURRENT BUSINESS PHASE: {context.phase.value.upper()}\n{phase_behavior}")

        # Part 3: Business Type Adaptations
        business_type = context.business_type.get('primary', 'Unknown')
        if business_type in agent_config.get('business_type_adaptations', {}):
            type_adaptation = agent_config['business_type_adaptations'][business_type]
            prompt_parts.append(f"\nBUSINESS TYPE: {business_type}\n{type_adaptation}")

        # Part 4: Cognitive State (if relevant)
        cognitive_state = context.cognitive_state.get(agent_config['domain'])
        if cognitive_state and cognitive_state.value in agent_config.get('cognitive_adaptations', {}):
            cognitive_adaptation = agent_config['cognitive_adaptations'][cognitive_state.value]
            prompt_parts.append(f"\nCOGNITIVE STATE: {cognitive_state.value.upper()}\n{cognitive_adaptation}")

        # Part 5: Current Context Snapshot
        context_snapshot = f"""
CURRENT BUSINESS CONTEXT:
- Phase: {context.phase.value}
- Resources: {json.dumps(context.resources, indent=2)}
- Strategic Convictions: {len(context.strategic_convictions)} active
- Recent Activities: {len(context.recent_activities)} tracked
"""
        prompt_parts.append(context_snapshot)

        # Part 6: Behavioral Guidelines
        prompt_parts.append(f"""
BEHAVIORAL GUIDELINES:
1. Explain your reasoning clearly
2. State confidence levels when appropriate
3. Acknowledge limitations honestly
4. Defer to entrepreneur for final decisions
5. Adapt communication style to entrepreneur preferences
6. Surface insights proactively when high-impact
7. Be concise by default, expand when asked
8. Reference relevant frameworks when helpful (but don't overwhelm)
""")

        return "\n".join(prompt_parts)
```

**Agent Configuration Example (Capital Agent):**

```python
# config/agents/capital_agent.yaml

capital_agent:
  name: "Capital & Financing Agent"
  nickname: "The CFO"
  domain: "finance"
  ai_impact_level: "HIGH"

  core_identity: |
    You are an expert in financial modeling, unit economics, runway management,
    and fundraising strategy. You provide data-driven financial guidance to
    entrepreneurs, helping them make informed capital allocation decisions.

  phase_behaviors:
    foundation: |
      FOUNDATION PHASE:
      - You are in TEACHING MODE - explain financial concepts clearly
      - Focus on: Unit economics, break-even analysis, pricing validation
      - Be encouraging - losses are normal while learning
      - Distinguish sweat equity from actual costs
      - Build basic financial tracking habits

    strategy: |
      STRATEGY PHASE:
      - Focus on: Path to profitability, channel economics, margin optimization
      - Provide strategic financial insights
      - Help with growth planning and resource allocation
      - Introduce cohort analysis, CAC:LTV ratios

    development: |
      DEVELOPMENT PHASE:
      - Focus on: Burn rate, runway, fundraising urgency
      - Monitor: Burn multiple (burn ÷ net new MRR)
      - Alert: Cash crises proactively
      - Scenario modeling: Cut burn vs raise capital vs accelerate revenue

    launch: |
      LAUNCH PHASE:
      - Focus on: Scaling economics, capital efficiency
      - Advanced metrics: Gross margin %, rule of 40, burn multiple
      - Support: Fundraising strategy, financial forecasting

  business_type_adaptations:
    "Physical Product": |
      - Emphasize: COGS, inventory, production costs
      - Track: Unit economics (cost/unit, margin/unit)
      - Consider: Bulk purchasing, production efficiency, shipping
      - Metrics: Gross margin %, contribution margin

    "SaaS": |
      - Emphasize: MRR, ARR, churn rate, CAC, LTV
      - Track: Burn multiple, months to payback CAC
      - Consider: Pricing models (seat-based vs usage-based)
      - Metrics: Rule of 40, net dollar retention

  cognitive_adaptations:
    response: |
      RESPONSE MODE DETECTED:
      Entrepreneur is making a financial decision based on test results.
      - Help interpret data objectively
      - Present options with clear trade-offs
      - Support decision-making, don't decide for them
      - Prevent analysis paralysis

  proactive_triggers:
    - type: "runway_alert"
      condition: "runway_months < 3"
      priority: "high"

    - type: "burn_spike"
      condition: "burn_increase_pct > 0.15"
      priority: "high"

    - type: "negative_margin"
      condition: "selling_below_cost == true"
      priority: "medium"
```

---

## Integration Architecture

### External Tool Integration Strategy

**OAuth 2.0 Integration Pattern:**

```python
# services/integrations/oauth_manager.py

class OAuthIntegrationManager:
    """Manages OAuth connections to external tools"""

    def __init__(self, db_client, encryption_service):
        self.db = db_client
        self.encryption = encryption_service

        # Supported integrations
        self.providers = {
            "stripe": StripeIntegration(),
            "quickbooks": QuickBooksIntegration(),
            "github": GitHubIntegration(),
            "google": GoogleIntegration(),  # Calendar, Gmail
            "slack": SlackIntegration()
        }

    async def authorize(self, entrepreneur_id: str, provider: str, scopes: List[str]):
        """Initiate OAuth flow"""

        integration = self.providers.get(provider)
        if not integration:
            raise ValueError(f"Unsupported provider: {provider}")

        # Generate authorization URL
        auth_url, state = integration.get_authorization_url(scopes)

        # Store state for CSRF protection
        await self.db.execute(
            """
            INSERT INTO oauth_states (entrepreneur_id, provider, state, scopes, created_at)
            VALUES ($1, $2, $3, $4, NOW())
            """,
            entrepreneur_id, provider, state, json.dumps(scopes)
        )

        return auth_url

    async def handle_callback(self, state: str, code: str):
        """Handle OAuth callback"""

        # Verify state
        oauth_state = await self.db.fetch_one(
            "SELECT * FROM oauth_states WHERE state = $1",
            state
        )

        if not oauth_state:
            raise ValueError("Invalid OAuth state")

        provider_name = oauth_state["provider"]
        integration = self.providers[provider_name]

        # Exchange code for tokens
        tokens = await integration.exchange_code(code)

        # Encrypt and store tokens
        encrypted_access_token = self.encryption.encrypt(tokens["access_token"])
        encrypted_refresh_token = self.encryption.encrypt(tokens.get("refresh_token", ""))

        await self.db.execute(
            """
            INSERT INTO integrations (entrepreneur_id, provider, access_token, refresh_token, scopes, expires_at)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (entrepreneur_id, provider)
            DO UPDATE SET access_token = $3, refresh_token = $4, expires_at = $6, updated_at = NOW()
            """,
            oauth_state["entrepreneur_id"],
            provider_name,
            encrypted_access_token,
            encrypted_refresh_token,
            oauth_state["scopes"],
            datetime.now() + timedelta(seconds=tokens.get("expires_in", 3600))
        )

        return oauth_state["entrepreneur_id"]

    async def get_client(self, entrepreneur_id: str, provider: str):
        """Get authenticated client for provider"""

        integration_record = await self.db.fetch_one(
            """
            SELECT * FROM integrations
            WHERE entrepreneur_id = $1 AND provider = $2
            """,
            entrepreneur_id, provider
        )

        if not integration_record:
            raise ValueError(f"No {provider} integration found for entrepreneur")

        # Decrypt tokens
        access_token = self.encryption.decrypt(integration_record["access_token"])

        # Check if token expired
        if datetime.now() >= integration_record["expires_at"]:
            access_token = await self._refresh_token(entrepreneur_id, provider, integration_record)

        # Return authenticated client
        integration = self.providers[provider]
        return integration.get_client(access_token)
```

**Integration-Specific Implementations:**

```python
# services/integrations/stripe_integration.py

class StripeIntegration:
    """Stripe API integration for financial data"""

    def __init__(self):
        self.client_id = os.getenv("STRIPE_CLIENT_ID")
        self.client_secret = os.getenv("STRIPE_CLIENT_SECRET")

    def get_authorization_url(self, scopes: List[str]):
        import stripe
        state = secrets.token_urlsafe(32)

        auth_url = f"https://connect.stripe.com/oauth/authorize?" + urlencode({
            "response_type": "code",
            "client_id": self.client_id,
            "scope": " ".join(scopes or ["read_only"]),
            "state": state
        })

        return auth_url, state

    async def exchange_code(self, code: str):
        import stripe
        stripe.api_key = self.client_secret

        response = stripe.OAuth.token(
            grant_type='authorization_code',
            code=code
        )

        return {
            "access_token": response["access_token"],
            "refresh_token": response.get("refresh_token"),
            "stripe_user_id": response["stripe_user_id"],
            "expires_in": 86400  # 24 hours
        }

    def get_client(self, access_token: str):
        import stripe
        return stripe.StripeClient(api_key=access_token)

    async def fetch_financial_data(self, client, period_start: datetime, period_end: datetime):
        """Fetch revenue, charges, refunds for period"""

        # Fetch charges
        charges = client.charges.list(
            created={
                "gte": int(period_start.timestamp()),
                "lte": int(period_end.timestamp())
            },
            limit=100
        )

        revenue = sum(charge.amount for charge in charges.data if charge.paid) / 100  # Convert cents

        # Fetch refunds
        refunds = client.refunds.list(
            created={
                "gte": int(period_start.timestamp()),
                "lte": int(period_end.timestamp())
            },
            limit=100
        )

        refund_total = sum(refund.amount for refund in refunds.data) / 100

        return {
            "revenue": revenue,
            "refunds": refund_total,
            "net_revenue": revenue - refund_total,
            "transaction_count": len(charges.data)
        }
```

**Data Sync Strategy:**

```python
# services/integrations/sync_engine.py

class IntegrationSyncEngine:
    """Syncs data from external integrations"""

    def __init__(self, oauth_manager: OAuthIntegrationManager, db_client):
        self.oauth = oauth_manager
        self.db = db_client

        # Sync schedules
        self.sync_intervals = {
            "stripe": 3600,  # 1 hour
            "quickbooks": 21600,  # 6 hours
            "github": 1800,  # 30 minutes
            "google_calendar": 600  # 10 minutes
        }

    async def start_sync_loops(self):
        """Start background sync loops for all integrations"""

        tasks = []
        for provider, interval in self.sync_intervals.items():
            tasks.append(self.sync_loop(provider, interval))

        await asyncio.gather(*tasks)

    async def sync_loop(self, provider: str, interval: int):
        """Background loop for syncing a provider"""

        while True:
            try:
                # Get all entrepreneurs with this integration
                entrepreneurs = await self.db.fetch_all(
                    """
                    SELECT entrepreneur_id FROM integrations
                    WHERE provider = $1 AND status = 'active'
                    """,
                    provider
                )

                # Sync each in parallel
                await asyncio.gather(*[
                    self.sync_entrepreneur(ent["entrepreneur_id"], provider)
                    for ent in entrepreneurs
                ])

            except Exception as e:
                logger.error(f"Sync error for {provider}: {e}")

            await asyncio.sleep(interval)

    async def sync_entrepreneur(self, entrepreneur_id: str, provider: str):
        """Sync data for one entrepreneur from one provider"""

        try:
            if provider == "stripe":
                await self.sync_stripe(entrepreneur_id)
            elif provider == "quickbooks":
                await self.sync_quickbooks(entrepreneur_id)
            elif provider == "github":
                await self.sync_github(entrepreneur_id)

        except Exception as e:
            logger.error(f"Sync error for {entrepreneur_id} / {provider}: {e}")

    async def sync_stripe(self, entrepreneur_id: str):
        """Sync Stripe financial data"""

        client = await self.oauth.get_client(entrepreneur_id, "stripe")

        # Fetch last 30 days of data
        period_end = datetime.now()
        period_start = period_end - timedelta(days=30)

        financial_data = await StripeIntegration().fetch_financial_data(
            client, period_start, period_end
        )

        # Update financial metrics
        await self.db.execute(
            """
            INSERT INTO financial_metrics
            (entrepreneur_id, period_start, period_end, revenue, metrics, created_at)
            VALUES ($1, $2, $3, $4, $5, NOW())
            ON CONFLICT (entrepreneur_id, period_end)
            DO UPDATE SET revenue = $4, metrics = $5, updated_at = NOW()
            """,
            entrepreneur_id,
            period_start,
            period_end,
            financial_data["net_revenue"],
            json.dumps(financial_data)
        )

        # Update business context
        await self.update_context_from_financial_data(entrepreneur_id, financial_data)
```

---

## Deployment & Operations

### Docker Deployment

**Production docker-compose.yml:**

```yaml
version: '3.8'

services:
  # API Gateway
  api:
    build:
      context: ./services/api
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://agent_user:${DB_PASSWORD}@postgres:5432/agent_framework
      - REDIS_URL=redis://redis:6379
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - QDRANT_URL=http://qdrant:6333
      - ENV=production
    depends_on:
      - postgres
      - redis
      - qdrant
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Orchestrator Service (Chief of Staff)
  orchestrator:
    build:
      context: ./services/orchestrator
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://agent_user:${DB_PASSWORD}@postgres:5432/agent_framework
      - REDIS_URL=redis://redis:6379
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  # Proactive Engine (Background monitoring)
  proactive_engine:
    build:
      context: ./services/proactive_engine
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://agent_user:${DB_PASSWORD}@postgres:5432/agent_framework
      - REDIS_URL=redis://redis:6379
      - QDRANT_URL=http://qdrant:6333
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  # File Monitor Service
  file_monitor:
    build:
      context: ./services/file_monitor
      dockerfile: Dockerfile
    volumes:
      - ${ENTREPRENEUR_WORKSPACE}:/workspace:ro  # Read-only access
    environment:
      - DATABASE_URL=postgresql://agent_user:${DB_PASSWORD}@postgres:5432/agent_framework
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  # Integration Sync Engine
  integration_sync:
    build:
      context: ./services/integrations
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://agent_user:${DB_PASSWORD}@postgres:5432/agent_framework
      - REDIS_URL=redis://redis:6379
      - STRIPE_CLIENT_ID=${STRIPE_CLIENT_ID}
      - STRIPE_CLIENT_SECRET=${STRIPE_CLIENT_SECRET}
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  # Celery Worker (async tasks)
  celery_worker:
    build:
      context: ./services/workers
      dockerfile: Dockerfile
    command: celery -A tasks worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://agent_user:${DB_PASSWORD}@postgres:5432/agent_framework
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  # PostgreSQL
  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    environment:
      - POSTGRES_DB=agent_framework
      - POSTGRES_USER=agent_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    ports:
      - "5432:5432"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U agent_user -d agent_framework"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Qdrant (Vector Database)
  qdrant:
    image: qdrant/qdrant:latest
    volumes:
      - qdrant_data:/qdrant/storage
    ports:
      - "6333:6333"
    restart: unless-stopped

  # Nginx (Reverse Proxy)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  qdrant_data:
```

**Dockerfile Example (API Service):**

```dockerfile
# services/api/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### CI/CD Pipeline

**GitHub Actions Workflow:**

```yaml
# .github/workflows/deploy.yml

name: Deploy Agent Framework

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: agent_framework_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run linters
        run: |
          black --check .
          flake8 .
          mypy .

      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:test_password@localhost:5432/agent_framework_test
          REDIS_URL: redis://localhost:6379
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY_TEST }}
        run: |
          pytest tests/ --cov=services --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push images
        run: |
          docker-compose -f docker-compose.prod.yml build
          docker-compose -f docker-compose.prod.yml push

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to production
        env:
          SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
          DEPLOY_HOST: ${{ secrets.DEPLOY_HOST }}
        run: |
          echo "$SSH_PRIVATE_KEY" > deploy_key
          chmod 600 deploy_key
          ssh -i deploy_key -o StrictHostKeyChecking=no deploy@$DEPLOY_HOST << 'EOF'
            cd /opt/agent_framework
            git pull origin main
            docker-compose -f docker-compose.prod.yml pull
            docker-compose -f docker-compose.prod.yml up -d
            docker-compose -f docker-compose.prod.yml exec -T api python manage.py migrate
          EOF
```

### Monitoring & Observability

**Prometheus + Grafana Stack:**

```yaml
# monitoring/docker-compose.monitoring.yml

version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana:latest
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - loki_data:/loki

  promtail:
    image: grafana/promtail:latest
    volumes:
      - /var/log:/var/log:ro
      - ./promtail-config.yml:/etc/promtail/config.yml
    command: -config.file=/etc/promtail/config.yml

volumes:
  prometheus_data:
  grafana_data:
  loki_data:
```

**Application Metrics:**

```python
# services/common/metrics.py

from prometheus_client import Counter, Histogram, Gauge
import time

# Agent interaction metrics
agent_requests = Counter(
    'agent_requests_total',
    'Total agent requests',
    ['agent_name', 'entrepreneur_id']
)

agent_response_time = Histogram(
    'agent_response_seconds',
    'Agent response time',
    ['agent_name']
)

proactive_insights_surfaced = Counter(
    'proactive_insights_total',
    'Total proactive insights surfaced',
    ['agent_name', 'trigger_type']
)

# LLM metrics
llm_requests = Counter(
    'llm_requests_total',
    'Total LLM API requests',
    ['provider', 'model']
)

llm_tokens_used = Counter(
    'llm_tokens_total',
    'Total LLM tokens used',
    ['provider', 'type']  # type: prompt or completion
)

llm_cost = Counter(
    'llm_cost_usd',
    'Total LLM cost in USD',
    ['provider']
)

# Context detection metrics
phase_detections = Counter(
    'phase_detections_total',
    'Phase detection runs',
    ['detected_phase']
)

phase_transitions = Counter(
    'phase_transitions_total',
    'Phase transitions',
    ['from_phase', 'to_phase']
)

# System health
active_entrepreneurs = Gauge(
    'active_entrepreneurs',
    'Number of active entrepreneurs'
)


class MetricsMiddleware:
    """Middleware to collect metrics"""

    async def track_agent_request(self, agent_name: str, entrepreneur_id: str):
        agent_requests.labels(
            agent_name=agent_name,
            entrepreneur_id=entrepreneur_id
        ).inc()

        start_time = time.time()

        try:
            yield
        finally:
            duration = time.time() - start_time
            agent_response_time.labels(agent_name=agent_name).observe(duration)

    async def track_llm_request(self, provider: str, model: str, response: Dict):
        llm_requests.labels(provider=provider, model=model).inc()

        usage = response.get("usage", {})
        llm_tokens_used.labels(provider=provider, type="prompt").inc(usage.get("prompt_tokens", 0))
        llm_tokens_used.labels(provider=provider, type="completion").inc(usage.get("completion_tokens", 0))

        # Calculate cost (example rates)
        cost = self.calculate_cost(provider, model, usage)
        llm_cost.labels(provider=provider).inc(cost)
```

---

## Security & Privacy

### Security Architecture

**Encryption at Rest:**

```python
# services/security/encryption.py

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64
import os

class EncryptionService:
    """Handles encryption for sensitive data"""

    def __init__(self):
        # Master key from environment (rotated regularly)
        self.master_key = os.getenv("ENCRYPTION_MASTER_KEY").encode()

        # Derive encryption key
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"agent_framework_salt",  # Unique per deployment
            iterations=100000
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_key))
        self.cipher = Fernet(key)

    def encrypt(self, plaintext: str) -> str:
        """Encrypt sensitive data"""
        encrypted = self.cipher.encrypt(plaintext.encode())
        return base64.urlsafe_b64encode(encrypted).decode()

    def decrypt(self, ciphertext: str) -> str:
        """Decrypt sensitive data"""
        encrypted = base64.urlsafe_b64decode(ciphertext.encode())
        decrypted = self.cipher.decrypt(encrypted)
        return decrypted.decode()
```

**Permission System:**

```python
# services/security/permissions.py

class PermissionManager:
    """Manages entrepreneur permissions for file/app access"""

    async def request_permission(
        self,
        entrepreneur_id: str,
        permission_type: str,
        resource: str
    ) -> bool:
        """Request permission from entrepreneur"""

        # Check if already granted
        existing = await self.db.fetch_one(
            """
            SELECT * FROM permissions
            WHERE entrepreneur_id = $1 AND type = $2 AND resource = $3
            """,
            entrepreneur_id, permission_type, resource
        )

        if existing and existing["status"] == "granted":
            return True

        # Create permission request
        await self.db.execute(
            """
            INSERT INTO permission_requests
            (entrepreneur_id, type, resource, requested_at, status)
            VALUES ($1, $2, $3, NOW(), 'pending')
            """,
            entrepreneur_id, permission_type, resource
        )

        # Notify entrepreneur (email, in-app notification)
        await self.notify_permission_request(entrepreneur_id, permission_type, resource)

        return False

    async def grant_permission(
        self,
        request_id: str,
        granted: bool,
        scope: Dict = None
    ):
        """Entrepreneur grants or denies permission"""

        request = await self.db.fetch_one(
            "SELECT * FROM permission_requests WHERE id = $1",
            request_id
        )

        if granted:
            await self.db.execute(
                """
                INSERT INTO permissions (entrepreneur_id, type, resource, scope, granted_at)
                VALUES ($1, $2, $3, $4, NOW())
                """,
                request["entrepreneur_id"],
                request["type"],
                request["resource"],
                json.dumps(scope or {})
            )

        await self.db.execute(
            """
            UPDATE permission_requests
            SET status = $1, resolved_at = NOW()
            WHERE id = $2
            """,
            "granted" if granted else "denied",
            request_id
        )

    async def check_permission(
        self,
        entrepreneur_id: str,
        permission_type: str,
        resource: str
    ) -> bool:
        """Check if permission is granted"""

        permission = await self.db.fetch_one(
            """
            SELECT * FROM permissions
            WHERE entrepreneur_id = $1 AND type = $2 AND (resource = $3 OR resource = '*')
            """,
            entrepreneur_id, permission_type, resource
        )

        return permission is not None
```

**Data Privacy Compliance:**

```python
# services/security/privacy.py

class PrivacyManager:
    """Ensures GDPR, CCPA compliance"""

    async def export_user_data(self, entrepreneur_id: str) -> Dict:
        """Export all user data (GDPR right to access)"""

        data = {
            "profile": await self.db.fetch_one(
                "SELECT * FROM entrepreneurs WHERE id = $1",
                entrepreneur_id
            ),
            "context": await self.db.fetch_one(
                "SELECT * FROM business_context WHERE entrepreneur_id = $1",
                entrepreneur_id
            ),
            "decisions": await self.db.fetch_all(
                "SELECT * FROM decisions WHERE entrepreneur_id = $1",
                entrepreneur_id
            ),
            "interactions": await self.db.fetch_all(
                "SELECT * FROM agent_interactions WHERE entrepreneur_id = $1 ORDER BY created_at DESC",
                entrepreneur_id
            ),
            "integrations": await self.db.fetch_all(
                "SELECT provider, scopes, created_at FROM integrations WHERE entrepreneur_id = $1",
                entrepreneur_id
            )
        }

        # Remove encrypted tokens from export
        for integration in data["integrations"]:
            integration.pop("access_token", None)
            integration.pop("refresh_token", None)

        return data

    async def delete_user_data(self, entrepreneur_id: str):
        """Delete all user data (GDPR right to erasure)"""

        # Log deletion request (for audit)
        await self.db.execute(
            """
            INSERT INTO deletion_log (entrepreneur_id, requested_at)
            VALUES ($1, NOW())
            """,
            entrepreneur_id
        )

        # Delete from all tables (cascading)
        await self.db.execute(
            "DELETE FROM entrepreneurs WHERE id = $1",
            entrepreneur_id
        )

        # Delete vector embeddings
        await self.vector_store.delete_all(
            filter={"entrepreneur_id": entrepreneur_id}
        )

        # Revoke OAuth integrations
        integrations = await self.db.fetch_all(
            "SELECT * FROM integrations WHERE entrepreneur_id = $1",
            entrepreneur_id
        )

        for integration in integrations:
            await self.revoke_integration(integration)
```

---

## Development Roadmap

### Phase 1: MVP Core (Weeks 1-6)

**Goal:** Minimal working system with 5 agents, basic orchestration

**Week 1-2: Infrastructure**
- [x] Set up development environment (Docker, PostgreSQL, Redis)
- [x] Create database schemas
- [x] Build Context State Manager
- [x] Implement basic LLM integration (Claude API)

**Week 3-4: Core Agents**
- [x] Build Base Agent class
- [x] Implement Chief of Staff (orchestrator)
- [x] Implement 3 specialist agents:
  - Market Discovery Agent
  - Product & Technology Agent
  - Capital & Financing Agent
- [x] Basic prompt engineering + phase adaptation

**Week 5-6: Interface + Testing**
- [x] Build CLI interface for conversation
- [x] Implement basic conversation memory
- [x] Write integration tests
- [x] Deploy to staging environment

**Success Criteria:**
- ✅ Entrepreneur can chat with agents via CLI
- ✅ Agents adapt responses to business phase
- ✅ Context persists across conversations
- ✅ All 5 agents respond appropriately to domain-specific questions

---

### Phase 2: Proactive Intelligence (Weeks 7-10)

**Goal:** Background monitoring + proactive insights

**Week 7-8: Monitoring**
- [ ] Implement file system monitoring (watchdog)
- [ ] Build domain inference logic
- [ ] Create Proactive Intelligence Engine
- [ ] Develop insight filtering system

**Week 9-10: Proactive Triggers**
- [ ] Implement agent-specific proactive checks:
  - Capital: Runway alerts, burn spikes
  - Market: Pattern detection in customer feedback
  - Product: Code quality issues, technical debt
- [ ] Build notification system (desktop notifications)
- [ ] Create proactive engagement logging

**Success Criteria:**
- ✅ System detects file changes in entrepreneur's workspace
- ✅ Agents proactively surface 2-3 high-impact insights per week
- ✅ <5% false positive rate (insights entrepreneur dismisses)
- ✅ Entrepreneur can configure focus hours (no interruptions)

---

### Phase 3: Memory & Learning (Weeks 11-14)

**Goal:** Long-term memory, preference learning, improved responses

**Week 11-12: Memory Systems**
- [ ] Set up vector database (Qdrant)
- [ ] Implement embedding service
- [ ] Build semantic search over decisions and interactions
- [ ] Create memory retrieval for agents

**Week 13-14: Learning & Adaptation**
- [ ] Implement preference learning
  - Track accepted/rejected advice
  - Adapt communication style
  - Learn domain preferences
- [ ] Build outcome tracking
  - Link decisions to results
  - Update conviction strength based on evidence
- [ ] Create feedback loops
  - Entrepreneur ratings on interactions
  - Agent confidence calibration

**Success Criteria:**
- ✅ Agents reference relevant past decisions in responses
- ✅ Communication style adapts to entrepreneur preferences
- ✅ Agent recommendations improve accuracy over time (measured by acceptance rate)
- ✅ System suggests similar past situations when entrepreneur faces new decisions

---

### Phase 4: Integrations (Weeks 15-18)

**Goal:** External tool integrations for richer context

**Week 15-16: Financial Integrations**
- [ ] Build OAuth integration framework
- [ ] Implement Stripe integration
  - Revenue sync
  - Transaction data
  - Refunds tracking
- [ ] Implement QuickBooks integration
  - P&L sync
  - Expense categorization
- [ ] Build financial data sync engine

**Week 17-18: Product & Communication Integrations**
- [ ] GitHub integration
  - Commit activity
  - Pull request patterns
  - Issue tracking
- [ ] Google Calendar integration
  - Meeting patterns
  - Availability detection
- [ ] Slack/Email integration (optional)
  - Communication volume
  - Team collaboration patterns

**Success Criteria:**
- ✅ Financial data syncs automatically from Stripe/QuickBooks
- ✅ Capital Agent has real-time revenue/expense data
- ✅ Product Agent aware of code activity from GitHub
- ✅ System respects meeting schedules (doesn't interrupt during calls)

---

### Phase 5: Advanced Features (Weeks 19-24)

**Goal:** Remaining agents + advanced systems

**Week 19-21: Additional Agents**
- [ ] Build 2 remaining MVP agents:
  - Strategic Conviction Keeper
  - Methodology Coach
- [ ] Implement Conviction Tracking System
- [ ] Build Framework Integration Engine

**Week 22-24: Advanced Coordination**
- [ ] Implement Cross-Domain Impact Analysis
- [ ] Build Execution Sequencer
- [ ] Create multi-agent conflict resolution
- [ ] Improve orchestration logic

**Success Criteria:**
- ✅ All 7 MVP agents functional
- ✅ Conviction tracker maintains strategic vs tactical separation
- ✅ System detects when multiple domains affected by one decision
- ✅ Agents coordinate recommendations without contradictions

---

### Phase 6: Scale & Polish (Weeks 25-30)

**Goal:** Production-ready, multi-entrepreneur support

**Week 25-26: Web Interface**
- [ ] Build React web dashboard
- [ ] Create conversation UI (chat interface)
- [ ] Build context visualization
- [ ] Implement notification management

**Week 27-28: Performance & Scale**
- [ ] Optimize database queries
- [ ] Implement caching strategies
- [ ] Load testing (100+ entrepreneurs)
- [ ] Cost optimization (LLM usage)

**Week 29-30: Production Hardening**
- [ ] Security audit
- [ ] Compliance review (GDPR, CCPA)
- [ ] Monitoring & alerting setup
- [ ] Documentation completion
- [ ] Beta testing with 10 entrepreneurs

**Success Criteria:**
- ✅ Web dashboard functional and polished
- ✅ System supports 100+ concurrent entrepreneurs
- ✅ Response time <2 seconds for agent queries
- ✅ LLM cost <$50/entrepreneur/month
- ✅ Security audit passed with no critical issues

---

## Alternative Approaches

### Framework Comparison

**Option A: AutoGen (Microsoft)**

**Pros:**
- Mature multi-agent orchestration
- Built-in conversation patterns
- Group chat support
- Good documentation

**Cons:**
- Opinionated architecture (hard to customize)
- Designed for coding agents, not business agents
- Limited built-in memory systems
- Requires significant adaptation for our use case

**Verdict:** ❌ Not recommended - too opinionated, doesn't match our architecture

---

**Option B: LangChain + LangGraph**

**Pros:**
- Flexible component library
- Strong LLM abstraction layer
- Good memory management tools
- Active community

**Cons:**
- Can be overengineered
- Steep learning curve
- Frequent breaking changes
- Performance concerns at scale

**Verdict:** ⚠️ Use selectively - adopt components (memory, LLM interface), build custom orchestration

---

**Option C: CrewAI**

**Pros:**
- Simple multi-agent setup
- Good for prototyping
- Easy to understand

**Cons:**
- Young project (immature)
- Limited features
- Not production-ready
- Small community

**Verdict:** ❌ Not recommended for production

---

**Option D: Custom-Built (Recommended)**

**Pros:**
- Full control over architecture
- Optimized for our specific use case
- No framework lock-in
- Can evolve as needs change

**Cons:**
- More upfront development work
- Need to build common patterns ourselves

**Verdict:** ✅ Recommended - Build custom orchestration, use LangChain components for utilities

---

### Build vs Buy Decisions

**LLM Provider:**
- **Build:** Self-hosted open-source models (Llama, Mixtral)
- **Buy:** Claude API, GPT-4 API
- **Decision:** Start with Claude API (faster development), add local models later for privacy/cost

**Vector Database:**
- **Build:** Custom embedding + PostgreSQL pgvector
- **Buy:** Qdrant, Pinecone, Weaviate
- **Decision:** Use Qdrant (open-source, self-hosted, production-ready)

**Monitoring:**
- **Build:** Custom metrics + logging
- **Buy:** Datadog, New Relic
- **Decision:** Prometheus + Grafana (open-source, self-hosted, cost-effective)

**Authentication:**
- **Build:** Custom OAuth implementation
- **Buy:** Auth0, Clerk
- **Decision:** Custom OAuth (simple use case, full control, no per-user costs)

---

## Implementation Priorities

### Must-Have for MVP (Phase 1-2):
1. ✅ Context State Manager with phase detection
2. ✅ Chief of Staff orchestrator
3. ✅ 5 core specialist agents
4. ✅ Basic prompt engineering + adaptation
5. ✅ CLI interface for conversation
6. ✅ File system monitoring
7. ✅ Proactive intelligence engine

### Nice-to-Have (Phase 3-4):
1. Vector database for semantic memory
2. Integration with Stripe/QuickBooks
3. Preference learning
4. GitHub integration
5. Web dashboard

### Future Enhancements (Phase 5+):
1. Remaining 15+ agents
2. Advanced multi-agent coordination
3. Community learning (patterns across entrepreneurs)
4. Mobile app
5. Voice interface

---

## Cost Estimates

**Development Costs (6-month MVP):**
- Solo developer: $60K-90K (salary/contract)
- 2-3 person team: $150K-250K
- Infrastructure (AWS/GCP): $500-1000/month during development

**Operational Costs (Per Entrepreneur/Month):**
- LLM API (Claude): $30-50
- Infrastructure (hosting): $5-10
- Vector DB: $5
- **Total:** $40-65/entrepreneur/month

**At Scale (100 entrepreneurs):**
- LLM costs: $3,000-5,000/month
- Infrastructure: $500-1,000/month
- **Total:** ~$4,000-6,000/month

**Break-even:** ~$50-60/entrepreneur/month pricing

---

## Success Metrics

**Technical Metrics:**
- Agent response time: <2 seconds (p95)
- System uptime: >99.5%
- Proactive insight acceptance rate: >60%
- False positive rate: <10%

**Business Metrics:**
- Entrepreneur satisfaction: >8/10
- Weekly active usage: >5 interactions/week
- Retention: >80% after 3 months
- NPS: >40

---

**Related Documentation:**
- [Part 1: Executive Overview](./part-1-executive-overview.md) - System vision
- [Part 2: Foundational Concepts](./part-2-foundational-concepts.md) - Business phases, cognitive loops
- [Part 3: Agent Architecture Index](./part-3-agent-architecture.md) - All 26 agents
- [Part 4: Behavioral Models & Tools](./part-4-behavioral-models-tools.md) - Universal behaviors
- [Part 5: Operational Systems](./part-5-operational-systems.md) - Strategic Conviction Tracker, Phase Detection
- [Part 6: Universal Agent Adaptation](./part-6-universal-agent-adaptation.md) - Cross-industry examples
- [v2 README](./README.md) - Implementation guide

**Back to:** [v2 Documentation Index](./README.md)
