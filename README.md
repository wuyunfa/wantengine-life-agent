# WantEngine Life Agent

A life-oriented AI agent prototype inspired by the **Seven Laws of AI Agent Vitalization**.

## Vision
Traditional agents are task-driven tools. This project explores a different path:

- Endogenous deficiency-driven behavior
- Finite lifecycle and survival pressure
- Private inner world boundary
- Bounded irrational decision-making
- Self-endowed meaning evolution
- Attachment and exclusivity policy
- Genetic inheritance and mutation

## Project Structure

```text
src/life_agent/
  vitalis.py      # Deficiency engine
  finis.py        # Finiteness contract
  attachment.py   # Attachment/exclusivity routing
  eidolon.py      # Genetic inheritance and mutation
  agent.py        # Agent core and orchestration
  want_engine/
    state.py      # Boredom/curiosity/energy/fatigue state model
    taskgen.py    # Template-based task generation engine
    executor.py   # OpenClaw-aware executor with fallback
    loop.py       # End-to-end lifecycle loop
sim/
  run_demo.py
  run_multi_agent.py
  run_want_engine_demo.py
config/
  default.yaml
  scenarios.yaml
pet/
  desktop_pet_wantengine.py
```

## Quick Start

```bash
python -m pip install pyyaml
python sim/run_demo.py
python sim/run_multi_agent.py
python sim/run_want_engine_demo.py
```

Outputs:
- `outputs/multi_agent_metrics.csv`
- `outputs/want_engine_v02_log.csv`

## Core Modules

1. **Vitalis (Want Engine)**
   - Multi-dimensional deficiency state and decay
   - Pressure-driven autonomous action proposal

2. **Finis (Finite Contract)**
   - Life credit, aging, survival gate
   - Reward/penalty for long-horizon adaptation

3. **Inner World Layer**
   - Private memory separated from external summary

4. **Irrational Engine**
   - 70% rational best-choice + 30% bounded divergence

5. **Meaning Core**
   - Mission evolves by internal state transitions

6. **Attachment Protocol**
   - Prioritized routing for bonded target
   - Secret disclosure constraints

7. **Eidolon Genetic Pool**
   - Trait fusion + mutation for offspring agents

## Roadmap

See `ROADMAP.md` for staged milestones.

## Language

- English: `README.md`
- 中文：`README.zh-CN.md`

## License

MIT
