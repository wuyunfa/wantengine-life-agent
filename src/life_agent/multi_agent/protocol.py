from dataclasses import dataclass
from typing import Literal
import time

MsgType = Literal['request', 'response', 'evidence', 'risk', 'handoff']


@dataclass
class ProtocolMessage:
    msg_id: str
    msg_type: MsgType
    sender: str
    receiver: str
    task_id: str
    payload: dict
    timestamp: float


def make_message(msg_id: str, msg_type: MsgType, sender: str, receiver: str, task_id: str, payload: dict) -> ProtocolMessage:
    return ProtocolMessage(
        msg_id=msg_id,
        msg_type=msg_type,
        sender=sender,
        receiver=receiver,
        task_id=task_id,
        payload=payload,
        timestamp=time.time(),
    )


def retry_send(send_fn, message: ProtocolMessage, max_retries: int = 3, base_delay: float = 0.2) -> bool:
    for i in range(max_retries):
        ok = send_fn(message)
        if ok:
            return True
        time.sleep(base_delay * (i + 1))
    return False


def resolve_conflict(old_item: dict, new_item: dict, policy: str = 'newer_wins') -> dict:
    if policy == 'newer_wins':
        return new_item if new_item.get('version', 0) >= old_item.get('version', 0) else old_item
    if policy == 'higher_confidence':
        return new_item if new_item.get('confidence', 0.0) >= old_item.get('confidence', 0.0) else old_item
    return old_item
