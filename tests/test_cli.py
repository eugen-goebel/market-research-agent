"""Tests for CLI argument parsing."""

import subprocess
import sys
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestCLIDryRun:
    """Test --dry-run mode end-to-end via subprocess."""

    def test_dry_run_succeeds(self, tmp_path):
        result = subprocess.run(
            [sys.executable, "main.py", "--dry-run", "--output", str(tmp_path)],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0
        assert "DRY RUN" in result.stdout

    def test_dry_run_creates_docx(self, tmp_path):
        subprocess.run(
            [sys.executable, "main.py", "--dry-run", "--output", str(tmp_path)],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=30,
        )
        docx_files = [f for f in os.listdir(tmp_path) if f.endswith(".docx")]
        assert len(docx_files) == 1

    def test_dry_run_with_custom_company(self, tmp_path):
        result = subprocess.run(
            [sys.executable, "main.py", "Test AG", "--dry-run", "--output", str(tmp_path)],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0
        docx_files = [f for f in os.listdir(tmp_path) if f.endswith(".docx")]
        assert len(docx_files) == 1
        assert "test_ag" in docx_files[0]

    def test_dry_run_output_mentions_steps(self, tmp_path):
        result = subprocess.run(
            [sys.executable, "main.py", "--dry-run", "--output", str(tmp_path)],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert "[1/3]" in result.stdout
        assert "[2/3]" in result.stdout
        assert "[3/3]" in result.stdout


class TestCLIErrorHandling:
    """Test CLI error messages when required args are missing."""

    def test_no_company_no_dryrun_fails(self):
        result = subprocess.run(
            [sys.executable, "main.py"],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=10,
            env={**os.environ, "ANTHROPIC_API_KEY": ""},
        )
        assert result.returncode != 0

    def test_no_api_key_fails(self):
        env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
        result = subprocess.run(
            [sys.executable, "main.py", "Test Corp"],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=10,
            env=env,
        )
        assert result.returncode != 0
        assert "ANTHROPIC_API_KEY" in result.stdout or "ANTHROPIC_API_KEY" in result.stderr
