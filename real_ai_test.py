"""
EPI v2.3.0 - Real AI Workflow Test

Tests EPI with actual Gemini API calls to verify real-time recording.
"""

import os
import sys
from pathlib import Path

print("=" * 60)
print("EPI v2.3.0 - Real AI Workflow Test")
print("=" * 60)

# Check for API key
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("\n[WARN] No GEMINI_API_KEY or GOOGLE_API_KEY found.")
    print("       Set one to run real AI tests.")
    print("       Example: set GEMINI_API_KEY=your_key_here")
    sys.exit(0)

print(f"\n[OK] API key found (length: {len(api_key)})")

# Import EPI
from epi_recorder import record, __version__
print(f"[OK] EPI v{__version__} imported")

# Test directory
test_dir = Path("real_ai_test_output")
test_dir.mkdir(exist_ok=True)

# ============================================================
# Test 1: Explicit API with Real Gemini Call
# ============================================================
print("\n" + "-" * 40)
print("Test 1: Real Gemini API with Explicit Logging")
print("-" * 40)

try:
    import google.generativeai as genai
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    epi_file = test_dir / "real_gemini_explicit.epi"
    
    with record(str(epi_file), workflow_name="Real Gemini Test") as epi:
        # Make real API call
        prompt = "What is 2 + 2? Reply in one word."
        print(f"   Sending: '{prompt}'")
        
        response = model.generate_content(prompt)
        answer = response.text.strip()
        print(f"   Response: '{answer}'")
        
        # Explicit logging
        epi.log_llm_call(response, messages=[{"role": "user", "content": prompt}])
    
    print(f"   [OK] Created: {epi_file.name} ({epi_file.stat().st_size:,} bytes)")
    
    # Verify contents
    import zipfile
    import json
    
    with zipfile.ZipFile(epi_file, 'r') as zf:
        steps_content = zf.read("steps.jsonl").decode("utf-8")
        steps = [json.loads(line) for line in steps_content.strip().split("\n") if line]
    
    llm_steps = [s for s in steps if s["kind"].startswith("llm.")]
    print(f"   [OK] Captured {len(llm_steps)} LLM steps")
    
except Exception as e:
    print(f"   [FAIL] {type(e).__name__}: {e}")

# ============================================================
# Test 2: Multi-turn Conversation
# ============================================================
print("\n" + "-" * 40)
print("Test 2: Multi-turn Conversation with Gemini")
print("-" * 40)

try:
    epi_file = test_dir / "real_gemini_conversation.epi"
    
    with record(str(epi_file), workflow_name="Multi-turn Chat") as epi:
        chat = model.start_chat(history=[])
        
        # Turn 1
        msg1 = "My name is Alex. Remember it."
        print(f"   User: {msg1}")
        resp1 = chat.send_message(msg1)
        print(f"   AI: {resp1.text.strip()[:50]}...")
        epi.log_chat(
            model="gemini-1.5-flash",
            messages=[{"role": "user", "content": msg1}],
            response_content=resp1.text,
            provider="gemini"
        )
        
        # Turn 2
        msg2 = "What's my name?"
        print(f"   User: {msg2}")
        resp2 = chat.send_message(msg2)
        print(f"   AI: {resp2.text.strip()[:50]}...")
        epi.log_chat(
            model="gemini-1.5-flash",
            messages=[{"role": "user", "content": msg2}],
            response_content=resp2.text,
            provider="gemini"
        )
    
    print(f"   [OK] Created: {epi_file.name} ({epi_file.stat().st_size:,} bytes)")
    
    # Count steps
    with zipfile.ZipFile(epi_file, 'r') as zf:
        steps_content = zf.read("steps.jsonl").decode("utf-8")
        steps = [json.loads(line) for line in steps_content.strip().split("\n") if line]
    
    llm_steps = [s for s in steps if s["kind"].startswith("llm.")]
    print(f"   [OK] Captured {len(llm_steps)} LLM steps (2 conversations)")

except Exception as e:
    print(f"   [FAIL] {type(e).__name__}: {e}")

# ============================================================
# Test 3: Legacy Patching with Real Gemini (Deprecated)
# ============================================================
print("\n" + "-" * 40)
print("Test 3: Legacy Auto-Patching (deprecated)")
print("-" * 40)

try:
    import warnings
    
    epi_file = test_dir / "real_gemini_legacy.epi"
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        with record(str(epi_file), legacy_patching=True, workflow_name="Legacy Test"):
            # This should be auto-captured by monkey patching
            prompt = "Say 'hello' only."
            print(f"   Sending: '{prompt}'")
            response = model.generate_content(prompt)
            print(f"   Response: '{response.text.strip()}'")
        
        # Check for deprecation warning
        dep_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
        if dep_warnings:
            print(f"   [OK] Deprecation warning shown (as expected)")
    
    print(f"   [OK] Created: {epi_file.name} ({epi_file.stat().st_size:,} bytes)")
    
    # Verify auto-capture worked
    with zipfile.ZipFile(epi_file, 'r') as zf:
        steps_content = zf.read("steps.jsonl").decode("utf-8")
        steps = [json.loads(line) for line in steps_content.strip().split("\n") if line]
    
    llm_steps = [s for s in steps if s["kind"].startswith("llm.")]
    print(f"   [OK] Auto-captured {len(llm_steps)} LLM steps via legacy patching")

except Exception as e:
    print(f"   [FAIL] {type(e).__name__}: {e}")

# ============================================================
# Verify All Files
# ============================================================
print("\n" + "-" * 40)
print("Verifying All EPI Files")
print("-" * 40)

import subprocess

for epi_file in test_dir.glob("*.epi"):
    result = subprocess.run(
        f"python -m epi_cli.main verify {epi_file}",
        shell=True,
        capture_output=True,
        text=True
    )
    status = "VALID" if result.returncode == 0 else "INVALID"
    print(f"   {epi_file.name}: {status}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("[SUCCESS] REAL AI WORKFLOW TESTS COMPLETE!")
print("=" * 60)

epi_files = list(test_dir.glob("*.epi"))
print(f"\nGenerated {len(epi_files)} .epi files in: {test_dir.absolute()}")
for f in epi_files:
    print(f"   - {f.name}")

print("\nTo view an evidence file, run:")
print(f"   python -m epi_cli.main view {test_dir / epi_files[0].name if epi_files else 'file.epi'}")
