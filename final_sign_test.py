from pathlib import Path
import shutil
from epi_recorder import record

test_file = Path("epi-recordings") / "final_sign_test.epi"

# Make sure directory exists
test_file.parent.mkdir(exist_ok=True)

# Remove if exists
if test_file.exists():
    test_file.unlink()

print(f"Before: {test_file.exists()}")

# Create with record
with record(str(test_file), goal="Final test"):
    print("Recording...")

print(f"After: {test_file.exists()}")

if test_file.exists():
    print(f"Size: {test_file.stat().st_size} bytes")
    
    from epi_core.container import EPIContainer
    from epi_core.trust import verify_signature
    
    manifest = EPIContainer.read_manifest(test_file)
    print(f"Signature: {manifest.signature[:60] if manifest.signature else 'None'}...")
    print(f"Public key: {manifest.public_key[:32] if manifest.public_key else 'None'}...")
    
    if manifest.signature and manifest.public_key:
        pub_key_bytes = bytes.fromhex(manifest.public_key)
        valid, msg = verify_signature(manifest, pub_key_bytes)
        integrity_ok, _ = EPIContainer.verify_integrity(test_file)
        
        print(f"\nSignature valid: {valid}")
        print(f"Integrity OK: {integrity_ok}")
        
        if valid and integrity_ok:
            print("\n✅ SIGNING/VERIFICATION WORKING PERFECTLY")
        else:
            print(f"\n❌ PROBLEM: valid={valid}, integrity={integrity_ok}")
    else:
        print("\n❌ Missing signature or public_key")
else:
    print(f"\n❌ FILE NOT CREATED")
    print(f"Dir contents: {list(test_file.parent.glob('*.epi'))[-3:]}")
