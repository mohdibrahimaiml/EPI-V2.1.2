#!/usr/bin/env python3
"""
Stress test for pip install epi-recorder
Running 54 installations to test stability and reliability
"""
import subprocess
import sys
import time
from datetime import datetime

def run_installation_test(iteration):
    """Run a single installation test and return success/failure"""
    print(f"[{iteration}/54] Starting installation test at {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        # Run pip install command
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", "epi-recorder"
        ], capture_output=True, text=True, timeout=300)  # 5 minute timeout
        
        success = result.returncode == 0
        if success:
            print(f"[{iteration}/54] ✓ Installation successful")
        else:
            print(f"[{iteration}/54] ✗ Installation failed")
            print(f"  Error: {result.stderr[:200]}...")  # Truncate long errors
            
        return success, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        print(f"[{iteration}/54] ✗ Installation timed out")
        return False, "", "Installation timed out after 5 minutes"
    except Exception as e:
        print(f"[{iteration}/54] ✗ Installation error: {str(e)}")
        return False, "", str(e)

def run_uninstall_test():
    """Uninstall epi-recorder to prepare for next test"""
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "uninstall", "-y", "epi-recorder"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✓ Uninstalled successfully")
        else:
            print(f"⚠ Uninstall had issues: {result.stderr[:100]}...")
            
    except Exception as e:
        print(f"⚠ Uninstall error: {str(e)}")

def main():
    print("="*60)
    print("EPI-RECORDER PIP INSTALL STRESS TEST")
    print(f"Running 54 installation tests")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    successes = 0
    failures = 0
    
    for i in range(1, 55):
        print()
        success, stdout, stderr = run_installation_test(i)
        
        if success:
            successes += 1
        else:
            failures += 1
            
        # Uninstall after each test to prepare for next
        if i < 54:  # Don't uninstall after the last one
            print(f"[{i}/54] Uninstalling for next test...")
            run_uninstall_test()
        
        # Small delay between installations
        time.sleep(2)
    
    print()
    print("="*60)
    print("STRESS TEST RESULTS")
    print("="*60)
    print(f"Total tests: 54")
    print(f"Successful: {successes}")
    print(f"Failed: {failures}")
    print(f"Success rate: {(successes/54)*100:.1f}%")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    if failures == 0:
        print("🎉 ALL TESTS PASSED! Installation is stable.")
    else:
        print(f"⚠️  {failures} tests failed. Please review installation issues.")
    
    return failures == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)