from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from life_agent.want_engine import WantEngine


if __name__ == "__main__":
    engine = WantEngine()
    out = engine.run(steps=40)
    print(f"done: {out}")
