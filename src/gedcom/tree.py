from gedcom.person import Person
from gedcom.family import Family
from gedcom.fact import Fact, GedcomTag
from gedcom.source import Source

import time


class FamilyTree:
    def __init__(self, facts: list[Fact]) -> None:
        self.persons: dict[str, Person] = {}  # key: xref_id, value: Person
        self.families: dict[str, Family] = {}  # key: xref_id, value: Family
        self.sources: dict[str, Source] = {}  # key: xref_id, value: Source
        self.header: Fact | None = None
        self.trailer: Fact | None = None
        self.data: list[Fact] = []  # list of facts not related to above facts

        self.parse_facts(facts)
        start = time.time()
        self.link_families()
        print(f"Total link family time: {time.time() - start}")

    def parse_facts(self, facts: list[Fact]) -> None:
        person_time = family_time = source_time = 0.0

        for fact in facts:
            if fact.tag == GedcomTag.HEAD:
                self.header = fact
            elif fact.tag == GedcomTag.TRLR:
                self.trailer = fact
            elif fact.tag == GedcomTag.INDI:
                start = time.time()
                self.persons[fact.value] = Person(fact)
                person_time += time.time() - start
            elif fact.tag == GedcomTag.FAM:
                start = time.time()
                self.families[fact.value] = Family(fact)
                family_time += time.time() - start
            elif fact.tag == GedcomTag.SOUR:
                start = time.time()
                self.sources[fact.value] = Source(fact)
                source_time += time.time() - start
            else:
                self.data.append(fact)

        print(f"Total person time: {person_time}")
        print(f"Total family time: {family_time}")
        print(f"Total source time: {source_time}")

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
