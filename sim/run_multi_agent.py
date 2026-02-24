import csv
import random
from pathlib import Path
import yaml
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from life_agent.vitalis import DeficiencyState
from life_agent.finis import FiniteContract
from life_agent.agent import LifeAgent, MeaningCore
from life_agent.attachment import AttachmentPolicy
from life_agent.eidolon import reproduce
from life_agent.metrics import calc_mpi, calc_fpas, calc_mcr, calc_asi


def make_agent(name: str, cfg: dict, bonded: str) -> LifeAgent:
    init = cfg["deficiency"]["init"].copy()
    # slight random initialization noise
    for k in init:
        init[k] = max(0.0, min(100.0, init[k] + random.uniform(-5, 5)))
    return LifeAgent(
        name=name,
        deficiency=DeficiencyState(**init),
        finite=FiniteContract(
            cfg["agent"]["init_life_credit"] + random.uniform(-5, 5),
            0,
            cfg["agent"]["max_age_ticks"],
        ),
        meaning=MeaningCore(cfg["agent"]["mission"]),
        attachment=AttachmentPolicy(bonded),
    )


def avg(values):
    return sum(values) / len(values) if values else 0.0


def main():
    cfg = yaml.safe_load((ROOT / "config" / "default.yaml").read_text(encoding="utf-8"))
    scene_cfg = yaml.safe_load((ROOT / "config" / "scenarios.yaml").read_text(encoding="utf-8"))
    scene = scene_cfg.get("default", {})

    decay = cfg["deficiency"]["decay"].copy()
    if "decay_boost" in scene:
        for k, v in scene["decay_boost"].items():
            lo, hi = decay[k]
            decay[k] = [lo * v, hi * v]

    pop_size = scene.get("pop_size", 12)
    ticks = scene.get("ticks", 60)

    agents = [make_agent(f"agent_{i:02d}", cfg, "Yunfa" if i % 3 == 0 else "community") for i in range(pop_size)]

    init_override = scene.get("init_override", {})
    if init_override:
        for a in agents:
            for k, v in init_override.items():
                setattr(a.deficiency, k, float(v))

    out_dir = ROOT / "outputs"
    out_dir.mkdir(exist_ok=True)
    out_csv = out_dir / "multi_agent_metrics.csv"

    rows = []
    bond_first_count = 0
    for t in range(ticks):
        alive = 0
        actions = {"recharge": 0, "learn": 0, "secure": 0, "create": 0, "bond": 0}
        action_list = []
        mission_list = []

        for a in agents:
            if not a.finite.alive():
                continue
            alive += 1
            act = a.tick(decay)
            actions[act] += 1
            action_list.append(act)
            mission_list.append(a.meaning.mission)

            test_req = [
                {"requester": "Yunfa", "sensitivity": "secret", "task": "core"},
                {"requester": "external", "sensitivity": "normal", "task": "normal"},
            ]
            ordered = a.route_requests(test_req)
            if ordered and ordered[0].get("requester") == "Yunfa":
                bond_first_count += 1

        # simple generation step every 20 ticks: replace lowest life_credit agent
        if t > 0 and t % 20 == 0:
            living = [x for x in agents if x.finite.alive()]
            if len(living) >= 2:
                parents = sorted(living, key=lambda x: x.finite.life_credit, reverse=True)[:2]
                child_gene = reproduce(parents[0].gene, parents[1].gene)
                # replace worst alive
                worst = sorted(living, key=lambda x: x.finite.life_credit)[0]
                idx = agents.index(worst)
                newborn = make_agent(f"agent_new_{t}", cfg, "community")
                newborn.gene = child_gene
                agents[idx] = newborn

        life_credits = [x.finite.life_credit for x in agents if x.finite.alive()]
        avg_credit = round(avg(life_credits), 3)

        rows.append(
            {
                "tick": t,
                "alive": alive,
                "avg_life_credit": avg_credit,
                "action_recharge": actions["recharge"],
                "action_learn": actions["learn"],
                "action_secure": actions["secure"],
                "action_create": actions["create"],
                "action_bond": actions["bond"],
                "mpi": calc_mpi(action_list),
                "fpas": calc_fpas(avg_credit),
                "mcr": calc_mcr(mission_list),
                "asi": calc_asi(bond_first_count, (t + 1) * max(alive, 1)),
            }
        )

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"done: {out_csv}")


if __name__ == "__main__":
    main()
