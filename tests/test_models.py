"""Tests for Pydantic data models (AnalysisResult, SWOTAnalysis, Competitor)."""

import pytest
from pydantic import ValidationError
from agents.analyst import AnalysisResult, SWOTAnalysis, Competitor


class TestSWOTAnalysis:
    """Validate SWOT model constraints and serialization."""

    def test_valid_swot(self):
        swot = SWOTAnalysis(
            strengths=["Strong brand"],
            weaknesses=["Slow growth"],
            opportunities=["New markets"],
            threats=["New regulation"],
        )
        assert len(swot.strengths) == 1
        assert swot.weaknesses[0] == "Slow growth"

    def test_empty_lists_allowed(self):
        swot = SWOTAnalysis(
            strengths=[], weaknesses=[], opportunities=[], threats=[]
        )
        assert swot.strengths == []

    def test_multiple_items(self):
        swot = SWOTAnalysis(
            strengths=["A", "B", "C", "D", "E"],
            weaknesses=["W1", "W2", "W3"],
            opportunities=["O1"],
            threats=["T1", "T2"],
        )
        assert len(swot.strengths) == 5
        assert len(swot.threats) == 2

    def test_missing_field_raises(self):
        with pytest.raises(ValidationError):
            SWOTAnalysis(strengths=["A"], weaknesses=["B"], opportunities=["C"])

    def test_serialization_roundtrip(self):
        swot = SWOTAnalysis(
            strengths=["S"], weaknesses=["W"], opportunities=["O"], threats=["T"]
        )
        data = swot.model_dump()
        restored = SWOTAnalysis(**data)
        assert restored == swot


class TestCompetitor:
    """Validate Competitor model."""

    def test_valid_competitor(self):
        comp = Competitor(
            name="Oracle",
            overview="Enterprise software company.",
            key_strength="Database technology",
            key_weakness="Complex licensing",
        )
        assert comp.name == "Oracle"

    def test_missing_field_raises(self):
        with pytest.raises(ValidationError):
            Competitor(name="Oracle", overview="Test")

    def test_json_roundtrip(self):
        comp = Competitor(
            name="Test Corp",
            overview="A test company.",
            key_strength="Testing",
            key_weakness="Not real",
        )
        json_str = comp.model_dump_json()
        restored = Competitor.model_validate_json(json_str)
        assert restored.name == comp.name


class TestAnalysisResult:
    """Validate the full AnalysisResult model."""

    @pytest.fixture
    def valid_analysis(self):
        return AnalysisResult(
            executive_summary="Test summary.",
            company_overview="Test overview.",
            market_position="Test position.",
            swot=SWOTAnalysis(
                strengths=["S1"], weaknesses=["W1"],
                opportunities=["O1"], threats=["T1"],
            ),
            top_competitors=[
                Competitor(
                    name="Rival Inc",
                    overview="A rival.",
                    key_strength="Speed",
                    key_weakness="Price",
                )
            ],
            key_trends=["AI adoption"],
            investment_thesis="Strong outlook.",
            risk_factors=["Market risk"],
        )

    def test_valid_analysis_creation(self, valid_analysis):
        assert valid_analysis.executive_summary == "Test summary."
        assert len(valid_analysis.top_competitors) == 1
        assert len(valid_analysis.key_trends) == 1

    def test_missing_required_field(self):
        with pytest.raises(ValidationError):
            AnalysisResult(
                executive_summary="Test",
                company_overview="Test",
            )

    def test_nested_swot_access(self, valid_analysis):
        assert valid_analysis.swot.strengths[0] == "S1"
        assert valid_analysis.swot.threats[0] == "T1"

    def test_serialization(self, valid_analysis):
        data = valid_analysis.model_dump()
        assert "swot" in data
        assert "top_competitors" in data
        assert isinstance(data["top_competitors"], list)

    def test_json_roundtrip(self, valid_analysis):
        json_str = valid_analysis.model_dump_json()
        restored = AnalysisResult.model_validate_json(json_str)
        assert restored.executive_summary == valid_analysis.executive_summary
        assert len(restored.top_competitors) == len(valid_analysis.top_competitors)
