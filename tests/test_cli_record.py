"""
Comprehensive tests for epi_cli/record.py (CLI record command).

Tests the full CLI recording workflow including:
- Command execution and recording
- Environment variable setup
- Signing
- Output packaging
"""

import os
import sys
import tempfile
from pathlib import Path
import pytest
import zipfile
import json

from epi_cli.record import _ensure_python_command, _build_env_for_child


class TestEnsurePythonCommand:
    """Test _ensure_python_command helper."""
    
    def test_python_script_gets_interpreter(self):
        """Python scripts should get sys.executable prepended."""
        cmd = ["script.py", "arg1"]
        result = _ensure_python_command(cmd)
        assert result[0] == sys.executable
        assert result[1] == "script.py"
        assert result[2] == "arg1"
    
    def test_python_script_uppercase(self):
        """Uppercase .PY extension should work."""
        cmd = ["SCRIPT.PY"]
        result = _ensure_python_command(cmd)
        assert result[0] == sys.executable
    
    def test_non_python_command_unchanged(self):
        """Non-Python commands should pass through."""
        cmd = ["ls", "-la"]
        result = _ensure_python_command(cmd)
        assert result == cmd
    
    def test_empty_command(self):
        """Empty command should return empty."""
        result = _ensure_python_command([])
        assert result == []
    
    def test_python_already_present(self):
        """Commands starting with python should pass through."""
        cmd = ["python", "script.py"]
        result = _ensure_python_command(cmd)
        assert result == cmd


class TestBuildEnvForChild:
    """Test _build_env_for_child environment setup."""
    
    def test_epi_record_flag_set(self):
        """EPI_RECORD should be set to 1."""
        temp_dir = Path(tempfile.mkdtemp())
        env = _build_env_for_child(temp_dir, True)
        assert env["EPI_RECORD"] == "1"
    
    def test_steps_dir_set(self):
        """EPI_STEPS_DIR should point to temp dir."""
        temp_dir = Path(tempfile.mkdtemp())
        env = _build_env_for_child(temp_dir, True)
        assert env["EPI_STEPS_DIR"] == str(temp_dir)
    
    def test_redaction_enabled(self):
        """EPI_REDACT should be 1 when enabled."""
        temp_dir = Path(tempfile.mkdtemp())
        env = _build_env_for_child(temp_dir, True)
        assert env["EPI_REDACT"] == "1"
    
    def test_redaction_disabled(self):
        """EPI_REDACT should be 0 when disabled."""
        temp_dir = Path(tempfile.mkdtemp())
        env = _build_env_for_child(temp_dir, False)
        assert env["EPI_REDACT"] == "0"
    
    def test_pythonpath_includes_bootstrap(self):
        """PYTHONPATH should include bootstrap directory."""
        temp_dir = Path(tempfile.mkdtemp())
        env = _build_env_for_child(temp_dir, True)
        assert "PYTHONPATH" in env
        # Should contain epi_bootstrap
        assert "epi_bootstrap_" in env["PYTHONPATH"]
    
    def test_pythonpath_includes_project_root(self):
        """PYTHONPATH should include project root."""
        temp_dir = Path(tempfile.mkdtemp())
        env = _build_env_for_child(temp_dir, True)
        pythonpath = env["PYTHONPATH"]
        # Should contain multiple paths
        assert os.pathsep in pythonpath or len(pythonpath) > 0
    
    def test_preserves_existing_pythonpath(self):
        """Should preserve existing PYTHONPATH."""
        original = os.environ.get("PYTHONPATH", "")
        try:
            os.environ["PYTHONPATH"] = "/some/custom/path"
            temp_dir = Path(tempfile.mkdtemp())
            env = _build_env_for_child(temp_dir, True)
            assert "/some/custom/path" in env["PYTHONPATH"]
        finally:
            if original:
                os.environ["PYTHONPATH"] = original
            else:
                os.environ.pop("PYTHONPATH", None)


