from gedcom.fact import Fact, GedcomTag


class Family:
    def __init__(self, fact: Fact) -> None:
        self.xref_id = fact.value  # Family ID
        self.husb: str | None = None  # Husband ID
        self.wife: str | None = None  # Wife ID
        self.children: list[str] = []  # List of children ID
        self.facts: list[Fact] = fact.sub_facts  # Store facts like MARR, DIV, etc.
        self.name: str | None = None

        self.parse_facts()

    def parse_facts(self) -> None:
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
