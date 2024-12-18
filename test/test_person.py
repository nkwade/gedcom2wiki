import sys
import os

# Add the src directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import pytest
from gedcom.person import Person, Sex  # type: ignore
from gedcom.fact import GedcomTag, TagValue, Fact  # type: ignore


def test_parse_tag_values():
    person = Person(xref_id="I1")
    tag_values = [
        TagValue(level=1, tag=GedcomTag.NAME, value="John /Doe/"),
        TagValue(level=1, tag=GedcomTag.SEX, value="M"),
        TagValue(level=1, tag=GedcomTag.BIRT, value=""),
        TagValue(level=2, tag=GedcomTag.DATE, value="1 JAN 1990"),
        TagValue(level=3, tag=GedcomTag.DATE, value="10am est"),
        TagValue(level=1, tag=GedcomTag.DEAT, value=""),
        TagValue(level=2, tag=GedcomTag.DATE, value="31 DEC 2050"),
    ]
    person.parse_tag_values(tag_values)

    assert person.sex == Sex.M
    assert person.birthday == "1 JAN 1990"
    assert person.death == "31 DEC 2050"
    assert len(person.facts) == 4
    assert len(person.facts[2].sub_facts.keys()) == 1


def test_parse_fact():
    person = Person(xref_id="I2")
    fact_sex = Fact(tag=GedcomTag.SEX, value="F")
    person.parse_fact(fact_sex)
    assert person.sex == Sex.F

    fact_birth = Fact(tag=GedcomTag.BIRT, value="")
    fact_birth.sub_facts[GedcomTag.DATE] = Fact(tag=GedcomTag.DATE, value="15 JUL 1985")
    person.parse_fact(fact_birth)
    assert person.birthday == "15 JUL 1985"


def test_person_initialization():
    person = Person(xref_id="I3")
    assert person.xref_id == "I3"
    assert person.famc == []
    assert person.fams == []
    assert person.facts == []
    assert person.sex is None
    assert person.birthday is None
    assert person.death == "Present"


if __name__ == "__main__":
    pytest.main()
