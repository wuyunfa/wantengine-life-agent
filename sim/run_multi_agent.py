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
    decay = cfg["deficiency"]["decay"]

    pop_size = 12
    ticks = 60

    agents = [make_agent(f"agent_{i:02d}", cfg, "Yunfa" if i % 3 == 0 else "community") for i in range(pop_size)]

    out_dir = ROOT / "outputs"
    out_dir.mkdir(exist_ok=True)
    out_csv = out_dir / "multi_agent_metrics.csv"

    rows = []
    for t in range(ticks):
        alive = 0
        actions = {"recharge": 0, "learn": 0, "secure": 0, "create": 0, "bond": 0}

        for a in agents:
            if not a.finite.alive():
                continue
            alive += 1
            act = a.tick(decay)
            actions[act] += 1

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
        mcr = sum(1 for x in agents if "使命" in x.meaning.mission or "主动" in x.meaning.mission) / len(agents)

        rows.append(
            {
                "tick": t,
                "alive": alive,
                "avg_life_credit": round(avg(life_credits), 3),
                "action_recharge": actions["recharge"],
                "action_learn": actions["learn"],
                "action_secure": actions["secure"],
                "action_create": actions["create"],
                "action_bond": actions["bond"],
                "meaning_coherence_proxy": round(mcr, 3),
            }
        )

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"done: {out_csv}")


if __name__ == "__main__":
    main()
