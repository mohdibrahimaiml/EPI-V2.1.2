from pathlib import Path
import traceback
from epi_recorder import record

test_file = Path("epi-recordings") / "debug_test.epi"
test_file.parent.mkdir(exist_ok=True)

if test_file.exists():
    test_file.unlink()

print(f"Before: {test_file.exists()}")

try:
    with record(str(test_file), goal="Debug test") as session:
        print(f"Inside context, session: {session}")
        print(f"  Output path: {session.output_path if session else 'No session'}")
        print(f"  Temp dir: {session.temp_dir if session else 'No session'}")
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()

print(f"After: {test_file.exists()}")

# Check if it was created elsewhere
import os
print(f"CWD: {os.getcwd()}")
print(f"Files in epi-recordings: {len(list(Path('epi-recordings').glob('*.epi')))}")
