"""
AnalysisAgent — Transforms raw research into structured strategic analysis.

Uses structured outputs (Pydantic) to guarantee a consistent,
machine-readable result that the report generator can reliably consume.
"""

from typing import Literal

import anthropic
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Data models — define the exact shape of the analysis output
# ---------------------------------------------------------------------------

class SWOTAnalysis(BaseModel):
    strengths: list[str] = Field(description="Internal strengths of the company (3–5 items)")
    weaknesses: list[str] = Field(description="Internal weaknesses or limitations (3–5 items)")
    opportunities: list[str] = Field(description="External opportunities the company can exploit (3–5 items)")
    threats: list[str] = Field(description="External threats or risks facing the company (3–5 items)")


class Force(BaseModel):
    """One of Porter's Five Forces — a rating plus the rationale."""
    rating: Literal["Low", "Medium", "High"] = Field(
        description="Strength of this force in the industry: Low, Medium or High"
    )
    rationale: str = Field(
        description="2-3 sentences justifying the rating, grounded in the research brief"
    )


class PortersFiveForces(BaseModel):
    """Porter's Five Forces industry attractiveness analysis."""
    competitive_rivalry: Force = Field(
        description="Intensity of competition between existing players"
    )
    threat_of_new_entrants: Force = Field(
        description="How easily new companies can enter the market"
    )
    threat_of_substitutes: Force = Field(
        description="Risk that customers switch to alternative products or services"
    )
    bargaining_power_of_suppliers: Force = Field(
        description="Leverage suppliers have over the company on price and terms"
    )
    bargaining_power_of_buyers: Force = Field(
        description="Leverage customers have over the company on price and terms"
    )
    summary: str = Field(
        description="One paragraph overall industry-attractiveness assessment"
    )


class Competitor(BaseModel):
    name: str = Field(description="Competitor company name")
    overview: str = Field(description="One-sentence description of the competitor")
    key_strength: str = Field(description="The competitor's single biggest advantage")
    key_weakness: str = Field(description="The competitor's single biggest limitation")


class AnalysisResult(BaseModel):
    executive_summary: str = Field(
        description="3–4 sentence executive summary of the company and its market position"
    )
    company_overview: str = Field(
        description="Concise paragraph covering founding, HQ, business model, products/services"
    )
    market_position: str = Field(
        description="Paragraph describing market standing, competitive advantages, and customer base"
    )
    swot: SWOTAnalysis
    porters_five_forces: PortersFiveForces = Field(
        description="Porter's Five Forces analysis of industry attractiveness"
    )
    top_competitors: list[Competitor] = Field(
        description="3–5 main competitors with structured comparison"
    )
    key_trends: list[str] = Field(
        description="5–7 significant industry trends relevant to the company"
    )
    investment_thesis: str = Field(
        description="2–3 sentence strategic outlook — growth potential or strategic rationale"
    )
    risk_factors: list[str] = Field(
        description="3–5 key risks the company faces"
    )


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a principal strategy consultant preparing a client deliverable.
Based on the raw research brief provided, produce a rigorous structured analysis.

Guidelines:
- Be concise but substantive — bullet points should be specific, not generic
- Base your analysis strictly on the research provided; do not invent facts
- SWOT items should be company-specific, not industry clichés
- For Porter's Five Forces, rate each force as Low / Medium / High and back
  the rating with 2-3 sentences of evidence drawn from the brief
- Competitors should be the actual named rivals from the research
- The investment thesis should reflect current strategic context"""


class AnalysisAgent:
    """
    Agent that converts a raw research brief into a validated AnalysisResult object.

    Uses `client.messages.parse()` with a Pydantic model for structured outputs,
    guaranteeing that the downstream report generator always receives well-formed data.
    """

    def __init__(self, client: anthropic.Anthropic, model: str = "claude-opus-4-6"):
        self.client = client
        self.model = model

    def analyze(self, company: str, research_brief: str) -> AnalysisResult:
        """
        Analyze raw research and return a structured AnalysisResult.

        Args:
            company: The company name being analyzed
            research_brief: The full text output from ResearchAgent

        Returns:
            A validated AnalysisResult Pydantic object
        """
        user_message = (
            f"Analyze the following research brief about '{company}' "
            f"and produce a complete structured analysis.\n\n"
            f"---RESEARCH BRIEF---\n{research_brief}\n---END OF BRIEF---"
        )

        response = self.client.messages.parse(
            model=self.model,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
            output_format=AnalysisResult,
            thinking={"type": "adaptive"},
        )

        return response.parsed_output
