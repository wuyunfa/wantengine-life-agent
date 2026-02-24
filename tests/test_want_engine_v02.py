from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from life_agent.want_engine import WantEngine


def test_want_engine_runs_and_exports_csv(tmp_path):
    engine = WantEngine()
    out = tmp_path / "want.csv"
    file_path = engine.run(steps=5, save_csv=True, csv_path=str(out))
    assert file_path is not None
    assert Path(file_path).exists()
    assert Path(file_path).stat().st_size > 20


def test_want_engine_cycle_has_required_fields():
    engine = WantEngine()
    row = engine.run_cycle()
    keys = {
        "intention_type",
        "task",
        "complexity",
        "energy",
        "boredom",
        "curiosity",
        "fatigue",
        "deep_rest",
        "success",
    }
    assert keys.issubset(set(row.keys()))
