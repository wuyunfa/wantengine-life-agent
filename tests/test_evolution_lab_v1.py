from pathlib import Path
import subprocess
import sys


def test_evolution_lab_runs_and_exports_csv():
    root = Path(__file__).resolve().parents[1]
    cmd = [sys.executable, str(root / "sim" / "run_evolution_lab_v1.py")]
    r = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    out = root / "outputs" / "evolution_lab_v1.csv"
    assert out.exists()
    assert out.stat().st_size > 30
