import pytest
from gedcom.source import Source
from gedcom.fact import Fact, GedcomTag

def test_source_creation():
    main_fact = Fact(0, GedcomTag.SOUR, "S1")
    sour_title = Fact(1, GedcomTag.TITL, "Sample Title")
    sour_publ = Fact(1, GedcomTag.PUBL, "Sample Publication")
    sour_file = Fact(1, GedcomTag.FILE, "http://example.com/sample.jpg")
    main_fact.sub_facts.extend([sour_title, sour_publ, sour_file])

    source = Source(main_fact)

    assert source.xref_id == "S1"
    assert source.title == "Sample Title"
    assert source.publisher == "Sample Publication"
    assert source.link == "http://example.com/sample.jpg"

if __name__ == "__main__":
    pytest.main()