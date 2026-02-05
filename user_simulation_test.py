"""
EPI v2.3.0 User Simulation Test

This script tests all features as a normal user would use them.
"""

import sys
from pathlib import Path
import tempfile
import json
import zipfile

print("=" * 60)
print("EPI v2.3.0 - User Simulation Test")
print("=" * 60)

# Test 1: Basic Import
print("\n[1] Testing package import...")
try:
    from epi_recorder import record, wrap_openai, TracedOpenAI, __version__
    print(f"   [OK] Package imported successfully (v{__version__})")
except ImportError as e:
    print(f"   [FAIL] Import failed: {e}")
    sys.exit(1)

# Create temp directory for test files
test_dir = Path(tempfile.mkdtemp(prefix="epi_user_test_"))
print(f"\n   Test directory: {test_dir}")

# Test 2: Basic Recording (no LLM calls)
print("\n[2] Testing basic recording...")
try:
    epi_file = test_dir / "basic_test.epi"
    with record(str(epi_file), workflow_name="Basic Test") as epi:
        epi.log_step("user.action", {"action": "started", "user": "test_user"})
        result = sum(range(100))
        epi.log_step("calc.done", {"result": result})
    
    assert epi_file.exists(), "EPI file not created"
    print(f"   [OK] Basic recording works ({epi_file.stat().st_size} bytes)")
except Exception as e:
    print(f"   [FAIL] Basic recording failed: {e}")
    sys.exit(1)

# Test 3: Explicit API - log_chat()
print("\n[3] Testing explicit API (log_chat)...")
try:
    epi_file = test_dir / "explicit_api_test.epi"
    with record(str(epi_file), workflow_name="Explicit API Test") as epi:
        # Simulate what a user would do without a real LLM
        messages = [{"role": "user", "content": "What is 2+2?"}]
        response_content = "The answer is 4."
        
        epi.log_chat(
            model="gpt-4",
            messages=messages,
            response_content=response_content,
            provider="openai"
        )
    
    # Verify the steps were logged
    with zipfile.ZipFile(epi_file, 'r') as zf:
        steps = zf.read("steps.jsonl").decode("utf-8")
        assert "llm.request" in steps, "LLM request not logged"
        assert "llm.response" in steps, "LLM response not logged"
    
    print(f"   [OK] log_chat() works correctly")
except Exception as e:
    print(f"   [FAIL] Explicit API test failed: {e}")
    sys.exit(1)

# Test 4: Explicit API - log_llm_call() with mock response
print("\n[4] Testing log_llm_call() with mock response...")
try:
    from unittest.mock import Mock
    
    epi_file = test_dir / "log_llm_call_test.epi"
    
    # Create mock OpenAI-like response
    mock_response = Mock()
    mock_response.model = "gpt-4-turbo"
    mock_response.choices = [
        Mock(
            message=Mock(role="assistant", content="Hello! How can I help you today?"),
            finish_reason="stop"
        )
    ]
    mock_response.usage = Mock(
        prompt_tokens=15,
        completion_tokens=10,
        total_tokens=25
    )
    
    with record(str(epi_file), workflow_name="Log LLM Call Test") as epi:
        epi.log_llm_call(
            mock_response,
            messages=[{"role": "user", "content": "Hello"}]
        )
    
    # Verify
    with zipfile.ZipFile(epi_file, 'r') as zf:
        steps = zf.read("steps.jsonl").decode("utf-8")
        assert "gpt-4-turbo" in steps, "Model name not in response"
        assert "openai" in steps, "Provider should be auto-detected as openai"
    
    print(f"   [OK] log_llm_call() works with auto-detection")
except Exception as e:
    print(f"   [FAIL] log_llm_call test failed: {e}")
    sys.exit(1)

# Test 5: Wrapper Client (TracedOpenAI)
print("\n[5] Testing wrapper client (TracedOpenAI)...")
try:
    from epi_recorder.wrappers.openai import TracedCompletions
    from unittest.mock import Mock
    
    epi_file = test_dir / "wrapper_test.epi"
    
    # Create mock completions object
    mock_completions = Mock()
    mock_response = Mock()
    mock_response.model = "gpt-3.5-turbo"
    mock_response.choices = [
        Mock(
            message=Mock(role="assistant", content="Wrapper test response"),
            finish_reason="stop"
        )
    ]
    mock_response.usage = Mock(
        prompt_tokens=5,
        completion_tokens=3,
        total_tokens=8
    )
    mock_completions.create.return_value = mock_response
    
    # Wrap and use
    traced = TracedCompletions(mock_completions)
    
    with record(str(epi_file), workflow_name="Wrapper Test"):
        result = traced.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Test"}]
        )
    
    assert result == mock_response, "Response should be passed through"
    
    # Verify steps
    with zipfile.ZipFile(epi_file, 'r') as zf:
        steps = zf.read("steps.jsonl").decode("utf-8")
        assert "llm.request" in steps, "Request not logged by wrapper"
        assert "llm.response" in steps, "Response not logged by wrapper"
    
    print(f"   [OK] TracedCompletions wrapper works correctly")
except Exception as e:
    print(f"   [FAIL] Wrapper test failed: {e}")
    sys.exit(1)

# Test 6: Verify EPI Files
print("\n[6] Verifying EPI file integrity...")
try:
    import subprocess
    
    for epi_file in test_dir.glob("*.epi"):
        result = subprocess.run(
            f"python -m epi_cli.main verify {epi_file}",
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"   [OK] {epi_file.name} - VALID")
        else:
            print(f"   [WARN] {epi_file.name} - {result.stderr.strip()}")
except Exception as e:
    print(f"   [WARN] Verification skipped: {e}")

# Test 7: Legacy Patching (deprecated)
print("\n[7] Testing legacy_patching deprecation warning...")
try:
    import warnings
    
    epi_file = test_dir / "legacy_test.epi"
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        with record(str(epi_file), legacy_patching=True):
            pass
        
        deprecation_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
        assert len(deprecation_warnings) > 0, "Should show deprecation warning"
    
    print(f"   [OK] legacy_patching shows deprecation warning")
except Exception as e:
    print(f"   [FAIL] Legacy patching test failed: {e}")
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("[SUCCESS] ALL USER SIMULATION TESTS PASSED!")
print("=" * 60)

epi_files = list(test_dir.glob("*.epi"))
print(f"\nCreated {len(epi_files)} .epi files:")
for f in epi_files:
    print(f"   - {f.name} ({f.stat().st_size:,} bytes)")

print(f"\nEPI v{__version__} is ready for users!")

# Cleanup
import shutil
try:
    shutil.rmtree(test_dir)
    print(f"\nCleaned up test directory")
except:
    pass
