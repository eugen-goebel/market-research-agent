"""
MarketResearchOrchestrator — Coordinates all agents in the research pipeline.

Pipeline:
  1. ResearchAgent  → gathers raw web intelligence
  2. AnalysisAgent  → structures and analyzes the research
  3. ReportGenerator → produces the final DOCX document
"""

import anthropic
from .researcher import ResearchAgent
from .analyst import AnalysisAgent
from utils.report_generator import generate_docx_report


class MarketResearchOrchestrator:
    """
    High-level coordinator for the multi-agent market research pipeline.

    Attributes:
        client:     Shared Anthropic client instance
        output_dir: Directory where generated reports are saved
    """

    def __init__(self, api_key: str | None = None, output_dir: str = "output"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.output_dir = output_dir
        self._researcher = ResearchAgent(self.client)
        self._analyst = AnalysisAgent(self.client)

    def run(self, company: str) -> str:
        """
        Execute the full research pipeline for a given company.

        Args:
            company: Company name to research (e.g. "SAP SE", "Zalando")

        Returns:
            Absolute path to the generated DOCX report
        """
        print(f"\n{'='*60}")
        print(f"  Market Research Agent  —  {company}")
        print(f"{'='*60}\n")

        # ---------------------------------------------------------------
        # Phase 1: Research
        # ---------------------------------------------------------------
        print("[1/3]  ResearchAgent: Gathering web intelligence...")
        print("       (This may take 30–60 seconds while the agent searches the web)\n")

        research_brief = self._researcher.research(company)

        word_count = len(research_brief.split())
        print(f"       ✓ Research complete — {word_count} words gathered\n")

        # ---------------------------------------------------------------
        # Phase 2: Analysis
        # ---------------------------------------------------------------
        print("[2/3]  AnalysisAgent: Structuring analysis & SWOT...\n")

        analysis = self._analyst.analyze(company, research_brief)

        print(f"       ✓ Analysis complete")
        print(f"         • SWOT: {len(analysis.swot.strengths)}S / "
              f"{len(analysis.swot.weaknesses)}W / "
              f"{len(analysis.swot.opportunities)}O / "
              f"{len(analysis.swot.threats)}T")
        print(f"         • Competitors: {len(analysis.top_competitors)}")
        print(f"         • Trends: {len(analysis.key_trends)}\n")

        # ---------------------------------------------------------------
        # Phase 3: Report Generation
        # ---------------------------------------------------------------
        print("[3/3]  ReportGenerator: Building DOCX report...\n")

        report_path = generate_docx_report(
            company=company,
            analysis=analysis,
            output_dir=self.output_dir,
        )

        print(f"       ✓ Report saved:\n       {report_path}\n")
        print(f"{'='*60}")
        print(f"  Done! Open the report in Microsoft Word or LibreOffice.")
        print(f"{'='*60}\n")

        return report_path
