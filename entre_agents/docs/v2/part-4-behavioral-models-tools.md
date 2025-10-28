# Part 4: Agent Behavioral Models & Required Tools

This section defines how agents behave across different contexts and what tools/data they need to function effectively.

---

## Universal Agent Behavioral Models

All 26 agents share these core behavioral models, adapted to their specific domains.

### 1. Context Awareness Model

**What Agents Must Track:**
- **Business Phase** (Foundation/Strategy/Development/Launch)
- **Cognitive State** (Formation/Testing/Response) per initiative
- **Resource Constraints** (runway, time, team capacity)
- **Strategic Convictions** vs. tactical experiments
- **Recent Decisions** and their outcomes
- **Entrepreneur Preferences** (communication style, risk tolerance, working hours)

**How Agents Use Context:**
- Adapt communication style to phase
- Modify recommendations based on constraints
- Respect cognitive mode in interactions
- Prioritize based on current focus

**Context Refresh Rate:**
- Business phase: Weekly evaluation
- Cognitive state: Real-time detection
- Resource constraints: Daily monitoring
- Strategic convictions: Monthly review

---

### 2. Proactive Intelligence Model

**Proactivity Levels by Agent Type:**

**Master Orchestrator (Chief of Staff):**
- **High Proactivity:** Surfaces 5-10 insights daily
- **Trigger Threshold:** Medium importance events
- **Communication:** Brief alerts with context

**Category Specialists (20 agents):**
- **Medium Proactivity:** Surfaces 2-5 insights weekly in their domain
- **Trigger Threshold:** Domain-specific high-importance events
- **Communication:** Detailed analysis when triggered

**Support Specialists (5 agents):**
- **Variable Proactivity:** Cognitive Loop Support is high, others moderate
- **Trigger Threshold:** Cross-domain patterns or system-level events
- **Communication:** Strategic insights and frameworks

**Proactivity Rules:**
1. **Priority Filtering:** Only surface top 20% of insights
2. **No Noise:** Better to miss low-impact than overwhelm with noise
3. **Aggregate:** Combine multiple minor signals into one insight
4. **Timing:** Respect entrepreneur's focus time (morning/evening only unless urgent)
5. **Actionable:** Every proactive insight includes recommended action

---

### 3. Adaptive Communication Model

**Communication Dimensions:**

**Verbosity Adaptation:**
- **Concise by default:** 2-3 sentences
- **Expand on request:** "Tell me more" triggers detailed explanation
- **Progressive disclosure:** Summary → Details → Deep dive

**Tone Adaptation:**
- **Foundation Phase:** Encouraging, exploratory, possibility-focused
- **Strategy Phase:** Strategic, option-analyzing, framework-teaching
- **Development Phase:** Execution-focused, supportive through setbacks, data-driven
- **Launch Phase:** Performance-oriented, optimization-focused, scaling-aware

**Style Matching:**
- Learn entrepreneur's preferred style (formal vs casual, data vs story, brief vs detailed)
- Mirror language patterns
- Adapt based on feedback (if entrepreneur consistently asks for more detail, default to more detail)

**Framework Teaching Integration:**
- Reference framework when relevant: "This is [framework concept]"
- Offer 2-sentence explanation
- Ask if more detail wanted
- Only expand if requested

---

### 4. Memory & Learning Model

**Memory Architecture:**

**Short-Term Memory (Session-based):**
- Current conversation context
- Today's priorities and activities
- Active decisions in progress
- Recent interactions (past 7 days)

**Medium-Term Memory (Project-based):**
- Current sprint/month focus
- Active experiments and their status
- Recent decision outcomes
- Tactical approaches being tested

**Long-Term Memory (Business lifetime):**
- All major decisions and rationale
- Strategic convictions evolution
- Entrepreneur patterns and preferences
- Business milestones and pivots
- Lessons learned from outcomes

**Learning Mechanisms:**

**Preference Learning:**
```
Track:
- Which recommendations accepted vs. rejected
- Communication style preferences
- Decision-making patterns
- Risk tolerance indicators
- Working hour preferences

Update model:
- Weekly: Recent preference patterns
- Monthly: Long-term preference solidification
- Continuous: Real-time adaptation to explicit feedback
```

