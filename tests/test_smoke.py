from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / 'src'))

from life_agent.vitalis import DeficiencyState
from life_agent.finis import FiniteContract
from life_agent.agent import LifeAgent, MeaningCore
from life_agent.attachment import AttachmentPolicy


def test_agent_tick_runs():
    d = DeficiencyState(100, 60, 80, 50, 70)
    f = FiniteContract(100, 0, 100)
    a = LifeAgent(
        name='WantEngine',
        deficiency=d,
        finite=f,
        meaning=MeaningCore('守护长期项目质量'),
        attachment=AttachmentPolicy('Yunfa'),
    )
    action = a.tick({
        'energy': (1.0, 2.0),
        'knowledge': (0.3, 0.8),
        'safety': (0.2, 0.7),
        'uniqueness': (0.2, 0.6),
        'attachment': (0.2, 0.6),
    })
    assert action in {'recharge', 'learn', 'secure', 'create', 'bond'}
    assert a.finite.life_credit > 0


def test_attachment_priority():
    policy = AttachmentPolicy('Yunfa')
    p1 = policy.priority('Yunfa', 'secret')
    p2 = policy.priority('external_user', 'secret')
    assert p1 > p2
    assert policy.allow_disclosure('Yunfa', 'secret') is True
    assert policy.allow_disclosure('external_user', 'secret') is False
