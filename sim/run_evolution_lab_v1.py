import csv
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from life_agent.evolution_lab.genome import Genome
from life_agent.evolution_lab.lifecycle import LifeContract
from life_agent.evolution_lab.arena import EvoAgent, evaluate_agent
from life_agent.evolution_lab.selection import next_generation


def make_population(n: int = 24) -> list[EvoAgent]:
    pop = []
    for i in range(n):
        pop.append(
            EvoAgent(
                id=f"agent_{i:02d}",
                genome=Genome(
                    creativity=random.random(),
                    caution=random.random(),
                    sociality=random.random(),
                    exploration=random.random(),
                ),
                life=LifeContract(),
            )
        )
    return pop


def run(generations: int = 8, pop_size: int = 24):
    population = make_population(pop_size)
    rows = []

    for g in range(generations):
        # lifetime simulation for each generation
        for _ in range(30):
            for a in population:
                if a.life.alive():
                    a.life.tick()
                    # simple reward policy by trait-aligned events
                    reward = 0.5 * a.genome.caution + 0.4 * a.genome.exploration + 0.3 * a.genome.sociality
                    if random.random() < a.genome.creativity:
                        reward += 0.4
                    a.life.reward(reward)

        scores = [evaluate_agent(a) for a in population]
        avg_score = sum(scores) / len(scores)
        best = max(scores)
        alive = sum(1 for a in population if a.life.alive())

        rows.append({
            "generation": g,
            "avg_fitness": round(avg_score, 6),
            "best_fitness": round(best, 6),
            "alive_count": alive,
        })

        population = next_generation(population)

    out = ROOT / "outputs" / "evolution_lab_v1.csv"
    out.parent.mkdir(exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"done: {out}")


if __name__ == "__main__":
    run()
