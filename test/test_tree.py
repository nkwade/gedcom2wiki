import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import pytest
from gedcom.tree import FamilyTree
from gedcom.fact import Fact, GedcomTag


def test_tree_parsing():
    head_fact = Fact(0, GedcomTag.HEAD, "")
    indi_fact = Fact(0, GedcomTag.INDI, "I1")
    fam_fact = Fact(0, GedcomTag.FAM, "F1")
    husb_fact = Fact(1, GedcomTag.HUSB, "I1")
    fam_fact.sub_facts.append(husb_fact)
    trlr_fact = Fact(0, GedcomTag.TRLR, "")

    facts = [head_fact, indi_fact, fam_fact, trlr_fact]
    tree = FamilyTree(facts)

    assert tree.header == head_fact
    assert tree.trailer == trlr_fact
    assert "I1" in tree.persons
    assert "F1" in tree.families
    assert "F1" in tree.persons["I1"].fams


def test_family_linking():
    i1_fact = Fact(0, GedcomTag.INDI, "I1")
    i2_fact = Fact(0, GedcomTag.INDI, "I2")
    i3_fact = Fact(0, GedcomTag.INDI, "I3")

    f1_fact = Fact(0, GedcomTag.FAM, "F1")
    husb_fact = Fact(1, GedcomTag.HUSB, "I1")
    wife_fact = Fact(1, GedcomTag.WIFE, "I2")
    child_fact = Fact(1, GedcomTag.CHIL, "I3")
    f1_fact.sub_facts.extend([husb_fact, wife_fact, child_fact])

    facts = [i1_fact, i2_fact, i3_fact, f1_fact]
    tree = FamilyTree(facts)

    assert "I1" in tree.persons
    assert "I2" in tree.persons
    assert "I3" in tree.persons
    assert "F1" in tree.families
    assert tree.persons["I1"].fams == ["F1"]
    assert tree.persons["I2"].fams == ["F1"]
    assert tree.persons["I3"].famc == ["F1"]


if __name__ == "__main__":
    pytest.main()
