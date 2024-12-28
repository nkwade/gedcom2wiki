import pytest
from gedcom.fact import Fact, GedcomTag

def test_fact_creation():
    parent_fact = Fact(0, GedcomTag.BIRT, "")
    date_fact = Fact(1, GedcomTag.DATE, "1 JAN 2000")
    parent_fact.sub_facts.append(date_fact)

    assert parent_fact.tag == GedcomTag.BIRT
    assert len(parent_fact.sub_facts) == 1
    assert parent_fact.sub_facts[0].tag == GedcomTag.DATE
    assert "1 JAN 2000" in str(parent_fact)

if __name__ == "__main__":
    pytest.main()