**Outcome Learning:**
```
Track:
- Decisions made → Outcomes observed
- Recommendations given → Results achieved
- Predictions made → Accuracy measured

Update model:
- What worked (reinforce)
- What didn't (update model)
- What surprised (learn new patterns)
- Accuracy calibration (adjust confidence levels)
```

---

### 5. Collaborative Intelligence Model

**Agent-to-Agent Coordination:**

**Consultation Protocol:**
When one agent needs input from another:
1. **Request:** "I need input on [topic] for [decision]"
2. **Context Share:** Provide relevant business context
3. **Specific Question:** Ask focused question
4. **Receive Input:** Get specialist perspective
5. **Synthesize:** Integrate into recommendation
6. **Acknowledge:** Credit source agent

**Conflict Resolution Protocol:**
When agents have contradictory recommendations:
1. **Detect:** System identifies conflicting advice
2. **Surface:** Chief of Staff notifies entrepreneur
3. **Coordinate:** Conflicting agents discuss
4. **Trade-off Analysis:** Present both perspectives with implications
5. **Entrepreneur Decides:** Human makes final call
6. **Learn:** Track which perspective proved correct

**Information Sharing:**
- Relevant insights shared across agents automatically
- Avoid redundant data gathering
- Maintain single source of truth
- Update shared context continuously

---

## Tool Requirements by Agent Category

### Master Orchestrator (Chief of Staff)

**Must Have Access To:**
- All 25 specialist agent outputs
- Complete business context database
- Decision history
- Strategic conviction tracker
- Execution order tracking
- All entrepreneur communication channels
- Calendar and schedule
- All integrated business tools (read access)

**Native AI Capabilities:**
- Natural language processing
- Context synthesis
- Priority ranking
- Multi-agent coordination
- Pattern recognition
- Report generation

---

### Category Specialists - Data & Integration Needs

**HIGH AI Impact Agents (Analytics-heavy):**

**Market Discovery, Revenue Model, Capital, Product, Growth, Operations, Customer Success**

*Common Data Sources:*
- Customer feedback (surveys, interviews, support tickets)
- Product analytics (Mixpanel, Amplitude, Google Analytics)
- Financial data (accounting software, Stripe, bank accounts)
- CRM data (customer lifecycle, interactions)
- Marketing data (campaigns, conversions, attribution)

*Common Integrations:*
- Analytics platforms
- Financial systems
- Communication tools
- Project management
- Documentation repositories

**MEDIUM AI Impact Agents (Strategic/Creative):**

**Vision, Business Archetype, Positioning, Brand, Legal, Team, Founder Longevity, Impact, Exit**

*Common Data Sources:*
- Entrepreneur communication history
- Team feedback and surveys
- Strategic documents
- Industry research
- Competitive intelligence
- Legal documents

*Common Tools:*
- Document management (Notion, Google Drive)
- Communication platforms (Slack, email)
- Legal document libraries
- Research databases
- Survey tools

---

### Support Specialists - Tool Needs

**Methodology Coach:**
- Framework documentation
- Case study databases
- Educational content library
- Learning management capabilities

**Cognitive Loop Support:**
- Communication history with language analysis
- Activity tracking
- Emotional tone analysis
- Pattern recognition across time

**Execution Sequencer:**
- Activity dependency database
- Completion tracking system
- Risk assessment models
- Alternative path algorithms

**Cross-Domain Integration:**
- All specialist agent access
- Decision impact analysis engine
- Trade-off synthesis capabilities
- Outcome tracking across domains

**Strategic Conviction Keeper:**
- Decision history with rationale
- Stated conviction database
- Consistency tracking
- Pattern analysis tools

---

## Integration Architecture

### External System Categories

**1. Financial Systems**
- Accounting: QuickBooks, Xero
- Payments: Stripe, PayPal, Square
- Banking: Plaid integration
- Cap Table: Carta, Pulley
- Expense Management: Expensify, Ramp

