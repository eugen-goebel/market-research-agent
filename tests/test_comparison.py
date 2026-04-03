"""Tests for competitor comparison mode."""

import os
import subprocess
import sys

import pytest
from unittest.mock import MagicMock, patch

from agents.analyst import AnalysisResult, SWOTAnalysis, Competitor
from agents.mock_data import SAP_MOCK, ZALANDO_MOCK, COMPARISON_MOCKS
from utils.comparison_report import generate_comparison_report


@pytest.fixture
def minimal_analysis():
    return AnalysisResult(
        executive_summary="Summary.",
        company_overview="Overview.",
        market_position="Position.",
        swot=SWOTAnalysis(
            strengths=["S1"], weaknesses=["W1"],
            opportunities=["O1"], threats=["T1"],
        ),
        top_competitors=[
            Competitor(name="Rival", overview="Desc",
                       key_strength="Strong", key_weakness="Weak"),
        ],
        key_trends=["Trend 1"],
        investment_thesis="Thesis.",
        risk_factors=["Risk 1"],
    )


class TestComparisonMocks:
    def test_has_sap(self):
        assert "SAP SE" in COMPARISON_MOCKS

    def test_has_zalando(self):
        assert "Zalando SE" in COMPARISON_MOCKS

    def test_zalando_mock_valid(self):
        assert isinstance(ZALANDO_MOCK, AnalysisResult)
        assert len(ZALANDO_MOCK.top_competitors) >= 3
        assert len(ZALANDO_MOCK.swot.strengths) >= 3
        assert len(ZALANDO_MOCK.key_trends) >= 5

    def test_zalando_mock_content(self):
        assert "Zalando" in ZALANDO_MOCK.company_overview
        assert len(ZALANDO_MOCK.executive_summary) > 100


class TestComparisonReport:
    def test_generates_docx(self, tmp_path, minimal_analysis):
        path = generate_comparison_report(
            ["A", "B"], [minimal_analysis, minimal_analysis],
            output_dir=str(tmp_path),
        )
        assert os.path.isfile(path)
        assert path.endswith(".docx")

    def test_filename_format(self, tmp_path, minimal_analysis):
        path = generate_comparison_report(
            ["Alpha Corp", "Beta Inc"], [minimal_analysis, minimal_analysis],
            output_dir=str(tmp_path),
        )
        name = os.path.basename(path)
        assert "alpha_corp" in name
        assert "beta_inc" in name
        assert "_vs_" in name

    def test_three_companies(self, tmp_path, minimal_analysis):
        path = generate_comparison_report(
            ["A", "B", "C"],
            [minimal_analysis, minimal_analysis, minimal_analysis],
            output_dir=str(tmp_path),
        )
        assert os.path.isfile(path)

    def test_with_real_mocks(self, tmp_path):
        path = generate_comparison_report(
            ["SAP SE", "Zalando SE"],
            [SAP_MOCK, ZALANDO_MOCK],
            output_dir=str(tmp_path),
        )
        assert os.path.isfile(path)
        assert os.path.getsize(path) > 10000

    def test_creates_directory(self, tmp_path, minimal_analysis):
        out = str(tmp_path / "nested" / "dir")
        path = generate_comparison_report(
            ["X", "Y"], [minimal_analysis, minimal_analysis],
            output_dir=out,
        )
        assert os.path.isfile(path)


class TestOrchestratorComparison:
    def test_mock_comparison(self, tmp_path):
        from agents.orchestrator import MarketResearchOrchestrator
        orch = MarketResearchOrchestrator(output_dir=str(tmp_path))
        path = orch.run_comparison_with_mock(
            ["SAP SE", "Zalando SE"],
            [SAP_MOCK, ZALANDO_MOCK],
        )
        assert os.path.isfile(path)

    @patch("agents.orchestrator.ResearchAgent")
    @patch("agents.orchestrator.AnalysisAgent")
    def test_comparison_calls_agents(self, mock_analyst_cls, mock_researcher_cls, tmp_path):
        from agents.orchestrator import MarketResearchOrchestrator

        mock_researcher = MagicMock()
        mock_researcher.research.return_value = "Research data"
        mock_researcher_cls.return_value = mock_researcher

        mock_analyst = MagicMock()
        mock_analyst.analyze.return_value = SAP_MOCK
        mock_analyst_cls.return_value = mock_analyst

        orch = MarketResearchOrchestrator(output_dir=str(tmp_path))
        path = orch.run_comparison(["Company A", "Company B"])

        assert mock_researcher.research.call_count == 2
        assert mock_analyst.analyze.call_count == 2
        assert os.path.isfile(path)


class TestComparisonCLI:
    def test_dry_run_compare(self, tmp_path):
        result = subprocess.run(
            [sys.executable, "main.py", "--dry-run",
             "--compare", "SAP SE", "Zalando SE",
             "--output", str(tmp_path)],
            capture_output=True, text=True,
            cwd=os.path.dirname(os.path.dirname(__file__)),
        )
        assert result.returncode == 0
        assert "COMPARISON" in result.stdout

    def test_compare_needs_two(self):
        result = subprocess.run(
            [sys.executable, "main.py", "--dry-run", "--compare", "OnlyOne"],
            capture_output=True, text=True,
            cwd=os.path.dirname(os.path.dirname(__file__)),
        )
        assert result.returncode != 0
