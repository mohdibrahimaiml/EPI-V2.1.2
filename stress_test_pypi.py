import subprocess
import time
import sys
from datetime import datetime

def stress_test(iterations):
    print(f"Starting stress test: {iterations} iterations of 'pip install epi-recorder --force-reinstall --no-cache-dir'")
    success_count = 0
    fail_count = 0
    
    start_time = time.time()
    
    for i in range(1, iterations + 1):
        iter_start = time.time()
        print(f"\n[{i}/{iterations}] Installing epi-recorder...")
        
        try:
            # Run pip install command
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "epi-recorder", "--force-reinstall", "--no-cache-dir"],
                capture_output=True,
                text=True,
                check=True
            )
            elapsed = time.time() - iter_start
            print(f"[OK] Success (took {elapsed:.2f}s)")
            success_count += 1
        except subprocess.CalledProcessError as e:
            elapsed = time.time() - iter_start
            print(f"[FAIL] Failed (took {elapsed:.2f}s)")
            print(f"Error output: {e.stderr}")
            fail_count += 1
        except Exception as e:
            print(f"[ERROR] Error: {e}")
            fail_count += 1

    total_time = time.time() - start_time
    print("\n" + "="*30)
    print("STRESS TEST COMPLETE")
    print(f"Total Iterations: {iterations}")
    print(f"Successful: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"Total Time: {total_time:.2f}s")
    print("="*30)

if __name__ == "__main__":
    # You can change the number of iterations here
    stress_test(500)
