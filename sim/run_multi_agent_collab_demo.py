from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from life_agent.multi_agent import CollaborationOrchestrator


def main():
    orch = CollaborationOrchestrator()
    goal = "deliver a module-focused, tested upgrade"
    result = orch.run_round(goal)

    out = ROOT / "outputs" / "multi_agent_collab_round.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"done: {out}")
    print(f"status: {result['round_status']}")


if __name__ == "__main__":
    main()
