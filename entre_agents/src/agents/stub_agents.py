"""
Stub agents for multi-agent coordination.

These are placeholder agents that Chief of Staff can consult.
They provide basic responses now and will be fully built out later.

Current stubs:
- Market Discovery Agent
- Product & Technology Agent
- Capital & Financing Agent
"""

from typing import Dict, Any


class StubAgent:
    """
    Base class for stub agents.
    Provides minimal functionality for Chief of Staff to consult.
    """

    def __init__(self, name: str, capabilities: str, config=None, db=None, llm=None):
        self.name = name
        self.capabilities = capabilities
        self.config = config
        self.db = db
        self.llm = llm

    def consult(self, question: str, context: Dict[str, Any], from_agent: str) -> str:
        """
        Handle a consultation request from another agent.

        Args:
            question: The question/task from the consulting agent
            context: Relevant context
            from_agent: Name of the agent making the request

        Returns:
            Response as a string
        """
        return self._generate_response(question, context)

    def _generate_response(self, question: str, context: Dict[str, Any]) -> str:
        """
        Generate response to consultation.
        Override in subclasses for agent-specific logic.
        """
        return f"[{self.name} - Stub] I'm not fully implemented yet, but here's what I would help with: {self.capabilities}"


class MarketDiscoveryAgent(StubAgent):
    """
    Market Discovery Agent (Stub)

    Helps entrepreneurs:
    - Understand target customers
    - Validate problem/solution fit
    - Analyze customer feedback
    - Identify market segments
    """

    def __init__(self, config=None, db=None, llm=None):
        super().__init__(
            name="Market Discovery Agent",
            capabilities="Customer research, validation, feedback analysis, market segmentation",
            config=config,
            db=db,
            llm=llm
        )

    def _generate_response(self, question: str, context: Dict[str, Any]) -> str:
        """
        Provide market discovery guidance.
        """

        # Simple keyword-based responses for now
        question_lower = question.lower()

        if "customer" in question_lower or "user" in question_lower:
            return """I can help with customer discovery. Here's my recommendation:

**Customer Discovery Approach:**
1. **Define Target Segment**: Start with your hypothesis about who has this problem
2. **Customer Interviews**: Conduct 10-15 in-depth interviews (30-45 min each)
3. **Key Questions to Ask**:
   - Tell me about the last time you experienced [problem]
   - How do you currently solve this?
   - What's frustrating about current solutions?
   - If you had a magic wand, what would the perfect solution look like?

4. **Look for Patterns**: What pain points come up in 80%+ of conversations?

**Next Steps:**
- Create interview script
- Identify 20 people who fit target profile
- Schedule and conduct interviews
- Document insights

Would you like me to help create an interview guide?"""

        elif "market" in question_lower or "segment" in question_lower:
            return """Let's analyze your market opportunity:

**Market Segmentation Framework:**
1. **Who has the problem most acutely?** (pain intensity)
2. **Who is easiest to reach?** (distribution)
3. **Who has budget to pay?** (willingness to pay)
4. **Who is currently underserved?** (competition)

**Recommendation:**
Start with the segment that scores highest across all 4 dimensions.
Validate with 10+ customer interviews before building anything.

**Red Flags to Watch:**
- "Everyone" is your customer → need to narrow
- Can't identify specific pain point → validate problem first
- No budget for solutions → reconsider monetization

What's your current hypothesis about your target segment?"""

        elif "validation" in question_lower or "validate" in question_lower:
            return """Here's a validation roadmap:

**Phase 1: Problem Validation** (Week 1-2)
- 10-15 customer interviews
- Confirm: Do people really have this problem?
- Measure: How painful is it? (1-10 scale)

**Phase 2: Solution Validation** (Week 3-4)
- Show mockups/prototype
- Confirm: Does your solution resonate?
- Test: Would they pay for this?

**Phase 3: MVP Validation** (Week 5-8)
- Build minimal version
- Get 10-50 users actually using it
- Measure: Retention, engagement, willingness to pay

**You're Ready to Build When:**
✓ 80%+ of interviews confirm painful problem
✓ People ask "when can I get this?"
✓ Clear willingness to pay emerges

Where are you in this journey?"""

        else:
            # Generic response
            return f"""I'm the Market Discovery Agent. I help with:

- **Customer Research**: Understanding who your customers are and what they need
- **Problem Validation**: Confirming the problem is real and painful enough
- **Solution Validation**: Testing if your solution resonates
- **Market Sizing**: Estimating market opportunity
- **Segmentation**: Identifying your best target customers

Based on your question: "{question}"

I recommend starting with customer interviews to validate assumptions.
Would you like help designing a customer discovery plan?

[Note: I'm a stub agent - will be fully implemented in Phase 2]"""


