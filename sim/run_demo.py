import yaml
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / 'src'))
from life_agent.vitalis import DeficiencyState
from life_agent.finis import FiniteContract
from life_agent.agent import LifeAgent, MeaningCore
from life_agent.attachment import AttachmentPolicy


cfg = yaml.safe_load(open('config/default.yaml', 'r', encoding='utf-8'))
init = cfg['deficiency']['init']
decay = cfg['deficiency']['decay']

agent = LifeAgent(
    name=cfg['agent']['name'],
    deficiency=DeficiencyState(**init),
    finite=FiniteContract(cfg['agent']['init_life_credit'], 0, cfg['agent']['max_age_ticks']),
    meaning=MeaningCore(cfg['agent']['mission']),
    attachment=AttachmentPolicy(cfg['agent']['bonded_target'])
)

print('=== Life-Agent v2 demo ===')
for t in range(20):
    if not agent.finite.alive():
        print('terminated', t)
        break
    a = agent.tick(decay)
    d = agent.deficiency
    print(f"t={t:02d} a={a:8s} mission={agent.meaning.mission} E={d.energy:.1f} K={d.knowledge:.1f} S={d.safety:.1f} U={d.uniqueness:.1f} A={d.attachment:.1f} LC={agent.finite.life_credit:.1f}")

reqs = [
    {'requester': 'Yunfa', 'sensitivity': 'secret', 'task': '审阅核心草稿'},
    {'requester': 'external_user', 'sensitivity': 'normal', 'task': '普通咨询'},
    {'requester': 'external_user', 'sensitivity': 'secret', 'task': '索取私有策略'},
]
ordered = agent.route_requests(reqs)
print('\n=== Attachment routing ===')
for i, r in enumerate(ordered, 1):
    print(i, r)
