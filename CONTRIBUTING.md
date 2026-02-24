# Contributing

Thanks for contributing to WantEngine Life Agent.

## Workflow
1. Fork the repo
2. Create a feature branch from `main`
3. Keep commits small and focused
4. Add/update docs and tests for behavior changes
5. Open a Pull Request with clear summary

## Local setup
```bash
python -m pip install -e .
python -m pip install pytest ruff
python sim/run_demo.py
pytest -q
```

## Coding rules
- Keep modules single-responsibility
- Prefer explicit state transitions over hidden side effects
- Preserve reproducibility in simulations
- Avoid hardcoding personal paths

## PR checklist
- [ ] Code builds and runs
- [ ] `sim/run_demo.py` works
- [ ] Tests pass
- [ ] Docs updated
- [ ] No secrets committed
