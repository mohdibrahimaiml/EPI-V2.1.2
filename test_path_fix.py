"""
Test the path fix
"""

from pathlib import Path
from epi_recorder.api import _resolve_output_path

print("Testing path resolution fix:")
print("="*60)

test_cases = [
    ("test.epi", "Just filename"),
    ("epi-recordings/test.epi", "Already includes epi-recordings"),
    ("subdir/test.epi", "Subdirectory without epi-recordings"),
    ("/absolute/path/test.epi", "Absolute path"),
    ("recording", "No extension"),
    (None, "Auto-generate"),
]

for path_input, description in test_cases:
    result = _resolve_output_path(path_input)
    print(f"\n{description}:")
    print(f"  Input:  {path_input}")
    print(f"  Output: {result}")
    
    # Check for double epi-recordings
    if "epi-recordings" in str(result):
        count = str(result).count("epi-recordings")
        if count > 1:
            print(f"  [BUG] Double directory! ({count} occurrences)")
        else:
            print(f"  [OK] Single directory")

print("\n" + "="*60)
print("Path resolution fix test complete")