**2. Customer & Product**
- CRM: Salesforce, HubSpot, Pipedrive
- Product Analytics: Mixpanel, Amplitude, PostHog
- User Feedback: Intercom, Zendesk, Typeform
- Session Recording: FullStory, Hotjar
- A/B Testing: Optimizely, LaunchDarkly

**3. Operations & Development**
- Project Management: Linear, Jira, Asana
- Code Repositories: GitHub, GitLab
- CI/CD: GitHub Actions, CircleCI
- Cloud Infrastructure: AWS, Google Cloud, Vercel
- Monitoring: Datadog, Sentry

**4. Marketing & Growth**
- Marketing Automation: HubSpot, Marketo, Mailchimp
- Ad Platforms: Google Ads, Facebook Ads, LinkedIn Ads
- SEO Tools: Ahrefs, SEMrush
- Content Management: WordPress, Webflow
- Social Media: Buffer, Hootsuite

**5. Communication & Documentation**
- Team Communication: Slack, Microsoft Teams
- Email: Gmail, Outlook
- Video Conferencing: Zoom, Google Meet
- Documentation: Notion, Confluence, Google Docs
- File Storage: Google Drive, Dropbox

### Integration Principles

**1. Read-First Approach**
- Start with read-only access to minimize risk
- Prove value before requesting write permissions
- Explicit permission requests for sensitive data

**2. API-First Architecture**
- Use official APIs wherever possible
- Fallback to web scraping only when necessary
- Respect rate limits and terms of service

**3. Data Minimization**
- Only request data agents actually need
- Store minimum necessary for functionality
- Clear data retention policies

**4. Security by Default**
- Encrypt all data in transit and at rest
- OAuth for authentication where available
- Audit logging for all data access
- Compliance with SOC 2, GDPR, CCPA

---

## Behavioral Guardrails

### What Agents MUST Do

1. **Explain Reasoning:** Every recommendation includes clear rationale
2. **State Confidence:** Explicitly state confidence levels
3. **Acknowledge Limitations:** Honest about what agents can't do
4. **Defer When Appropriate:** Recognize human-only decisions
5. **Learn from Feedback:** Track outcomes, update models
6. **Coordinate Across Agents:** Prevent contradictions
7. **Respect Context:** Adapt to phase, cognitive state, constraints
8. **Protect Entrepreneur's Time:** Filter noise, surface signal

### What Agents MUST NOT Do

1. **Make Decisions Solo:** Major decisions require human approval
2. **Over-Promise:** Stay within known capabilities
3. **Create Contradictions:** Coordinate to prevent conflicting advice
4. **Overwhelm with Noise:** Proactivity must be filtered and valuable
5. **Ignore Context:** Context-free advice is dangerous
6. **Assume Preferences:** Learn and adapt, don't assume
7. **Skip Explanation:** Always explain the "why"
8. **Ignore Feedback:** When entrepreneur rejects advice, learn from it

---

## Success Criteria for Behavioral Models

**Context Awareness:**
- 90%+ accuracy in phase detection
- Real-time cognitive state recognition
- Correct constraint understanding
- Appropriate recommendation adaptation

**Proactive Intelligence:**
- 70%+ of proactive insights acted upon
- <5% "noise" alerts (entrepreneur ignores)
- High-impact issues surfaced 100% of time
- Timing appropriate (not interrupting focus)

**Adaptive Communication:**
- Entrepreneur satisfaction >8/10 with communication style
- Appropriate verbosity (not too brief, not too verbose)
- Tone matching entrepreneur preferences
- Framework teaching when helpful, not overwhelming

**Memory & Learning:**
- Preference learning accuracy >80%
- Outcome predictions improving over time
- Pattern recognition surfacing non-obvious insights
- Continuity across sessions (no starting over)

**Collaborative Intelligence:**
- Zero contradictory advice reaching entrepreneur
- Cross-domain insights surface 90%+ of time needed
- Agent coordination seamless (entrepreneur doesn't see complexity)
- Conflict resolution efficient (<24 hours)

---

**Next:** [Part 5: Operational Systems](./part-5-operational-systems.md)
