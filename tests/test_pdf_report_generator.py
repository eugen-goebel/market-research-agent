"""Tests for PDF report generation."""

import os

from agents.mock_data import SAP_MOCK
from agents.analyst import AnalysisResult, SWOTAnalysis, Competitor
from utils.pdf_report_generator import generate_pdf_report


class TestPDFReportGeneration:
    """Test the full PDF generation pipeline."""

    def test_generates_pdf_file(self, tmp_path):
        path = generate_pdf_report("SAP SE", SAP_MOCK, output_dir=str(tmp_path))
        assert os.path.exists(path)
        assert path.endswith(".pdf")

    def test_filename_contains_company(self, tmp_path):
        path = generate_pdf_report("SAP SE", SAP_MOCK, output_dir=str(tmp_path))
        assert "sap_se" in os.path.basename(path)

    def test_file_not_empty(self, tmp_path):
        path = generate_pdf_report("SAP SE", SAP_MOCK, output_dir=str(tmp_path))
        assert os.path.getsize(path) > 1000

    def test_pdf_starts_with_header(self, tmp_path):
        path = generate_pdf_report("SAP SE", SAP_MOCK, output_dir=str(tmp_path))
        with open(path, "rb") as f:
            header = f.read(5)
        assert header == b"%PDF-"

    def test_creates_output_directory(self, tmp_path):
        new_dir = str(tmp_path / "new_subdir" / "reports")
        path = generate_pdf_report("Test Corp", SAP_MOCK, output_dir=new_dir)
        assert os.path.exists(path)
        assert os.path.isdir(new_dir)

    def test_special_characters_in_company_name(self, tmp_path):
        path = generate_pdf_report("Müller & Co / GmbH", SAP_MOCK, output_dir=str(tmp_path))
        assert os.path.exists(path)
        assert "müller" in os.path.basename(path)


class TestPDFReportWithMinimalData:
    """Test PDF generation with edge cases."""

    def _minimal_analysis(self):
        return AnalysisResult(
            executive_summary="Summary.",
            company_overview="Overview.",
            market_position="Position.",
            swot=SWOTAnalysis(
                strengths=["S"], weaknesses=["W"],
                opportunities=["O"], threats=["T"],
            ),
            top_competitors=[
                Competitor(
                    name="Rival",
                    overview="A rival company.",
                    key_strength="Fast",
                    key_weakness="Expensive",
                )
            ],
            key_trends=["Trend 1"],
            investment_thesis="Thesis.",
            risk_factors=["Risk 1"],
        )

    def test_minimal_data_generates(self, tmp_path):
        path = generate_pdf_report(
            "Minimal Corp", self._minimal_analysis(), output_dir=str(tmp_path)
        )
        assert os.path.exists(path)
        assert os.path.getsize(path) > 500
