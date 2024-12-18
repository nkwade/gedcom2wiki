from typing import Any
from .fact import Fact


class Family:
    def __init__(self, xref_id: str):
        self.xref_id = xref_id
        self.husb: str | None = None
        self.wife: str | None = None
        self.children: list[str] = []
        self.facts: list[Any] = []  # Store facts like MARR, DIV, etc.
        self.data: dict[str, list[Any]] = {}
        self.name: str | None = xref_id

    def add_data(self, tag: str, value: Any):
        if tag not in self.data:
            self.data[tag] = []
        self.data[tag].append(value)

    def add_fact(self, fact: Fact):
        self.facts.append(fact)

    def __repr__(self):
        return (
            f"Family({self.xref_id}, husb={self.husb}, wife={self.wife}, "
            f"children={self.children}, facts={self.facts})"
        )
