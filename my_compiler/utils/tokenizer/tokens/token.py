from dataclasses import dataclass


@dataclass
class Token:
    value: str
    tag: str
    priority: int
