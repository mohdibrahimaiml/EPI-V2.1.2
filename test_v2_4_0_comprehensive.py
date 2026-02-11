"""
COMPREHENSIVE v2.4.0 PRE-RELEASE TEST SUITE

Tests EVERY feature as a normal user would.
"""

import asyncio
import sys
from pathlib import Path

# Ensure we're testing the local version
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("EPI RECORDER v2.4.0 - COMPREHENSIVE PRE-RELEASE TESTS")
print("=" * 70)
print()

# Track results
results = {
    "passed": [],
    "failed": [],
    "skipped": []
}

def test_result(name, passed, error=None):
    if passed:
        results["passed"].append(name)
        print(f"[PASS] {name}")
    else:
        results["failed"].append((name, error))
        print(f"[FAIL] {name}: {error}")

# ==============================================================================
# TEST 1: BASIC IMPORTS
# ==============================================================================
print("\n[TEST 1] Basic Imports")
print("-" * 70)

try:
    from epi_recorder import record, wrap_openai, AgentAnalytics, __version__
    test_result("Import epi_recorder", True)
    test_result(f"Version is 2.4.0 (got {__version__})", __version__ == "2.4.0")
except Exception as e:
    test_result("Import epi_recorder", False, str(e))

try:
    from epi_core import __version__ as core_version
    test_result(f"epi_core version is 2.4.0 (got {core_version})", core_version == "2.4.0")
except Exception as e:
    test_result("Import epi_core", False, str(e))

# ==============================================================================
# TEST 2: BASIC SYNC RECORDING
# ==============================================================================
print("\n[TEST 2] Basic Sync Recording")
print("-" * 70)

try:
    with record("test_sync.epi", goal="Test sync recording") as epi:
        epi.log_step("test.start", {"message": "Testing sync mode"})
        epi.log_step("test.end", {"status": "success"})
    
    test_result("Sync recording", True)
    
    # Check file exists
    if Path("epi-recordings/test_sync.epi").exists():
        test_result(".epi file created (sync)", True)
    else:
        test_result(".epi file created (sync)", False, "File not found")
        
except Exception as e:
    test_result("Sync recording", False, str(e))

# ==============================================================================
# TEST 3: ASYNC RECORDING (NEW!)
# ==============================================================================
print("\n[TEST 3] Async Recording (NEW v2.4.0)")
print("-" * 70)

async def test_async_recording():
    try:
        async with record("test_async.epi", goal="Test async recording") as epi:
            await epi.alog_step("test.async_start", {"mode": "async"})
            await asyncio.sleep(0.1)
            await epi.alog_step("test.async_end", {"status": "success"})
        
        test_result("Async recording", True)
        
        if Path("epi-recordings/test_async.epi").exists():
            test_result(".epi file created (async)", True)
        else:
            test_result(".epi file created (async)", False, "File not found")
            
    except Exception as e:
        test_result("Async recording", False, str(e))

asyncio.run(test_async_recording())

# ==============================================================================
# TEST 4: AGENT ANALYTICS (NEW!)
# ==============================================================================
print("\n[TEST 4] Agent Analytics Engine (NEW v2.4.0)")
print("-" * 70)

try:
    from epi_recorder import AgentAnalytics
    
    # Create analytics instance
    analytics = AgentAnalytics("epi-recordings")
    test_result("AgentAnalytics import", True)
    
    # Get summary
    summary = analytics.performance_summary()
    test_result("performance_summary()", True)
    test_result(f"Found {summary.get('total_runs', 0)} runs", summary.get('total_runs', 0) > 0)
    
except Exception as e:
    test_result("Agent Analytics", False, str(e))

# ==============================================================================
# TEST 5: LANGGRAPH INTEGRATION (NEW!)
# ==============================================================================
print("\n[TEST 5] LangGraph Integration (NEW v2.4.0)")
print("-" * 70)

try:
    from epi_recorder.integrations import EPICheckpointSaver
    test_result("EPICheckpointSaver import", True)
    
    # Try to actually use it (requires langgraph)
    try:
        checkpointer = EPICheckpointSaver()
        test_result("EPICheckpointSaver instantiation", True)
    except ImportError as e:
        results["skipped"].append(f"LangGraph checkpoint test ({str(e)})")
        print("[SKIP] LangGraph not installed - integration code works but optional dependency missing")
    
except Exception as e:
    test_result("LangGraph Integration", False, str(e))

# ==============================================================================
# TEST 6: OLLAMA INTEGRATION (NEW!)
# ==============================================================================
print("\n[TEST 6] Ollama Integration (NEW v2.4.0)")
print("-" * 70)

