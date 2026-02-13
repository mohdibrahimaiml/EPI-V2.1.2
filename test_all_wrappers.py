"""
COMPREHENSIVE WRAPPER TESTING
Tests both OpenAI and Anthropic wrappers with mock data
"""

import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock

print("="*70)
print("COMPREHENSIVE WRAPPER TESTS")
print("="*70)
print()

passed = 0
failed = 0

def test_result(name, success, error=None):
    global passed, failed
    if success:
        print(f"[PASS] {name}")
        passed += 1
    else:
        print(f"[FAIL] {name}")
        if error:
            print(f"  Error: {error}")
        failed += 1

# ============ TEST 1: IMPORTS ============
print("[TEST 1] Import both wrappers")
print("-"*70)
try:
    from epi_recorder.wrappers import wrap_openai, wrap_anthropic
    from epi_recorder import record
    test_result("Import wrappers", True)
except ImportError as e:
    test_result("Import wrappers", False, str(e))
    sys.exit(1)

print()

# ============ TEST 2: OPENAI WRAPPER STRUCTURE ============
print("[TEST 2] OpenAI wrapper structure")
print("-"*70)

# Create mock OpenAI client
mock_openai = Mock()
mock_openai.chat = Mock()
mock_openai.chat.completions = Mock()

wrapped_openai = wrap_openai(mock_openai)

test_result("OpenAI wrapper created", hasattr(wrapped_openai, 'chat'))
test_result("OpenAI has chat.completions", hasattr(wrapped_openai.chat, 'completions'))
test_result("OpenAI has create method", hasattr(wrapped_openai.chat.completions, 'create'))

print()

# ============ TEST 3: ANTHROPIC WRAPPER STRUCTURE ============
print("[TEST 3] Anthropic wrapper structure")  
print("-"*70)

# Create mock Anthropic client
mock_anthropic = Mock()
mock_anthropic.messages = Mock()

wrapped_anthropic = wrap_anthropic(mock_anthropic)

test_result("Anthropic wrapper created", hasattr(wrapped_anthropic, 'messages'))
test_result("Anthropic has messages.create", hasattr(wrapped_anthropic.messages, 'create'))
test_result("Anthropic has messages.stream", hasattr(wrapped_anthropic.messages, 'stream'))

print()

# ============ TEST 4: OPENAI MOCK CALL ============
print("[TEST 4] OpenAI wrapper with mock response")
print("-"*70)

# Setup mock response
mock_response = Mock()
mock_response.choices = [Mock()]
mock_response.choices[0].message = Mock(role="assistant", content="Hello!")
mock_response.choices[0].finish_reason = "stop"
mock_response.usage = Mock(prompt_tokens=10, completion_tokens=5, total_tokens=15)

mock_openai.chat.completions.create = Mock(return_value=mock_response)
wrapped_openai = wrap_openai(mock_openai)

try:
    # Test WITHOUT recording context (should work, just not log)
    response = wrapped_openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "test"}]
    )
    test_result("OpenAI call without record()", response is not None)
except Exception as e:
    test_result("OpenAI call without record()", False, str(e))

try:
    # Test WITH recording context
    with record("test_openai_wrapper.epi"):
        response = wrapped_openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}]
        )
    test_result("OpenAI call with record()", response is not None)
    test_result("OpenAI .epi file created", Path("epi-recordings/test_openai_wrapper.epi").exists())
except Exception as e:
    test_result("OpenAI call with record()", False, str(e))

print()

# ============ TEST 5: ANTHROPIC MOCK CALL ============
print("[TEST 5] Anthropic wrapper with mock response")
print("-"*70)

# Setup mock response
mock_content = Mock()
mock_content.text = "Hello from Claude!"
mock_anthropic_response = Mock()
mock_anthropic_response.content = [mock_content]
mock_anthropic_response.role = "assistant"
mock_anthropic_response.stop_reason = "end_turn"
mock_anthropic_response.usage = Mock(input_tokens=10, output_tokens=5)

mock_anthropic.messages.create = Mock(return_value=mock_anthropic_response)
wrapped_anthropic = wrap_anthropic(mock_anthropic)

try:
    # Test WITHOUT recording context
    response = wrapped_anthropic.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": "test"}]
    )
    test_result("Anthropic call without record()", response is not None)
except Exception as e:
    test_result("Anthropic call without record()", False, str(e))

try:
    # Test WITH recording context
    with record("test_anthropic_wrapper.epi"):
        response = wrapped_anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": "test"}]
        )
    test_result("Anthropic call with record()", response is not None)
    test_result("Anthropic .epi file created", Path("epi-recordings/test_anthropic_wrapper.epi").exists())
except Exception as e:
    test_result("Anthropic call with record()", False, str(e))

print()

# ============ TEST 6: ERROR HANDLING ============
print("[TEST 6] Error handling")
print("-"*70)

# OpenAI error
mock_openai.chat.completions.create = Mock(side_effect=Exception("API Error"))
wrapped_openai = wrap_openai(mock_openai)

try:
    with record("test_openai_error.epi"):
        try:
            response = wrapped_openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "test"}]
            )
        except Exception:
            pass  # Expected
    
    # File should still be created
    test_result("OpenAI error creates .epi", Path("epi-recordings/test_openai_error.epi").exists())
except Exception as e:
    test_result("OpenAI error handling", False, str(e))

# Anthropic error
mock_anthropic.messages.create = Mock(side_effect=Exception("API Error"))
wrapped_anthropic = wrap_anthropic(mock_anthropic)

try:
    with record("test_anthropic_error.epi"):
        try:
            response = wrapped_anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": "test"}]
            )
        except Exception:
            pass  # Expected
    
    test_result("Anthropic error creates .epi", Path("epi-recordings/test_anthropic_error.epi").exists())
except Exception as e:
    test_result("Anthropic error handling", False, str(e))

print()

# ============ TEST 7: VERIFY .EPI FILES ============
print("[TEST 7] Verify created .epi files")
print("-"*70)

import zipfile
import json

def verify_epi_file(filename):
    """Check if .epi file is valid"""
    filepath = Path(f"epi-recordings/{filename}")
    if not filepath.exists():
        return False, "File not found"
    
    try:
        with zipfile.ZipFile(filepath, 'r') as zf:
            # Check required files
            if 'manifest.json' not in zf.namelist():
                return False, "Missing manifest.json"
            if 'steps.jsonl' not in zf.namelist():
                return False, "Missing steps.jsonl"
            
            # Verify manifest
            manifest_data = zf.read('manifest.json')
            manifest = json.loads(manifest_data)
            
            return True, f"Valid (spec {manifest.get('spec_version', 'unknown')})"
    except Exception as e:
        return False, str(e)

files_to_verify = [
    "test_openai_wrapper.epi",
    "test_anthropic_wrapper.epi",
    "test_openai_error.epi",
    "test_anthropic_error.epi"
]

for filename in files_to_verify:
    valid, msg = verify_epi_file(filename)
    test_result(f"Verify {filename}", valid, None if valid else msg)

print()

# ============ SUMMARY ============
print("="*70)
print("TEST SUMMARY")
print("="*70)
print()
print(f"PASSED: {passed}")
print(f"FAILED: {failed}")
print(f"SUCCESS RATE: {passed/(passed+failed)*100:.1f}%")
print()

if failed == 0:
    print("All wrappers working perfectly!")
    sys.exit(0)
else:
    print(f"{failed} tests failed")
    sys.exit(1)
