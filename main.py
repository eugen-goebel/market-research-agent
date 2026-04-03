"""
Multi-Agent Market Research System
===================================
Generates a professional market research report for any company using a
three-stage AI pipeline: Research → Analysis → Report.

Usage:
    python3 main.py "SAP SE"
    python3 main.py "Zalando" --output ./reports
    python3 main.py --dry-run              # test without API key (uses SAP mock data)
"""

import argparse
import os
import sys
from dotenv import load_dotenv
from agents.orchestrator import MarketResearchOrchestrator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Multi-Agent Market Research System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py "SAP SE"
  python3 main.py "Zalando SE" --output ./reports
  python3 main.py --dry-run              # no API key needed, uses SAP mock data
        """,
    )
    parser.add_argument(
        "company",
        nargs="?",
        default=None,
        help='Company name to research (e.g. "SAP SE", "Zalando", "Tesla")',
    )
    parser.add_argument(
        "--compare",
        nargs="+",
        metavar="COMPANY",
        help="Compare 2-3 companies side-by-side (e.g., --compare 'SAP SE' 'Zalando SE')",
    )
    parser.add_argument(
        "--output",
        default="output",
        help="Directory to save the generated report (default: ./output)",
    )
    parser.add_argument(
        "--format",
        choices=["docx", "pdf"],
        default="docx",
        help="Output format for the report (default: docx)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip API calls and generate a report using built-in SAP SE mock data",
    )
    return parser.parse_args()


def main():
    load_dotenv()
    args = parse_args()

    if args.compare and len(args.compare) < 2:
        print("Error: --compare requires at least 2 companies.")
        sys.exit(1)
    if args.compare and len(args.compare) > 3:
        print("Error: --compare supports at most 3 companies.")
        sys.exit(1)

    # -----------------------------------------------------------------------
    # Dry-run: generate report from mock data, no API key required
    # -----------------------------------------------------------------------
    if args.dry_run:
        from agents.mock_data import SAP_MOCK, COMPARISON_MOCKS

        if args.compare:
            companies = args.compare
            analyses = [COMPARISON_MOCKS.get(c, SAP_MOCK) for c in companies]
            print(f"\n{'='*60}")
            print(f"  DRY RUN — COMPETITOR COMPARISON")
            print(f"  Companies: {', '.join(companies)}")
            print(f"{'='*60}\n")

            orch = MarketResearchOrchestrator(output_dir=args.output)
            report_path = orch.run_comparison_with_mock(companies, analyses)
        else:
            from utils.report_generator import generate_docx_report
            from utils.pdf_report_generator import generate_pdf_report

            company = args.company or "SAP SE"
            fmt = args.format
            print(f"\n{'='*60}")
            print(f"  DRY RUN — using mock data for: {company}")
            print(f"{'='*60}\n")
            print("[1/3]  ResearchAgent:  skipped (dry-run)\n")
            print("[2/3]  AnalysisAgent:  skipped (dry-run)\n")
            print(f"[3/3]  ReportGenerator: building {fmt.upper()}...\n")

            generator = generate_pdf_report if fmt == "pdf" else generate_docx_report
            report_path = generator(
                company=company,
                analysis=SAP_MOCK,
                output_dir=args.output,
            )

        print(f"       Report saved:\n       {report_path}\n")
        print(f"{'='*60}")
        print("  Open the report in Word or LibreOffice to preview.")
        print(f"{'='*60}\n")
        return

    # -----------------------------------------------------------------------
    # Normal run: requires API key and company name
    # -----------------------------------------------------------------------
    if not args.company and not args.compare:
        print("Error: please provide a company name, e.g.:")
        print('  python3 main.py "SAP SE"')
        print('  python3 main.py --compare "SAP SE" "Zalando SE"')
        print("  python3 main.py --dry-run   (no API key needed)")
        sys.exit(1)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set.")
        print("  1. Copy .env.example to .env")
        print("  2. Add your API key: https://console.anthropic.com/")
        print()
        print("  Tip: python3 main.py --dry-run   (works without an API key)")
        sys.exit(1)

    orchestrator = MarketResearchOrchestrator(
        api_key=api_key,
        output_dir=args.output,
        report_format=args.format,
    )

    try:
        if args.compare:
            report_path = orchestrator.run_comparison(args.compare)
        else:
            report_path = orchestrator.run(args.company)
        print(f"\nReport: {report_path}")
    except KeyboardInterrupt:
        print("\n\nAborted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
