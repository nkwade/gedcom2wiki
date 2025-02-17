from gedcom.fact import Fact, GedcomTag


class Source:
    def __init__(self, fact: Fact) -> None:
        self.xref_id: str = fact.value
        self.title: str = "Unknown"
        self.origin: str = "Unknown"
        self.publisher: str = "Unknown"
        self.link: str = "Unknown"
        self.facts: list[Fact] = fact.sub_facts

        self.parse_facts()

    @property
    def display_name(self) -> str:
        if self.title != "Unknown":
            return self.title
        return self.xref_id

    def parse_facts(self) -> None:
        to_remove: list[Fact] = []  # remove used facts that have no subfacts
        for sub in self.facts:
            if sub.tag == GedcomTag.TITL:
                self.title = sub.value
                to_remove.append(sub)

            if sub.tag == GedcomTag._TYPE:
                self.origin = sub.value
                to_remove.append(sub)

            if sub.tag == GedcomTag.PUBL:
                self.publisher = sub.value
                to_remove.append(sub)

            if sub.tag == GedcomTag.FILE:
                self.link = sub.value
                to_remove.append(sub)

        for fact in to_remove:
            if len(fact.sub_facts) == 0:
                self.facts.remove(fact)
