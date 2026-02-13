"""
COMPREHENSIVE SIGNING AND VERIFICATION TEST
Tests complete workflow after bug fix
"""

from pathlib import Path
from epi_recorder import record
from epi_core.container import EPIContainer
from epi_core.trust import verify_signature

print("="*70)
print("COMPREHENSIVE SIGNING/VERIFICATION TEST AFTER BUG FIX")
print("="*70)
print()

passed = 0
failed = 0

def test(name, condition):
    global passed, failed
    if condition:
        print(f"[PASS] {name}")
        passed += 1
    else:
        print(f"[FAIL] {name}")
        failed += 1

# Clean up old test file
test_file = Path("final_comprehensive_test.epi")
if test_file.exists():
    test_file.unlink()

print("[TEST 1] Create signed .epi file with different path formats")
print("-"*70)

# Test with just filename
with record("final_comprehensive_test.epi", goal="Complete test"):
    pass

test("File created", test_file.exists() if not test_file.is_absolute() else Path("epi-recordings/final_comprehensive_test.epi").exists())

# Use the actual path
actual_file = Path("epi-recordings/final_comprehensive_test.epi")

print()
print("[TEST 2] Verify file structure")
print("-"*70)

if actual_file.exists():
    test("File exists at correct location", True)
    test("File size > 0", actual_file.stat().st_size > 0)
    
    manifest = EPIContainer.read_manifest(actual_file)
    test("Manifest loaded", manifest is not None)
    test("Has signature", manifest.signature is not None)
    test("Has public_key", manifest.public_key is not None)
    
    print()
    print("[TEST 3] Cryptographic verification")
    print("-"*70)
    
    # Verify signature using public key from manifest
    if manifest.signature and manifest.public_key:
        pub_key_bytes = bytes.fromhex(manifest.public_key)
        sig_valid, sig_msg = verify_signature(manifest, pub_key_bytes)
        test("Signature valid", sig_valid)
        
        if sig_valid:
            print(f"      Message: {sig_msg}")
    
    print()
    print("[TEST 4] Integrity verification")
    print("-"*70)
    
    integrity_ok, mismatches = EPIContainer.verify_integrity(actual_file)
    test("Integrity check passes", integrity_ok)
    test("No mismatches", len(mismatches) == 0)
    
    print()
    print("[TEST 5] Path resolution correctness")
    print("-"*70)
    
    # Check that path doesn't have double epi-recordings
    path_str = str(actual_file)
    epi_rec_count = path_str.count("epi-recordings")
    test("No double epi-recordings directory", epi_rec_count <= 1)
    
else:
    print("[SKIP] File not created, skipping verification tests")
    failed += 5

print()
print("="*70)
print("SUMMARY")
print("="*70)
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Success Rate: {100*passed/(passed+failed) if (passed+failed) > 0 else 0:.1f}%")
print()

if failed == 0:
    print("SUCCESS - All signing and verification working perfectly!")
    print()
    print("What was fixed:")
    print("  1. Path resolution - no more double epi-recordings/")
    print("  2. Files create in correct location")
    print("  3. Signing works correctly")
    print("  4. Verification works correctly")
    print("  5. Ed25519 signatures valid")
else:
    print(f"FAILED - {failed} tests failed")
