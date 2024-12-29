from gedcom.person import Person
from gedcom.family import Family
from gedcom.fact import Fact, GedcomTag
from gedcom.source import Source


class FamilyTree:
    def __init__(self, facts: list[Fact]) -> None:
        self.persons: dict[str, Person] = {}  # key: xref_id, value: Person
        self.families: dict[str, Family] = {}  # key: xref_id, value: Family
        self.sources: dict[str, Source] = {}  # key: xref_id, value: Source
        self.header: Fact | None = None
        self.trailer: Fact | None = None
        self.data: list[Fact] = []  # list of facts not related to above facts

        self.parse_facts(facts)
        self.link_families()

    def parse_facts(self, facts: list[Fact]) -> None:
        for fact in facts:
            if fact.tag == GedcomTag.HEAD:
                self.header = fact
            elif fact.tag == GedcomTag.TRLR:
                self.trailer = fact
            elif fact.tag == GedcomTag.INDI:
                self.persons[fact.value] = Person(fact)
            elif fact.tag == GedcomTag.FAM:
                self.families[fact.value] = Family(fact)
            elif fact.tag == GedcomTag.SOUR:
                self.sources[fact.value] = Source(fact)
            else:
                self.data.append(fact)

    def link_families(self) -> None:
        """After parsing all individuals and families, link them."""
        for fam_id, family in self.families.items():
            if family.husb and self.persons.get(family.husb, None):
                self.persons[family.husb].fams.append(fam_id)
            if family.wife and self.persons.get(family.wife, None):
                self.persons[family.wife].fams.append(fam_id)

            if (
                family.husb
                and self.persons[family.husb].name
                and family.wife
                and self.persons[family.wife].name
            ):
                family.name = f"{self.persons[family.husb].name} and {self.persons[family.wife].name}"
            elif family.husb and self.persons[family.husb].name:
                family.name = self.persons[family.husb].name
            elif family.wife and self.persons[family.wife].name:
                family.name = self.persons[family.wife].name
            else:
                family.name = "Unknown"

            for c in family.children:
                if c in self.persons:
                    self.persons[c].famc.append(fam_id)

    def __repr__(self) -> str:
        return f"FamilyTree(persons={len(self.persons)}, families={len(self.families)})"
