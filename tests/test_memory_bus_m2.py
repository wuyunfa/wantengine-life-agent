from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from life_agent.multi_agent import SharedMemoryBus


def test_memory_bus_basic_flow():
    bus = SharedMemoryBus()
    bus.put_fact("goal", "test", source="planner")
    bus.add_task({"name": "collect_context", "status": "open"})
    t = bus.claim_task("researcher")
    assert t is not None
    ok = bus.close_task("collect_context", "done", "researcher")
    assert ok is True
    snap = bus.snapshot()
    assert "goal" in snap["facts"]
    assert len(snap["events"]) >= 3


def test_collab_output_contains_memory_bus():
    cmd = [sys.executable, str(ROOT / "sim" / "run_multi_agent_collab_demo.py")]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0
    out = ROOT / "outputs" / "multi_agent_collab_round.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "memory_bus" in data
    assert "facts" in data["memory_bus"]
