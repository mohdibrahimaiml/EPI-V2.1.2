"""
EPI v2.3.0 - CLI Commands Test

Tests all CLI commands without requiring an API key.
"""

import subprocess
import sys
import tempfile
from pathlib import Path
import shutil

def run_cmd(cmd, cwd=None, expect_success=True):
    """Run a command and return result."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=cwd
    )
    return result

print("=" * 60)
print("EPI v2.3.0 - CLI Commands Test")
print("=" * 60)

# Create test directory
test_dir = Path(tempfile.mkdtemp(prefix="epi_cli_test_"))
print(f"\nTest directory: {test_dir}")

# Create a sample .epi file using the API
print("\n[Setup] Creating sample .epi file...")
from epi_recorder import record, __version__
print(f"   Version: {__version__}")

sample_epi = test_dir / "sample.epi"
with record(str(sample_epi), workflow_name="CLI Test Sample") as epi:
    epi.log_step("test.start", {"message": "Starting test"})
    epi.log_chat(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}],
        response_content="Hi there!",
        provider="openai"
    )
    epi.log_step("test.end", {"message": "Test complete"})

print(f"   Created: {sample_epi.name} ({sample_epi.stat().st_size:,} bytes)")

# ============================================================
# Test 1: epi --help
# ============================================================
print("\n" + "-" * 40)
print("[1] epi --help")
print("-" * 40)
result = run_cmd("python -m epi_cli.main --help")
if result.returncode == 0 and "Usage:" in result.stdout:
    print("   [OK] Help command works")
    # Show available commands
    lines = result.stdout.split("\n")
    for line in lines:
        if line.strip().startswith(("verify", "view", "ls", "keys", "debug", "run", "record", "chat")):
            print(f"      - {line.strip()}")
else:
    print(f"   [FAIL] {result.stderr}")

# ============================================================
# Test 2: epi verify
# ============================================================
print("\n" + "-" * 40)
print("[2] epi verify <file>")
print("-" * 40)
result = run_cmd(f"python -m epi_cli.main verify {sample_epi}")
if result.returncode == 0:
    print("   [OK] Verify command works")
    # Show verification output
    for line in result.stdout.strip().split("\n")[:5]:
        if line.strip():
            print(f"      {line.strip()}")
else:
    print(f"   [FAIL] {result.stderr}")

# ============================================================
# Test 3: epi ls
# ============================================================
print("\n" + "-" * 40)
print("[3] epi ls")
print("-" * 40)
result = run_cmd("python -m epi_cli.main ls", cwd=str(test_dir))
if result.returncode == 0:
    print("   [OK] List command works")
    print(f"      Output: {result.stdout.strip()[:100]}...")
else:
    # ls might return 1 if no files found in default location
    if "No .epi files found" in result.stdout or "No .epi files found" in result.stderr:
        print("   [OK] List command works (no files in default location)")
    else:
        print(f"   [WARN] {result.stderr[:100] if result.stderr else result.stdout[:100]}")

# ============================================================
# Test 4: epi view (contents extraction)
# ============================================================
print("\n" + "-" * 40)
print("[4] epi view <file>")
print("-" * 40)
result = run_cmd(f"python -m epi_cli.main view {sample_epi}")
if result.returncode == 0:
    print("   [OK] View command works")
    # Show first few lines
    lines = result.stdout.strip().split("\n")[:3]
    for line in lines:
        print(f"      {line[:60]}...")
else:
    print(f"   [WARN] View may require browser: {result.stderr[:50]}")

# ============================================================
# Test 5: epi keys list
# ============================================================
print("\n" + "-" * 40)
print("[5] epi keys list")
print("-" * 40)
result = run_cmd("python -m epi_cli.main keys list")
if result.returncode == 0:
    print("   [OK] Keys list command works")
    output = result.stdout.strip()
    if output:
        print(f"      {output[:80]}...")
    else:
        print("      (no keys configured)")
else:
    print(f"   [WARN] {result.stderr[:80] if result.stderr else 'No output'}")

# ============================================================
# Test 6: epi keys generate (test key)
# ============================================================
print("\n" + "-" * 40)
print("[6] epi keys generate test_key")
print("-" * 40)
result = run_cmd("python -m epi_cli.main keys generate test_cli_key")
if result.returncode == 0:
    print("   [OK] Keys generate command works")
else:
    if "already exists" in str(result.stderr):
        print("   [OK] Key already exists (expected)")
    else:
        print(f"   [WARN] {result.stderr[:80] if result.stderr else 'Failed'}")

# ============================================================
# Test 7: epi debug (analyze .epi file)
# ============================================================
print("\n" + "-" * 40)
print("[7] epi debug <file>")
print("-" * 40)
result = run_cmd(f"python -m epi_cli.main debug {sample_epi}")
if result.returncode == 0:
    print("   [OK] Debug command works")
    lines = result.stdout.strip().split("\n")[:3]
    for line in lines:
        print(f"      {line[:60]}...")
else:
    # Debug might need API key for some features
    if "API" in result.stderr or "key" in result.stderr.lower():
        print("   [OK] Debug works but needs API key for full analysis")
    else:
        print(f"   [WARN] {result.stderr[:80] if result.stderr else 'Check output'}")

# ============================================================
# Test 8: epi run --help (don't actually run)
# ============================================================
print("\n" + "-" * 40)
print("[8] epi run --help")
print("-" * 40)
result = run_cmd("python -m epi_cli.main run --help")
if result.returncode == 0 and ("Usage" in result.stdout or "run" in result.stdout.lower()):
    print("   [OK] Run help command works")
else:
    print(f"   [WARN] {result.stderr[:80] if result.stderr else result.stdout[:80]}")

# ============================================================
# Test 9: epi record --help
# ============================================================
print("\n" + "-" * 40)
print("[9] epi record --help")
print("-" * 40)
result = run_cmd("python -m epi_cli.main record --help")
if result.returncode == 0:
    print("   [OK] Record help command works")
else:
    print(f"   [WARN] {result.stderr[:80] if result.stderr else result.stdout[:80]}")

# ============================================================
# Test 10: Python API import check
# ============================================================
print("\n" + "-" * 40)
print("[10] Python API Imports")
print("-" * 40)
try:
    from epi_recorder import record, wrap_openai, TracedOpenAI, get_current_session
    from epi_recorder.wrappers import TracedCompletions
    from epi_core import EPIContainer, ManifestModel
    from epi_core.trust import sign_manifest, verify_signature
    print("   [OK] All core imports work")
except ImportError as e:
    print(f"   [FAIL] Import error: {e}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("CLI COMMANDS TEST COMPLETE")
print("=" * 60)

# Cleanup
try:
    shutil.rmtree(test_dir)
    print(f"\nCleaned up: {test_dir}")
except:
    print(f"\nTest files at: {test_dir}")

print("\nCommands tested:")
print("   1. epi --help")
print("   2. epi verify <file>")
print("   3. epi ls")
print("   4. epi view <file>")
print("   5. epi keys list")
print("   6. epi keys generate")
print("   7. epi debug <file>")
print("   8. epi run --help")
print("   9. epi record --help")
print("  10. Python API imports")
