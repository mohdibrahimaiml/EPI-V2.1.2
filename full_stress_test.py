#!/usr/bin/env python3
"""
Full stress test for pip install epi-recorder
Running 54 installations to test stability and reliability
"""
import subprocess
import sys
import time
from datetime import datetime

def run_stress_test():
    start_time = datetime.now()
    print('EPI-RECORDER PIP INSTALL STRESS TEST - Full Suite')
    print('Running 54 installations as requested...')
    print(f'Start time: {start_time.strftime("%H:%M:%S")}')
    print()

    successes = 0
    failures = 0

    for i in range(1, 55):
        print(f'[{i:2d}/54] Installing...', end='', flush=True)
        
        try:
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', '--upgrade', 'epi-recorder'
            ], capture_output=True, text=True, timeout=180)  # 3-minute timeout
            
            if result.returncode == 0:
                print(' OK')
                successes += 1
            else:
                print(' FAIL')
                failures += 1
                
        except subprocess.TimeoutExpired:
            print(' TIMEOUT')
            failures += 1
        except Exception as e:
            print(f' ERROR: {str(e)[:50]}')
            failures += 1
        
        # Uninstall after each test (except the last one)
        if i < 54:
            subprocess.run([
                sys.executable, '-m', 'pip', 'uninstall', '-y', 'epi-recorder'
            ], capture_output=True, text=True, timeout=30)
            
        time.sleep(0.5)  # Short pause

    end_time = datetime.now()
    print()
    print('FINAL STRESS TEST RESULTS:')
    print(f'Total installations: 54')
    print(f'Successful: {successes}')
    print(f'Failed: {failures}')
    print(f'Success rate: {(successes/54)*100:.1f}%')
    print(f'Start time: {start_time.strftime("%H:%M:%S")}')
    print(f'End time: {end_time.strftime("%H:%M:%S")}')

    if failures == 0:
        print()
        print('🎉 PERFECT SCORE! All 54 installations succeeded.')
        print('EPI-Recorder installation is extremely stable!')
    elif failures <= 5:
        print()
        print('👍 Good result! Most installations succeeded.')
        print(f'Only {failures} failures out of 54 attempts.')
    else:
        print()
        print('⚠️  High failure rate detected.')
        print(f'{failures} failures out of 54 attempts need investigation.')

if __name__ == "__main__":
    run_stress_test()