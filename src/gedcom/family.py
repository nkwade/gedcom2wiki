from .fact import Fact, GedcomTag


class Family:
    def __init__(self, fact: Fact) -> None:
        self.xref_id = fact.value  # Family ID
        self.husb: str | None = None  # Husband ID
        self.wife: str | None = None  # Wife ID
        self.children: list[str] = []  # List of children ID
        self.facts: list[Fact] = fact.sub_facts  # Store facts like MARR, DIV, etc.
        self.name: str | None = fact.value

        self.parse_facts()

    """
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
    """

    def parse_facts(self):
        to_remove: list[Fact] = []

        for sub in self.facts:
            if sub.tag == GedcomTag.HUSB:
                self.husb = sub.value
                to_remove.append(sub)
            elif sub.tag == GedcomTag.WIFE:
                self.wife = sub.value
                to_remove.append(sub)
            elif sub.tag == GedcomTag.CHIL:
                self.children.append(sub.value)
                to_remove.append(sub)

        for fact in to_remove:
            if len(fact.sub_facts) == 0:
                self.facts.remove(fact)

    def __repr__(self):
        return (
            f"Family({self.xref_id}, husb={self.husb}, wife={self.wife}, "
            f"children={self.children}, facts={self.facts})"
        )
