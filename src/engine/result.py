from dataclasses import dataclass, field
from typing import Any


@dataclass
class Result:
    text: str
    success: bool = True
    suggestions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