class ProductTechnologyAgent(StubAgent):
    """
    Product & Technology Agent (Stub)

    Helps entrepreneurs:
    - Scope MVP
    - Make build vs. buy decisions
    - Provide technical architecture guidance
    - Generate code and technical specs
    """

    def __init__(self, config=None, db=None, llm=None):
        super().__init__(
            name="Product & Technology Agent",
            capabilities="MVP scoping, technical architecture, code generation, build vs. buy decisions",
            config=config,
            db=db,
            llm=llm
        )

    def _generate_response(self, question: str, context: Dict[str, Any]) -> str:
        """
        Provide product/technology guidance.
        """

        question_lower = question.lower()

        if "mvp" in question_lower or "minimum" in question_lower:
            return """Let's scope your MVP using the "Minimum Viable Product" principle:

**MVP Scoping Framework:**

**What to INCLUDE:**
✓ Core value proposition (the ONE thing that solves the main problem)
✓ Minimum user flow to deliver value
✓ Just enough to test your riskiest assumption

**What to EXCLUDE:**
✗ Nice-to-have features
✗ Scalability (build for 100 users, not 1M)
✗ Polish and perfection
✗ Features that don't test core hypothesis

**Your MVP Should:**
- Be buildable in 4-8 weeks
- Cost <$10K to build (if outsourced) or <200 hours (if you build)
- Let 10-50 users test core value proposition
- Give you clear signal: does this solve the problem?

**Next Steps:**
1. Write user stories for core flow
2. Identify riskiest assumptions
3. Ruthlessly cut features that don't test those assumptions

What's the ONE problem your MVP absolutely must solve?"""

        elif "technical" in question_lower or "architecture" in question_lower or "stack" in question_lower:
            return """Here's my technical recommendation:

**Tech Stack Guidance for Startups:**

**Principle: Use Boring Technology**
- Choose mature, well-documented technologies
- Optimize for speed of development, not coolness
- You can always rebuild later with exotic tech

**Recommended Stack (2025):**

**Web App:**
- Frontend: React/Next.js or Vue/Nuxt (most talent available)
- Backend: Node.js/Express, Python/Flask, or Ruby/Rails
- Database: PostgreSQL (relational) + Redis (caching)
- Hosting: Vercel, Railway, or AWS/GCP

**Mobile App:**
- Cross-platform: React Native or Flutter
- Native: Swift (iOS) + Kotlin (Android) only if you have specific needs

**Key Decision Factors:**
1. What does your team know already?
2. What has the most available talent? (for hiring)
3. What gets you to MVP fastest?

**Build vs. Buy:**
- Auth: Use Auth0, Clerk, or Supabase (don't build)
- Payments: Use Stripe (definitely don't build)
- Email: Use SendGrid, Postmark (don't build)
- Analytics: Use Mixpanel, Amplitude (don't build)

BUILD: Your unique value proposition
BUY: Everything else

What's your core technical challenge?"""

        elif "code" in question_lower or "build" in question_lower:
            return """Let's talk about building your product:

**Build Approach:**

**Option 1: No-Code/Low-Code** (Fastest)
- Tools: Bubble, Webflow, Airtable, Zapier
- Timeline: Days to weeks
- Best for: Validating idea quickly, non-technical founders
- Limitation: Harder to scale, limited customization

**Option 2: Outsourced Development**
- Cost: $50-150/hour, $10K-50K for MVP
- Timeline: 4-12 weeks
- Best for: Non-technical founders with budget
- Risk: Handoff issues, ongoing maintenance

**Option 3: Technical Co-Founder**
- Cost: Equity (typically 20-40%)
- Timeline: Depends on their availability
- Best for: Complex technical products
- Risk: Founder relationship issues

**Option 4: Learn to Code**
- Cost: Time + course fees ($50-500)
- Timeline: 3-6 months to MVP level
- Best for: Technical products, long-term control
- Risk: Slower initial progress

**My Recommendation:**
Start with no-code if possible to validate. If validation is positive,
THEN invest in custom development.

Where are you in your journey?"""

        else:
            return f"""I'm the Product & Technology Agent. I help with:

- **MVP Scoping**: What to build (and what not to build)
- **Technical Architecture**: Tech stack, infrastructure, scalability
- **Build vs. Buy**: When to use existing tools vs. custom development
- **Code Generation**: Helping write code and technical specifications
- **Development Planning**: Timelines, milestones, technical hiring

Based on your question: "{question}"

I recommend starting with a ruthlessly scoped MVP that tests your
core value proposition with minimal features.

[Note: I'm a stub agent - will be fully implemented in Phase 3]"""


