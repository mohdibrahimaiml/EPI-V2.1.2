"""
Test EPI signing and verification to identify bugs
"""

import sys
import tempfile
from pathlib import Path
from datetime import datetime
import uuid

print("="*70)
print("EPI SIGNING/VERIFICATION DEBUG TEST")
print("="*70)
print()

# Test 1: Check key loading
print("[TEST 1] Load signing keys")
print("-"*70)
try:
    from epi_cli.keys import KeyManager
    km = KeyManager()
    private_key = km.load_private_key("default")
    public_key_bytes = km.load_public_key("default")
    
    print(f"[OK] Private key loaded: {type(private_key)}")
    print(f"[OK] Public key bytes: {len(public_key_bytes)} bytes")
    print(f"     Public key hex: {public_key_bytes.hex()[:32]}...")
except Exception as e:
    print(f"[FAIL] Could not load keys: {e}")
    sys.exit(1)

print()

# Test 2: Sign a manifest
print("[TEST 2] Sign a manifest")
print("-"*70)
try:
    from epi_core.schemas import ManifestModel
    from epi_core.trust import sign_manifest
    
    # Create test manifest
    manifest = ManifestModel(
        spec_version="2.5.0",
        workflow_id=uuid.uuid4(),
        created_at=datetime.utcnow(),
        file_manifest={
            "test.txt": "abc123"
        }
    )
    
    print(f"Original manifest signature: {manifest.signature}")
    print(f"Original manifest public_key: {manifest.public_key}")
    
    # Sign it
    signed_manifest = sign_manifest(manifest, private_key, "default")
    
    print(f"Signed manifest signature: {signed_manifest.signature[:50]}...")
    print(f"Signed manifest public_key: {signed_manifest.public_key[:32]}...")
    
    # CRITICAL CHECK: Does public_key in manifest match our public key?
    if signed_manifest.public_key == public_key_bytes.hex():
        print("[OK] Public key in manifest matches our public key")
    else:
        print("[BUG FOUND!] Public key mismatch!")
        print(f"  Expected: {public_key_bytes.hex()}")
        print(f"  Got:      {signed_manifest.public_key}")
        sys.exit(1)
    
except Exception as e:
    print(f"[FAIL] Signing failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 3: Verify the signature
print("[TEST 3] Verify signed manifest")
print("-"*70)
try:
    from epi_core.trust import verify_signature
    
    # Verify with the public key
    valid, message = verify_signature(signed_manifest, public_key_bytes)
    
    print(f"Verification result: {valid}")
    print(f"Message: {message}")
    
    if not valid:
        print("[BUG FOUND!] Signature verification failed!")
        print(f"  Signature: {signed_manifest.signature}")
        print(f"  Public key: {public_key_bytes.hex()}")
        sys.exit(1)
    else:
        print("[OK] Signature verified successfully")
        
except Exception as e:
    print(f"[FAIL] Verification failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 4: Create and verify a real .epi file
print("[TEST 4] Create and verify real .epi file")
print("-"*70)
try:
    from epi_recorder import record
    
    test_file = Path("epi-recordings/signing_test.epi")
    
    # Create .epi file
    with record(str(test_file), auto_sign=True):
        pass
    
    print(f"[OK] Created {test_file}")
    
    # Verify it
    from epi_core.container import EPIContainer
    
    manifest = EPIContainer.read_manifest(test_file)
    print(f"[OK] Read manifest")
    print(f"  Has signature: {manifest.signature is not None}")
    print(f"  Has public_key: {manifest.public_key is not None}")
    
    if manifest.signature:
        # Verify integrity
        integrity_ok, mismatches = EPIContainer.verify_integrity(test_file)
        print(f"  Integrity check: {integrity_ok}")
        
        # Verify signature using public_key FROM MANIFEST
        if manifest.public_key:
            manifest_public_key_bytes = bytes.fromhex(manifest.public_key)
            valid, message = verify_signature(manifest, manifest_public_key_bytes)
            print(f"  Signature check (using manifest public_key): {valid} - {message}")
            
            # CRITICAL: Also verify using our loaded public key
            valid2, message2 = verify_signature(manifest, public_key_bytes)
            print(f"  Signature check (using loaded public_key): {valid2} - {message2}")
            
            if valid != valid2:
                print("[BUG FOUND!] Signature verification inconsistent!")
                sys.exit(1)
    
except Exception as e:
    print(f"[FAIL] .epi file test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("="*70)
print("ALL SIGNING/VERIFICATION TESTS PASSED")
print("="*70)
