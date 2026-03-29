"""Tests for agent classes (using mocked API client)."""

from unittest.mock import MagicMock
from agents.researcher import ResearchAgent
from agents.analyst import AnalysisAgent, AnalysisResult
from agents.orchestrator import MarketResearchOrchestrator
from agents.mock_data import SAP_MOCK


class TestResearchAgent:
    """Test ResearchAgent with a mocked Anthropic client."""

    def _make_mock_response(self, text, stop_reason="end_turn"):
        block = MagicMock()
        block.text = text
        block.type = "text"

        response = MagicMock()
        response.content = [block]
        response.stop_reason = stop_reason
        return response

    def test_research_returns_text(self):
        mock_client = MagicMock()
        mock_client.messages.create.return_value = self._make_mock_response(
            "SAP is an enterprise software company."
        )

        agent = ResearchAgent(mock_client)
        result = agent.research("SAP SE")

        assert "SAP" in result
        assert mock_client.messages.create.called

    def test_research_handles_pause_turn(self):
        mock_client = MagicMock()
        # First call returns pause_turn, second returns end_turn
        mock_client.messages.create.side_effect = [
            self._make_mock_response("Partial research...", "pause_turn"),
            self._make_mock_response("Complete research about SAP.", "end_turn"),
        ]

        agent = ResearchAgent(mock_client)
        result = agent.research("SAP SE")

        assert "Complete research" in result
        assert mock_client.messages.create.call_count == 2

    def test_research_uses_correct_tools(self):
        mock_client = MagicMock()
        mock_client.messages.create.return_value = self._make_mock_response("Result.")

        agent = ResearchAgent(mock_client)
        agent.research("Test Corp")

        call_kwargs = mock_client.messages.create.call_args[1]
        tools = call_kwargs["tools"]
        assert any(t["type"] == "web_search_20260209" for t in tools)

    def test_research_uses_adaptive_thinking(self):
        mock_client = MagicMock()
        mock_client.messages.create.return_value = self._make_mock_response("Result.")

        agent = ResearchAgent(mock_client)
        agent.research("Test Corp")

        call_kwargs = mock_client.messages.create.call_args[1]
        assert call_kwargs["thinking"] == {"type": "adaptive"}


class TestAnalysisAgent:
    """Test AnalysisAgent with a mocked Anthropic client."""

    def test_analyze_returns_analysis_result(self):
        mock_client = MagicMock()

        mock_response = MagicMock()
        mock_response.parsed_output = SAP_MOCK
        mock_client.messages.parse.return_value = mock_response

        agent = AnalysisAgent(mock_client)
        result = agent.analyze("SAP SE", "Raw research brief text...")

        assert isinstance(result, AnalysisResult)
        assert result.executive_summary == SAP_MOCK.executive_summary

    def test_analyze_passes_correct_model(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.parsed_output = SAP_MOCK
        mock_client.messages.parse.return_value = mock_response

        agent = AnalysisAgent(mock_client, model="claude-sonnet-4-6")
        agent.analyze("Test", "Brief.")

        call_kwargs = mock_client.messages.parse.call_args[1]
        assert call_kwargs["model"] == "claude-sonnet-4-6"

    def test_analyze_uses_structured_output(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.parsed_output = SAP_MOCK
        mock_client.messages.parse.return_value = mock_response

        agent = AnalysisAgent(mock_client)
        agent.analyze("Test", "Brief.")

        call_kwargs = mock_client.messages.parse.call_args[1]
        assert call_kwargs["output_format"] == AnalysisResult


class TestOrchestrator:
    """Test orchestrator coordination logic."""

    def test_orchestrator_initializes(self):
        orch = MarketResearchOrchestrator(api_key="test-key")
        assert orch._researcher is not None
        assert orch._analyst is not None

    def test_orchestrator_full_pipeline(self, tmp_path):
        mock_client = MagicMock()

        # Mock researcher response
        research_block = MagicMock()
        research_block.text = "Research findings about SAP."
        research_block.type = "text"
        research_response = MagicMock()
        research_response.content = [research_block]
        research_response.stop_reason = "end_turn"
        mock_client.messages.create.return_value = research_response

        # Mock analyst response
        analysis_response = MagicMock()
        analysis_response.parsed_output = SAP_MOCK
        mock_client.messages.parse.return_value = analysis_response

        orch = MarketResearchOrchestrator(output_dir=str(tmp_path))
        orch.client = mock_client
        orch._researcher = ResearchAgent(mock_client)
        orch._analyst = AnalysisAgent(mock_client)

        report_path = orch.run("SAP SE")
        assert report_path.endswith(".docx")
        assert "sap_se" in report_path
