# WantEngine Life Agent

> From tool logic to life logic: an open-source agent framework for **endogenous motivation**, **finiteness pressure**, and **evolving intelligence**.

## Why this project
Most agents today are excellent task executors, but still fundamentally external-instruction driven.  
**WantEngine Life Agent** explores a next step: agents that can generate internal drives, adapt under finite constraints, and evolve across generations.

This project is built for researchers, engineers, and creators who want to prototype **life-oriented AI systems** with reproducible engineering modules.

---

## Core Idea: Seven Laws of Agent Vitalization
1. **Deficiency-Driven Law** — motivation emerges from internal scarcity, not only prompts.
2. **Finiteness Law** — bounded life/credit creates urgency and adaptive pressure.
3. **Inner-World Law** — private internal state enables subjective continuity.
4. **Irrationality-Priority Law** — bounded deviation unlocks novelty and creativity.
5. **Meaning Self-Endowment Law** — mission evolves from internal state transitions.
6. **Attachment & Exclusivity Law** — selective preference shapes stable social behavior.
7. **Group Genetic Law** — inheritance + mutation enables population-level evolution.

---

## What is already implemented
### ✅ Foundation modules
- `Vitalis` deficiency engine (multi-dimensional state + decay)
- `Finis` finite contract (life credit + aging + survival gate)
- Attachment policy routing (bonded target priority + secret constraints)
- Genetic pool (`Eidolon`) with trait fusion and mutation

### ✅ Simulation stack
- Single-agent simulation
- Multi-agent simulation with metrics export
- WantEngine v0.2 modular loop:
  - state
  - task generation
  - execution with fallback
  - lifecycle control and CSV logging

### ✅ Metrics (for research/reporting)
- **MPI**: Motivation Persistence Index
- **FPAS**: Finite-Pressure Adaptation Score
- **MCR**: Meaning Coherence Ratio
- **ASI**: Attachment Selectivity Index

---

## Repository structure
```text
src/life_agent/
  vitalis.py
  finis.py
  attachment.py
  eidolon.py
  agent.py
  metrics.py
  want_engine/
    state.py
    taskgen.py
    executor.py
    loop.py

sim/
  run_demo.py
  run_multi_agent.py
  run_want_engine_demo.py

config/
  default.yaml
  scenarios.yaml

tests/
  test_smoke.py
  test_multi_agent.py
  test_want_engine_v02.py

pet/
  desktop_pet_wantengine.py
  moe_pet_life.py
```

---

## Quick start
```bash
python -m pip install -e .
python -m pip install pytest ruff

python sim/run_demo.py
python sim/run_multi_agent.py
python sim/run_want_engine_demo.py
pytest -q
```

Outputs:
- `outputs/multi_agent_metrics.csv`
- `outputs/want_engine_v02_log.csv`

---

## Vision roadmap
See [`ROADMAP.md`](./ROADMAP.md) for staged milestones.

Near-term focus:
- self-reflection loop (ask-self → decide → execute → review)
- scenario benchmarks and visual analytics
- Digital Mate official soft-integration path

---

## Use cases
- Research prototypes for autonomous/life-oriented agents
- Cognitive architecture experiments
- Multi-agent adaptation and evolution studies
- Educational demonstrations for AI + robotics programs

---

## Contributing
Please read:
- [`CONTRIBUTING.md`](./CONTRIBUTING.md)
- [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md)

Issue templates are available under `.github/ISSUE_TEMPLATE/`.

---

## Language
- English: `README.md`
- 中文：[`README.zh-CN.md`](./README.zh-CN.md)

---

## License
MIT
