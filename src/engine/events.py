from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Event:
    name: str
    payload: dict[str, Any] = field(default_factory=dict)


class Bus:
    def __init__(self):
        self.listeners: dict[str, list[Callable]] = {}
        self.history: list[Event] = []

    def sub(self, event_name: str, callback: Callable) -> None:
        self.listeners.setdefault(event_name, []).append(callback)

    def emit(self, event_name: str, payload: dict | None = None) -> Event:
        event = Event(name=event_name, payload=payload or {})

        self.history.append(event)

        for callback in self.listeners.get(event_name, []):
            callback(event)

        return event

    def clear_history(self) -> None:
        self.history.clear()
