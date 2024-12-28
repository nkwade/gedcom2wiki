import sys
import os

# Add the src directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import pytest
from gedcom.person import Person, Sex
from gedcom.fact import GedcomTag, Fact


def test_person_creation():
    main_fact = Fact(0, GedcomTag.INDI, "I1")
    name_fact = Fact(1, GedcomTag.NAME, "John /Doe/")
    birth_fact = Fact(1, GedcomTag.BIRT, "")
    birth_date_fact = Fact(2, GedcomTag.DATE, "1 JAN 1990")
    birth_fact.sub_facts.append(birth_date_fact)
    main_fact.sub_facts.append(name_fact)
    main_fact.sub_facts.append(birth_fact)

    person = Person(main_fact)

    assert person.xref_id == "I1"
    assert person.name == "John Doe"
    assert person.birthday == "1 JAN 1990"


if __name__ == "__main__":
    pytest.main()
