from .fact import Fact, GedcomTag


class Source:
    def __init__(self, xref_id: str) -> None:
        self.xref_id: str = xref_id
        self.title: str | None = None
        self.origin: str | None = None
        self.publisher: str | None = None
        self.link: str | None = None
        self.facts: list[Fact] = []

    def parse_facts(self):
        for fact in self.facts:
            if fact.tag == GedcomTag.TITL:
                self.title = fact.value
            elif fact.tag == GedcomTag._TYPE:
                self.origin = fact.value
            elif fact.tag == GedcomTag.PUBL:
                self.publisher = fact.value
            #TODO: get link
