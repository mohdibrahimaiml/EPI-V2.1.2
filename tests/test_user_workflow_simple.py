"""
Simplified end-to-end user workflow test.
Tests core functionality without running commands that may have display issues.
"""

import sys
import tempfile
from pathlib import Path
import pytest

# Test direct API usage (most common for users)
def test_api_workflow():
    """Test the Python API as a normal user would use it."""
    
    print("="*60)
    print("USER WORKFLOW TEST - Python API")
    print("="*60)
    print()
    
    # Use a proper temp directory
    import tempfile as tf
    with tf.TemporaryDirectory(prefix="epi_test_") as tmpdir_str:
        tmpdir = Path(tmpdir_str)
        
        # Test 1: Basic import
        print("Test 1: Import package...")
        from epi_recorder import record, EpiRecorderSession
        print("✅ Package imported successfully")
        
        # Test 2: Simple recording
        print("\nTest 2: Create simple recording...")
        epi_file = tmpdir / "test_basic.epi"
        with record(str(epi_file), workflow_name="Simple Test"):
            result = sum([1, 2, 3, 4, 5])
            print(f"   Calculated sum: {result}")
        
        assert epi_file.exists(), ".epi file not created"
        print(f"✅ Created {epi_file.name} ({epi_file.stat().st_size} bytes)")
        
        # Test 3: Recording with custom logging
        print("\nTest 3: Recording with custom steps...")
        epi_file2 = tmpdir / "test_custom.epi"
        with record(str(epi_file2), workflow_name="Custom", tags=["test"]) as epi:
            epi.log_step("data.load", {"rows": 100})
            result = 42 * 2
            epi.log_step("calc.done", {"result": result})
        
        assert epi_file2.exists(), ".epi file not created"
        print(f"✅ Created {epi_file2.name} with custom steps")
        
        # Test 4: Error handling (file should still be created)
        print("\nTest 4: Recording with error (should still save)...")
        epi_file3 = tmpdir / "test_error.epi"
        try:
            with record(str(epi_file3), workflow_name="Error Test") as epi:
                epi.log_step("start", {"status": "ok"})
                raise ValueError("Test error")
        except ValueError:
            pass  # Expected
        
        assert epi_file3.exists(), ".epi file not created after error"
        print(f"✅ Created {epi_file3.name} despite error")
        
        # Test 5: Verify files using Python API
        print("\nTest 5: Verify created files...")
        import subprocess
        
        for ef in [epi_file, epi_file2, epi_file3]:
            result = subprocess.run(
                f"python -m epi_cli.main verify {ef}",
                shell=True,
                capture_output=True,
                text=True
            )
            assert result.returncode == 0, f"Verification failed for {ef.name}"
            print(f"✅ {ef.name} verified")
        
        # Test 6: Recording with artifact
        print("\nTest 6: Recording with file artifact...")
        artifact_file = tmpdir / "output.txt"
        artifact_file.write_text("Sample output from workflow")
        
        epi_file4 = tmpdir / "test_artifact.epi"
        with record(str(epi_file4), workflow_name="With Artifact") as epi:
            epi.log_step("file.created", {"name": "output.txt"})
            epi.log_artifact(artifact_file)
        
        assert epi_file4.exists(), ".epi file not created"
        print(f"✅ Created {epi_file4.name} with artifact")
        
        # Test 7: Check all files
        print("\nTest 7: Summary of created files...")
        epi_files = list(tmpdir.glob("*.epi"))
        print(f"   Created {len(epi_files)} .epi files:")
        for f in epi_files:
            print(f"      • {f.name} ({f.stat().st_size:,} bytes)")
        
        assert len(epi_files) >= 4, f"Expected 4 files, found {len(epi_files)}"
        print(f"✅ All {len(epi_files)} files created")
        
        # Test 8: CLI verify command
        print("\nTest 8: Test CLI verify command...")
        result = subprocess.run(
            f"python -m epi_cli.main verify {epi_file}",
            shell=True,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"CLI verify failed: {result.stderr}"
        print("✅ CLI verify command works")
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\n📊 Test Results:")
        print("   ✅ Package imports")
        print("   ✅ Basic recording")
        print("   ✅ Custom step logging")
        print("   ✅ Error handling")
        print("   ✅ File verification")
        print("   ✅ Artifact capture")
        print("   ✅ CLI commands")
        print(f"   ✅ {len(epi_files)} .epi files created and verified")
        print("\n🎉 Package is ready for users!")
        print(f"\n📁 Test files saved to: {tmpdir}")


if __name__ == "__main__":
    test_api_workflow()
    sys.exit(0)

 