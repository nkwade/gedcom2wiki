import sys
import os

# Add the src directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


import pytest  # type: ignore
from gedcom.family import Family  # type: ignore
from gedcom.person import Person  # type: ignore
from gedcom.tree import FamilyTree  # type: ignore


def test_link_families():
    # Create a FamilyTree instance
    ft = FamilyTree()

    # Create some Person instances
    person1 = Person(xref_id="I1")
    person2 = Person(xref_id="I2")
    person3 = Person(xref_id="I3")

    # Create some Family instances
    family1 = Family(xref_id="F1")
    family2 = Family(xref_id="F2")

    # Assign relationships
    family1.husb = person1.xref_id
    family1.wife = person2.xref_id
    family1.children.append(person3.xref_id)

    family2.husb = person3.xref_id
    family2.wife = person2.xref_id

    # Add persons and families to the FamilyTree
    ft.persons = {p.xref_id: p for p in [person1, person2, person3]}
    ft.families = {f.xref_id: f for f in [family1, family2]}

    # Link the families
    ft.link_families()

    # Check if the linking is correct
    assert person1.fams == ["F1"]
    assert person2.fams == ["F1", "F2"]
    assert person3.famc == ["F1"]
    assert person3.fams == ["F2"]


if __name__ == "__main__":
    pytest.main()
