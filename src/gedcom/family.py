from typing import Any
from .fact import Fact, TagValue


class Family:
    def __init__(self, xref_id: str):
        self.xref_id = xref_id  # Family ID
        self.husb: str | None = None  # Husband ID
        self.wife: str | None = None  # Wife ID
        self.children: list[str] = []  # List of children ID
        self.facts: list[Fact] = []  # Store facts like MARR, DIV, etc.
        self.name: str | None = xref_id

    def parse_data(self, data: list[TagValue]):
        i = 0
        queue: list[tuple[int, Fact]] = []  # level, Fact

        while i < len(data):
            tv = data[i]
            while len(queue) > 0 and tv.level <= queue[-1][0]:
                level, done = queue.pop(-1)
                if (
                    level == 1
                ):  # all subfacts stored in fact so we only want to keep track of level 1 facts for people
                    self.facts.append(done)

            fact = Fact(tv.tag, tv.value)

            if len(queue) > 0:
                queue[-1][1].sub_facts[fact.tag] = fact

            queue.append((tv.level, fact))
            i += 1

        # Finish the last fact left in the queue
        while len(queue) != 0:
            level, done = queue.pop(-1)
            if level == 1:
                self.facts.append(done)

    def __repr__(self):
        return (
            f"Family({self.xref_id}, husb={self.husb}, wife={self.wife}, "
            f"children={self.children}, facts={self.facts})"
        )
