from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from life_agent.multi_agent import make_message, retry_send, resolve_conflict


def test_make_message_and_retry():
    msg = make_message("m1", "request", "planner", "researcher", "t1", {"x": 1})
    attempts = {"n": 0}

    def send_fn(_):
        attempts["n"] += 1
        return attempts["n"] >= 2

    ok = retry_send(send_fn, msg, max_retries=3)
    assert ok is True
    assert attempts["n"] == 2


def test_conflict_resolution():
    old_item = {"version": 1, "confidence": 0.8, "value": "A"}
    new_item = {"version": 2, "confidence": 0.7, "value": "B"}
    out = resolve_conflict(old_item, new_item, policy="newer_wins")
    assert out["value"] == "B"
