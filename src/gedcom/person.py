from typing import Any
from .fact import GedcomTag, Fact, TagValue
import enum
from datetime import datetime


class Person:
    def __init__(self, xref_id: str):
        self.xref_id = xref_id
        self.famc: list[str] = []  # Family IDs where this person is a child
        self.fams: list[str] = []  # Family IDs where this person is a spouse
        self.facts: list[Fact] = []

        # Common facts that nearly everyone has:
        self.sex: Sex | None = None
        self.birthday: datetime | str | None = None
        self.death: datetime | str = "Present"

    def parse_tag_values(self, tvs: list[TagValue]) -> None:
        # TODO: Implement this method
        # This will parse the tag values into the appropriate fields for common tags like NAME, SEX, BIRTH, DEATH, etc.
        i = 0
        queue: list[tuple[int, Fact]] = []

        while i < len(tvs):
            tv = tvs[i]
            while tv.level <= queue[-1][0]:
                done = queue.pop(-1)[1]
                self.parse_fact(done)

            fact = Fact(tv.tag, tv.value)

            if len(queue) > 0:
                queue[-1][1].sub_facts[fact.tag] = fact

            queue.append((tv.level, fact))

    def parse_fact(self, fact: Fact) -> None:
        if fact.tag == GedcomTag.SEX:
            self.sex = Sex[fact.value]
        elif fact.tag == GedcomTag.BIRT and GedcomTag.DATE in fact.sub_facts.keys():
            # TODO: write gedcom date to datetime function
            self.birthday = fact.sub_facts[GedcomTag.DATE].value
        elif fact.tag == GedcomTag.DEAT and GedcomTag.DATE in fact.sub_facts.keys():
            self.death = fact.sub_facts[GedcomTag.DATE].value
        else:
            pass #TODO: add any other facts I want to parse here

    def __repr__(self):
        return f"Person({self.xref_id}, famc={self.famc}, fams={self.fams}), data={self.data}, tag_values={self.tag_values}"


class Sex(enum.Enum):
    MALE = "M"
    FEMALE = "F"
