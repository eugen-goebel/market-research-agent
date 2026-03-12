"""Tests for mock data integrity — ensures dry-run mode works correctly."""

from agents.mock_data import SAP_MOCK
from agents.analyst import AnalysisResult, SWOTAnalysis, Competitor


class TestMockDataIntegrity:
    """Verify SAP_MOCK is a valid, complete AnalysisResult."""

    def test_mock_is_analysis_result(self):
        assert isinstance(SAP_MOCK, AnalysisResult)

    def test_executive_summary_not_empty(self):
        assert len(SAP_MOCK.executive_summary) > 50

    def test_company_overview_not_empty(self):
        assert len(SAP_MOCK.company_overview) > 50

    def test_market_position_not_empty(self):
        assert len(SAP_MOCK.market_position) > 50

    def test_swot_is_valid(self):
        assert isinstance(SAP_MOCK.swot, SWOTAnalysis)
        assert len(SAP_MOCK.swot.strengths) >= 3
        assert len(SAP_MOCK.swot.weaknesses) >= 3
        assert len(SAP_MOCK.swot.opportunities) >= 3
        assert len(SAP_MOCK.swot.threats) >= 3

    def test_competitors_exist(self):
        assert len(SAP_MOCK.top_competitors) >= 3
        for comp in SAP_MOCK.top_competitors:
            assert isinstance(comp, Competitor)
            assert len(comp.name) > 0
            assert len(comp.overview) > 0

    def test_key_trends_exist(self):
        assert len(SAP_MOCK.key_trends) >= 5

    def test_investment_thesis_not_empty(self):
        assert len(SAP_MOCK.investment_thesis) > 30

    def test_risk_factors_exist(self):
        assert len(SAP_MOCK.risk_factors) >= 3

    def test_mock_serializes_to_json(self):
        json_str = SAP_MOCK.model_dump_json()
        restored = AnalysisResult.model_validate_json(json_str)
        assert restored.executive_summary == SAP_MOCK.executive_summary
