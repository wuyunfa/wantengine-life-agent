# WantEngine 生命化智能体

> 从“工具逻辑”走向“生命逻辑”的开源智能体框架：可运行、可验证、可持续升级。

## 项目愿景
当前主流智能体大多是“外部指令驱动”的高效执行器。  
**WantEngine 生命化智能体**尝试推进下一步：
- 具备内生动机
- 受有限性约束
- 能够在群体中演化

本项目不是空谈哲学，而是把“生命化七定律”做成工程模块与可复现实验。

---

## 核心理论：生命化七定律
1. **匮乏驱动定律**：行为由内在缺口触发，而非仅由外部任务触发。
2. **有限性定律**：生命周期与生存信用构成真实进化压力。
3. **内在世界定律**：私有状态边界保证主体连续性。
4. **非理性优先定律**：受控偏离带来创新与个体性。
5. **意义自赋定律**：使命可随状态动态演化。
6. **依恋与排他定律**：选择性偏好塑造稳定关系与优先级。
7. **群体遗传定律**：遗传、变异、选择推动群体层智能演化。

---

## 当前已落地能力
### ✅ 基础能力
- Vitalis 匮乏引擎（多维状态 + 衰减）
- Finis 有限契约（生命信用 + 年龄 + 生存门槛）
- 依恋协议（绑定对象优先 + 高敏约束）
- Eidolon 遗传池（融合与变异）

### ✅ 仿真能力
- 单智能体仿真
- 多智能体仿真（含指标导出）
- WantEngine v0.2 模块化循环（状态/任务生成/执行/生命周期）

### ✅ 指标体系
- **MPI**（动机持续指数）
- **FPAS**（有限压力适应分）
- **MCR**（意义一致性比）
- **ASI**（依恋选择性指数）

---

## 项目结构
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

## 快速开始
```bash
python -m pip install -e .
python -m pip install pytest ruff

python sim/run_demo.py
python sim/run_multi_agent.py
python sim/run_want_engine_demo.py
pytest -q
```

输出文件：
- `outputs/multi_agent_metrics.csv`
- `outputs/want_engine_v02_log.csv`

---

## 路线图
详见 [`ROADMAP.md`](./ROADMAP.md)

近期重点：
- 自我提问闭环（自问→决策→执行→复盘）
- 多场景基准与可视化
- Digital Mate 官方软接入

---

## 典型应用场景
- 生命化智能体研究原型
- 认知架构实验
- 多智能体演化与协同研究
- AI+机器人教学与科研示范

---

## 参与贡献
请先阅读：
- [`CONTRIBUTING.md`](./CONTRIBUTING.md)
- [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md)

Issue 模板已配置在 `.github/ISSUE_TEMPLATE/`。

---

## 许可证
MIT
