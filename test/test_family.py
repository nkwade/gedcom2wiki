import sys
import os

# Add the src directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


import pytest
from gedcom.family import Family
from gedcom.person import Person
from gedcom.tree import FamilyTree
from gedcom.fact import Fact, GedcomTag


def test_family_creation():
    main_fact = Fact(0, GedcomTag.FAM, "F1")
    husb_fact = Fact(1, GedcomTag.HUSB, "I1")
    wife_fact = Fact(1, GedcomTag.WIFE, "I2")
    child_fact = Fact(1, GedcomTag.CHIL, "I3")

    main_fact.sub_facts.extend([husb_fact, wife_fact, child_fact])
    fam = Family(main_fact)

    assert fam.xref_id == "F1"
    assert fam.husb == "I1"
    assert fam.wife == "I2"
    assert fam.children == ["I3"]


if __name__ == "__main__":
    pytest.main()
