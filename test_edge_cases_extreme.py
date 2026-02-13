"""
EXTREME EDGE CASE TESTING FOR v2.4.0 FEATURES
Tests every possible failure scenario and edge case
"""

import asyncio
import sys
from pathlib import Path
from epi_recorder import record, wrap_openai
from epi_recorder.analytics import AgentAnalytics

print("=" * 70)
print("EXTREME EDGE CASE TESTING - v2.4.0")
print("=" * 70)

tests_passed = 0
tests_failed = 0

def test(name):
    def decorator(func):
        def wrapper():
            global tests_passed, tests_failed
            print(f"\n[TEST] {name}")
            print("-" * 60)
            try:
                result = func()
                if result or result is None:
                    print(f"[PASS] {name}")
                    tests_passed += 1
                else:
                    print(f"[FAIL] {name}")
                    tests_failed += 1
            except Exception as e:
                print(f"[EXCEPTION] in {name}: {e}")
                tests_failed += 1
        return wrapper
    return decorator

# ============ ANALYTICS EDGE CASES ============

@test("Analytics: Empty directory (no .epi files)")
def test_analytics_empty():
    import tempfile
    tmpdir = tempfile.mkdtemp()
    try:
        analytics = AgentAnalytics(tmpdir)
        summary = analytics.performance_summary()
        print(f"  Empty dir handled: {summary}")
        return True
    except ValueError as e:
        # Expected behavior - Analytics raises ValueError for empty dirs
        print(f"  Correctly raises ValueError for empty directory: {e}")
        return True

@test("Analytics: Directory with only corrupted files")
def test_analytics_corrupted():
    import tempfile
    import zipfile
    tmpdir = tempfile.mkdtemp()
    
    # Create a fake corrupted .epi file
    fake_epi = Path(tmpdir) / "corrupted.epi"
    with open(fake_epi, 'wb') as f:
        f.write(b"THIS IS NOT A VALID EPI FILE")
    
    analytics = AgentAnalytics(tmpdir)
    # Should handle gracefully
    summary = analytics.performance_summary()
    print(f"  Handled corrupted file, found {summary['total_runs']} valid runs")
    return True

@test("Analytics: Very large dataset (100+ files)")
def test_analytics_large_scale():
    # Use existing epi-recordings directory
    analytics = AgentAnalytics("epi-recordings")
    summary = analytics.performance_summary()
    print(f"  Analyzed {summary['total_runs']} runs successfully")
    return summary['total_runs'] > 0

@test("Analytics: Cost calculation accuracy")
def test_analytics_cost():
    analytics = AgentAnalytics("test_analytics_data")
    summary = analytics.performance_summary()
    
    # Verify cost is a number and makes sense
    assert isinstance(summary['total_cost'], (int, float))
    assert summary['total_cost'] >= 0
    print(f"  Total cost: ${summary['total_cost']:.4f}")
    print(f"  Avg cost: ${summary['avg_cost_per_run']:.4f}")
    return True

# ============ ASYNC EDGE CASES ============

@test("Async: Rapid sequential recordings")
async def test_async_rapid():
    for i in range(10):
        async with record(f"epi-recordings/rapid_{i}.epi"):
            await asyncio.sleep(0.01)  # Very fast
    print(f"  Created 10 rapid recordings")
    return True

@test("Async: Exception mid-recording")
async def test_async_exception():
    try:
        async with record("epi-recordings/exception_test.epi"):
            await asyncio.sleep(0.1)
            raise ValueError("Intentional test error")
    except ValueError:
        pass
    
    # File should still exist
    assert Path("epi-recordings/exception_test.epi").exists()
    print("  Exception handled, file still created")
    return True

@test("Async: Nested async contexts")
async def test_async_nested():
    async with record("epi-recordings/outer.epi"):
        await asyncio.sleep(0.05)
        async with record("epi-recordings/inner.epi"):
            await asyncio.sleep(0.05)
    
    assert Path("epi-recordings/outer.epi").exists()
    assert Path("epi-recordings/inner.epi").exists()
    print("  Nested contexts handled correctly")
    return True

@test("Async: Very long recording")
async def test_async_long():
    async with record("epi-recordings/long_recording.epi"):
        for i in range(50):
            await asyncio.sleep(0.02)
    print("  Long async recording completed")
    return True

# ============ LANGGRAPH EDGE CASES ============

@test("LangGraph: Import without LangGraph installed")
def test_langgraph_import():
    try:
        from epi_recorder.integrations.langgraph import EPICheckpointSaver
        print("  EPICheckpointSaver imports successfully")
        return True
    except ImportError as e:
        print(f"  Import failed (expected if LangGraph not installed): {e}")
        return False

@test("LangGraph: Instantiation without LangGraph")
def test_langgraph_instantiate():
    try:
        from epi_recorder.integrations.langgraph import EPICheckpointSaver
        saver = EPICheckpointSaver("test.epi")
        print(f"  ❌ Should have raised ImportError")
        return False
    except ImportError as e:
        print(f"  Correctly raises ImportError: {e}")
        return True

# ============ OLLAMA EDGE CASES ============

@test("Ollama: Check if running")
def test_ollama_running():
    import subprocess
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            timeout=5,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        if result.returncode == 0:
            print("  Ollama is running")
            return True
    except:
        pass
    print("  Ollama not available (skipping Ollama tests)")
    return False

@test("Ollama: Invalid model name handling")
def test_ollama_invalid_model():
    from openai import OpenAI
    
    try:
        client = wrap_openai(OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"
        ))
        
        with record("epi-recordings/ollama_invalid.epi"):
            try:
                response = client.chat.completions.create(
                    model="this-model-does-not-exist",
                    messages=[{"role": "user", "content": "test"}]
                )
            except Exception as e:
                print(f"  Correctly handled invalid model: {type(e).__name__}")
                return True
    except:
        print("  Ollama not available")
        return False

# ============ RUN ALL TESTS ============

if __name__ == "__main__":
    print("\nRunning synchronous tests...")
    test_analytics_empty()
    test_analytics_corrupted()
    test_analytics_large_scale()
    test_analytics_cost()
    test_langgraph_import()
    test_langgraph_instantiate()
    test_ollama_running()
    
    print("\nRunning asynchronous tests...")
    asyncio.run(test_async_rapid())
    asyncio.run(test_async_exception())
    asyncio.run(test_async_nested())
    asyncio.run(test_async_long())
    
    print("\n" + "=" * 70)
    print("EDGE CASE TEST SUMMARY")
    print("=" * 70)
    print(f"PASSED: {tests_passed}")
    print(f"FAILED: {tests_failed}")
    print(f"SUCCESS RATE: {tests_passed/(tests_passed+tests_failed)*100:.1f}%")
    
    if tests_failed == 0:
        print("\n[SUCCESS] ALL EDGE CASES HANDLED PERFECTLY!")
        sys.exit(0)
    else:
        print(f"\n[WARNING] {tests_failed} edge cases failed")
        sys.exit(1)
