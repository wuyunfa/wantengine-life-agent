from pathlib import Path
import subprocess
import sys
import json


def test_multi_agent_collab_round():
    root = Path(__file__).resolve().parents[1]
    cmd = [sys.executable, str(root / "sim" / "run_multi_agent_collab_demo.py")]
    r = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr

    out = root / "outputs" / "multi_agent_collab_round.json"
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["round_status"] in {"done", "needs_refine"}
    assert "review" in data and "checks" in data["review"]
