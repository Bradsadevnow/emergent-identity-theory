# events.py
from dataclasses import dataclass
from typing import Any, Callable, Dict, List

@dataclass(frozen=True)
class GameEvent:
    name: str          # e.g. "ETB", "LEAVES", "CAST_SPELL", "DAMAGE"
    payload: Dict[str, Any]  # arbitrary, but consistent per event type
    timestamp: int     # monotonic event counter

class EventBus:
    def __init__(self):
        self._subs: Dict[str, List[Callable[[GameEvent], None]]] = {}
        self._counter = 0

    def dispatch(self, name: str, **payload):
        self._counter += 1
        evt = GameEvent(name=name, payload=payload, timestamp=self._counter)
        for fn in self._subs.get(name, []):
            fn(evt)
        # wildcard listeners
        for fn in self._subs.get("*", []):
            fn(evt)
        return evt

    def subscribe(self, name: str, handler: Callable[[GameEvent], None]):
        self._subs.setdefault(name, []).append(handler)