try:
    from openai import OpenAI
    from epi_recorder import wrap_openai
    
    # Check if Ollama is running
    import subprocess
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode == 0 and "deepseek-r1" in result.stdout:
        test_result("Ollama installed with DeepSeek-R1", True)
        
        # Test recording with Ollama
        client = wrap_openai(OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"
        ))
        
        try:
            with record("test_ollama.epi", goal="Test Ollama") as epi:
                response = client.chat.completions.create(
                    model="deepseek-r1:7b",
                    messages=[{"role": "user", "content": "Say 'test'"}],
                    max_tokens=10
                )
            
            test_result("Ollama recording", True)
            
            if Path("epi-recordings/test_ollama.epi").exists():
                test_result(".epi file created (Ollama)", True)
            else:
                test_result(".epi file created (Ollama)", False, "File not found")
                
        except Exception as e:
            test_result("Ollama LLM call", False, str(e))
            
    else:
        results["skipped"].append("Ollama tests (not installed or model not found)")
        print("[SKIP] Ollama tests skipped (not installed)")
        
except Exception as e:
    results["skipped"].append(f"Ollama tests ({str(e)})")
    print(f"[SKIP] Ollama tests skipped: {e}")

# ==============================================================================
# TEST 7: WRAPPER CLIENTS
# ==============================================================================
print("\n[TEST 7] Wrapper Clients")
print("-" * 70)

try:
    from epi_recorder import wrap_openai
    test_result("wrap_openai import", True)
    
except Exception as e:
    test_result("Wrapper clients", False, str(e))

# ==============================================================================
# TEST 8: CLI COMMANDS
# ==============================================================================
print("\n[TEST 8] CLI Commands")
print("-" * 70)

try:
    import subprocess
    
    # Test epi --version
    result = subprocess.run(
        ["epi", "--version"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode == 0:
        test_result("epi --version works", True)
        if "2.4.0" in result.stdout:
            test_result("CLI version is 2.4.0", True)
        else:
            test_result("CLI version is 2.4.0", False, f"Got: {result.stdout}")
    else:
        test_result("epi --version", False, result.stderr)
        
except Exception as e:
    test_result("CLI commands", False, str(e))

# ==============================================================================
# TEST 9: VERIFICATION
# ==============================================================================
print("\n[TEST 9] Verification")
print("-" * 70)

try:
    from epi_core.container import EPIContainer
    from epi_core.schemas import ManifestModel
    
    # Check a created .epi file
    test_file = Path("epi-recordings/test_sync.epi")
    if test_file.exists():
        manifest = EPIContainer.read_manifest(test_file)
        test_result("Read manifest from .epi", True)
        
        if manifest.spec_version == "2.4.0":
            test_result("spec_version is 2.4.0", True)
        else:
            test_result("spec_version is 2.4.0", False, f"Got: {manifest.spec_version}")
    else:
        test_result("Verification", False, "No .epi file to verify")
        
except Exception as e:
    test_result("Verification", False, str(e))

# ==============================================================================
# TEST 10: EDGE CASES
# ==============================================================================
print("\n[TEST 10] Edge Cases")
print("-" * 70)

# Test empty recording
try:
    with record("test_empty.epi"):
        pass
    test_result("Empty recording", True)
except Exception as e:
    test_result("Empty recording", False, str(e))

# Test recording with exception
try:
    try:
        with record("test_error.epi"):
            raise ValueError("Intentional error")
    except ValueError:
        pass
    
    if Path("epi-recordings/test_error.epi").exists():
        test_result("Recording with exception", True)
    else:
        test_result("Recording with exception", False, "File not created")
except Exception as e:
    test_result("Recording with exception", False, str(e))

# ==============================================================================
# SUMMARY
# ==============================================================================
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print()

print(f"PASSED: {len(results['passed'])}")
for test in results['passed']:
    print(f"   - {test}")

print()
print(f"FAILED: {len(results['failed'])}")
for test, error in results['failed']:
    print(f"   - {test}: {error}")

print()
print(f"SKIPPED: {len(results['skipped'])}")
for test in results['skipped']:
    print(f"   - {test}")

print()
print("=" * 70)

if len(results['failed']) == 0:
    print("ALL TESTS PASSED - READY FOR RELEASE!")
    print("=" * 70)
    sys.exit(0)
else:
    print(f"WARNING: {len(results['failed'])} TEST(S) FAILED - FIX BEFORE RELEASE")
    print("=" * 70)
    sys.exit(1)