class CapitalFinancingAgent(StubAgent):
    """
    Capital & Financing Agent (Stub)

    Helps entrepreneurs:
    - Model financial projections
    - Manage burn rate and runway
    - Plan fundraising
    - Make financial decisions
    """

    def __init__(self, config=None, db=None, llm=None):
        super().__init__(
            name="Capital & Financing Agent",
            capabilities="Financial modeling, burn rate analysis, fundraising strategy, runway management",
            config=config,
            db=db,
            llm=llm
        )

    def _generate_response(self, question: str, context: Dict[str, Any]) -> str:
        """
        Provide financial guidance.
        """

        question_lower = question.lower()

        if "burn" in question_lower or "runway" in question_lower:
            return """Let's analyze your runway situation:

**Burn Rate & Runway Framework:**

**Key Metrics:**
1. **Monthly Burn Rate** = Monthly expenses - Monthly revenue
2. **Runway** = Cash in bank / Monthly burn rate
3. **Danger Zone** = When runway < 6 months

**Action Thresholds:**

**Runway > 12 months:** ✅ Healthy
- Focus on growth and product
- No urgent financing needed

**Runway 6-12 months:** ⚠️ Caution
- Start exploring fundraising options
- Model different scenarios
- Build investor relationships

**Runway < 6 months:** 🚨 Critical
- Immediate action required
- Options: Cut burn, raise emergency round, pivot to revenue

**Questions to Ask:**
1. What's your current monthly burn?
2. What's your current monthly revenue (if any)?
3. How much cash in bank?
4. What growth initiatives could increase revenue?
5. What expenses could be cut if needed?

**Next Steps:**
Build a 12-month financial model showing:
- Monthly burn by category
- Revenue projections (conservative, realistic, optimistic)
- Runway scenarios

Would you like help building this model?"""

        elif "fundrais" in question_lower or "investment" in question_lower or "investor" in question_lower:
            return """Let's talk fundraising strategy:

**Fundraising Decision Framework:**

**Should You Fundraise?**

**Consider FUNDRAISING if:**
✓ Large market opportunity (>$1B potential)
✓ Winner-take-most dynamics (network effects, economies of scale)
✓ Need capital to grow faster than competition
✓ Clear path to 10x return for investors

**Consider BOOTSTRAPPING if:**
✓ Profitable business model from day 1
✓ Don't need to move extremely fast
✓ Want to maintain control
✓ Market doesn't require massive upfront investment

**Fundraising Stages:**

**Pre-Seed** ($100K-500K)
- Stage: Idea to prototype
- Investors: Angels, pre-seed funds, accelerators
- Dilution: 5-15%

**Seed** ($500K-2M)
- Stage: MVP + early traction
- Investors: Seed funds, angels
- Dilution: 15-25%

**Series A** ($2M-10M)
- Stage: Product-market fit, strong growth
- Investors: VCs
- Dilution: 20-30%

**Timeline:**
- Plan for 3-6 month fundraising process
- Start when runway is 9-12 months
- NEVER start when runway < 6 months (desperation shows)

**Your Readiness:**
Are you:
- [ ] Post-revenue?
- [ ] Growing >20% month-over-month?
- [ ] Clear on your market size ($1B+)?
- [ ] Have a compelling team?

Where are you in this journey?"""

        elif "financial" in question_lower or "model" in question_lower or "revenue" in question_lower:
            return """Let's build your financial model:

**Startup Financial Model Components:**

**1. Revenue Model**
- How do you make money? (subscription, transaction fees, usage-based, etc.)
- What's your pricing? ($X/month, $Y/transaction, etc.)
- How many customers can you acquire? (by month)
- What's your conversion rate? (visitors → paying customers)

**2. Cost Structure**

**Fixed Costs** (same regardless of customers):
- Salaries & contractors
- Software/tools subscriptions
- Office/overhead (if any)

**Variable Costs** (scale with customers):
- Customer acquisition cost (CAC)
- Cost of goods sold (COGS)
- Support costs

**3. Key Metrics**

**Unit Economics:**
- CAC (Customer Acquisition Cost)
- LTV (Lifetime Value)
- LTV:CAC Ratio (should be >3:1)

**Growth Metrics:**
- Monthly recurring revenue (MRR)
- Churn rate
- Net revenue retention

**Efficiency:**
- Burn multiple (cash burned / new ARR added)
- Gross margin

**12-Month Projection:**
Create a spreadsheet with:
- Month-by-month revenue
- Month-by-month costs
- Cash flow
- Runway calculation

**Rule of Thumb:**
Your financial model will be wrong. That's OK.
Build it to:
1. Understand the business
2. Identify key assumptions to test
3. Communicate with investors

What's your revenue model?"""

        else:
            return f"""I'm the Capital & Financing Agent. I help with:

- **Financial Modeling**: Building revenue and expense projections
- **Burn Rate Analysis**: Understanding cash flow and runway
- **Fundraising Strategy**: When, how much, and from whom to raise
- **Financial Decisions**: Evaluating hire/spend decisions impact on runway
- **Scenario Planning**: What if we grow faster/slower?

Based on your question: "{question}"

I recommend starting by understanding your current burn rate and
runway, then modeling different growth scenarios.

[Note: I'm a stub agent - will be fully implemented in Phase 4]"""


# Convenience function to create all stub agents
def create_stub_agents(config=None, db=None, llm=None):
    """
    Create all stub specialist agents.

    Returns:
        Dict of agent_name -> agent_instance
    """
    return {
        "Market Discovery Agent": MarketDiscoveryAgent(config, db, llm),
        "Product & Technology Agent": ProductTechnologyAgent(config, db, llm),
        "Capital & Financing Agent": CapitalFinancingAgent(config, db, llm)
    }