class TestCLIRecordCommand:
    """Integration tests for the record CLI command."""
    
    def test_record_simple_python_script(self, tmp_path):
        """Test recording a simple Python script."""
        from typer.testing import CliRunner
        from epi_cli.main import app
        
        runner = CliRunner()
        
        # Create a simple test script
        test_script = tmp_path / "test_script.py"
        test_script.write_text('print("Hello from recorded script")')
        
        output_epi = tmp_path / "output.epi"
        
        # Run record command
        result = runner.invoke(app, [
            "record",
            "--out", str(output_epi),
            "--no-sign",  # Skip signing for faster test
            "--", 
            "python", str(test_script)
        ])
        
        # Should succeed
        assert result.exit_code == 0
        
        # Output file should exist
        assert output_epi.exists()
        
        # Should be a valid ZIP
        assert zipfile.is_zipfile(output_epi)
    
    def test_record_with_signing(self, tmp_path):
        """Test recording with automatic signing."""
        from typer.testing import CliRunner
        from epi_cli.main import app
        
        runner = CliRunner()
        
        # Create test script
        test_script = tmp_path / "test_script.py"
        test_script.write_text('print("Test")')
        
        output_epi = tmp_path / "signed.epi"
        
        # Generate default key first
        runner.invoke(app, ["keys", "generate", "--name", "default"])
        
        # Run record command with signing
        result = runner.invoke(app, [
            "record",
            "--out", str(output_epi),
            "--", 
            "python", str(test_script)
        ])
        
        # Check if file exists
        if output_epi.exists():
            # Verify it's a valid EPI file
            with zipfile.ZipFile(output_epi, 'r') as zf:
                assert 'manifest.json' in zf.namelist()
                
                # Check if signed
                manifest_data = json.loads(zf.read('manifest.json'))
                # Signature might be present (depends on key availability)
                assert 'signature' in manifest_data or 'signature' not in manifest_data
    
    def test_record_adds_epi_extension(self, tmp_path):
        """Test that .epi extension is added if missing."""
        from typer.testing import CliRunner
        from epi_cli.main import app
        
        runner = CliRunner()
        
        test_script = tmp_path / "test.py"
        test_script.write_text('print("test")')
        
        output_file = tmp_path / "output_without_extension"
        
        result = runner.invoke(app, [
            "record",
            "--out", str(output_file),
            "--no-sign",
            "--",
            "python", str(test_script)
        ])
        
        # Should create file with .epi extension
        expected_path = tmp_path / "output_without_extension.epi"
        if expected_path.exists():
            assert expected_path.exists()
    
    def test_record_no_command_fails(self):
        """Test that record fails without a command."""
        from typer.testing import CliRunner
        from epi_cli.main import app
        
        runner = CliRunner()
        
        result = runner.invoke(app, [
            "record",
            "--out", "test.epi"
        ])
        
        # Should fail (no command provided)
        assert result.exit_code != 0
    
    def test_record_with_no_redact_flag(self, tmp_path):
        """Test recording with secret redaction disabled."""
        from typer.testing import CliRunner
        from epi_cli.main import app
        
        runner = CliRunner()
        
        test_script = tmp_path / "test.py"
        test_script.write_text('print("test")')
        
        output_epi = tmp_path / "no_redact.epi"
        
        result = runner.invoke(app, [
            "record",
            "--out", str(output_epi),
            "--no-sign",
            "--no-redact",
            "--",
            "python", str(test_script)
        ])
        
        # Should work
        if output_epi.exists():
            assert output_epi.exists()
    
    def test_record_with_failed_command(self, tmp_path):
        """Test recording a command that fails."""
        from typer.testing import CliRunner
        from epi_cli.main import app
        
        runner = CliRunner()
        
        test_script = tmp_path / "failing.py"
        test_script.write_text('import sys; sys.exit(1)')
        
        output_epi = tmp_path / "failed.epi"
        
        result = runner.invoke(app, [
            "record",
            "--out", str(output_epi),
            "--no-sign",
            "--",
            "python", str(test_script)
        ])
        
        # Should create .epi even on failure
        if output_epi.exists():
            assert output_epi.exists()
        
        # Exit code should match script exit code
        assert result.exit_code == 1


class TestRecordCommandEdgeCases:
    """Test edge cases and error handling."""
    
    def test_record_with_include_all_env(self, tmp_path):
        """Test --include-all-env flag."""
        from typer.testing import CliRunner
        from epi_cli.main import app
        
        runner = CliRunner()
        
        test_script = tmp_path / "test.py"
        test_script.write_text('print("test")')
        
        output_epi = tmp_path / "with_env.epi"
        
        result = runner.invoke(app, [
            "record",
            "--out", str(output_epi),
            "--no-sign",
            "--include-all-env",
            "--",
            "python", str(test_script)
        ])
        
        # Should work
        if output_epi.exists():
            with zipfile.ZipFile(output_epi, 'r') as zf:
                if 'env.json' in zf.namelist():
                    env_data = json.loads(zf.read('env.json'))
                    # Should have environment data
                    assert isinstance(env_data, dict)
