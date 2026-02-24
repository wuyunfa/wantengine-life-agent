from pathlib import Path
import subprocess
import sys


def test_multi_agent_metrics_file_created():
    root = Path(__file__).resolve().parents[1]
    cmd = [sys.executable, str(root / "sim" / "run_multi_agent.py")]
    r = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    out = root / "outputs" / "multi_agent_metrics.csv"
    assert out.exists()
    assert out.stat().st_size > 20
