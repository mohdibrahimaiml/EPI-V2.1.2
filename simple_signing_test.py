"""
Simple signing test - just verify .epi files can be created and verified
"""

from pathlib import Path
from epi_recorder import record

print("Creating signed .epi file...")
test_file = Path("epi-recordings/simple_sign_test.epi")

with record(str(test_file), auto_sign=True, goal="Test signing"):
    print("  Recording...")

print(f"\nFile exists: {test_file.exists()}")
print(f"File size: {test_file.stat().st_size if test_file.exists() else 'N/A'} bytes")

if test_file.exists():
    from epi_core.container import EPIContainer
    from epi_core.trust import verify_signature
    from epi_cli.keys import KeyManager
    
    # Read manifest
    manifest = EPIContainer.read_manifest(test_file)
    print(f"\nManifest:")
    print(f"  Has signature: {manifest.signature is not None}")
    print(f"  Has public_key: {manifest.public_key is not None}")
    
    if manifest.signature and manifest. public_key:
        # Verify using public_key FROM manifest
        pub_key_bytes = bytes.fromhex(manifest.public_key)
        valid, msg = verify_signature(manifest, pub_key_bytes)
        print(f"\nSignature verification: {valid}")
        print(f"Message: {msg}")
        
        # Also check integrity
        integrity_ok, mismatches = EPIContainer.verify_integrity(test_file)
        print(f"\nIntegrity check: {integrity_ok}")
        
        if valid and integrity_ok:
            print("\n[SUCCESS] Signing and verification working correctly!")
        else:
            print("\n[FAIL] Something is wrong")
            if mismatches:
                print(f"Mismatches: {mismatches}")
else:
    print("[FAIL] File was not created!")
