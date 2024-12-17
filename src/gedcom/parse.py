from .person import Person
from .family import Family
from .tree import FamilyTree
from .fact import GedcomTag, TagValue


def parse_gedcom(gedcom_text: str) -> FamilyTree:
    lines = gedcom_text.splitlines()
    ft = FamilyTree()

    # Parse the header
    # starts with a 0 and goes until the first INDI
    i = 1
    data = []
    while not lines[i].startswith("0 @I"):
        data.append(lines[i])
        i += 1
    header = parse_header(data)
    ft.header = header

    # Parse all the people
    data = []
    while i < len(lines) and not lines[i].startswith("0 @F"):
        data.append(lines[i])
        i += 1
    persons = parse_persons(data)
    ft.persons = {p.xref_id: p for p in persons}

    # Parse all the families
    data = []
    while i < len(lines) and not lines[i].startswith("0 @S"):
        data.append(lines[i])
        i += 1
    families = parse_families(data)
    ft.families = {f.xref_id: f for f in families}

    # Link the families
    ft.link_families()

    # Parse the sources and repositories
    # TODO: finish adding the sources to a source list
    while i < len(lines) and not lines[i].startswith("0 @T"):
        i += 1

    # Parse the trailer
    trailer = parse_trailer(lines[i:])
    ft.trailer = trailer

    return ft


def parse_persons(data: list[str]) -> list[Person]:
    persons: list[Person] = []
    i = 0
    while i < len(data):
        xref_id = data[i].split(" ")[1]
        person = Person(xref_id)
        i += 1
        p_data = []
        while i < len(data) and not data[i].startswith("0 @"):
            p_data.append(data[i])
            i += 1
        person = parse_person(person, p_data)
        persons.append(person)

    return persons


def parse_person(person: Person, p_data: list[str]) -> Person:
    tag_values = []
    i = 0
    while i < len(p_data):
        line = p_data[i]
        if line == "":
            i += 1
            continue
        level = int(line[0])
        tag = GedcomTag[line.split(" ")[1]]
        value = " ".join(line.split(" ")[2:])
        # some values are multi line
        i += 1
        while i < len(p_data) and len(p_data[i]) > 0 and not p_data[i][0].isdigit():
            # Handle multi-line values
            line = p_data[i]
            value += " " + line
            i += 1

        tv = TagValue(level, tag, value)
        tag_values.append(tv)

    person.parse_tag_values(tag_values)

    return person


def parse_families(data) -> list[Family]:
    families: list[Family] = []

    i = 0
    while i < len(data):
        xref_id = data[i].split(" ")[1]
        family = Family(xref_id)
        i += 1
        f_data = []
        while i < len(data) and not data[i].startswith("0 @"):
            f_data.append(data[i])
            i += 1
        family = parse_family(family, f_data)
        families.append(family)

    return families


def parse_family(family: Family, f_data: list[str]) -> Family:
    tag_values: list[TagValue] = []
    for line in f_data:
        level = int(line.split(" ")[0])
        tag = GedcomTag[line.split(" ")[1]]
        value = " ".join(line.split(" ")[2:])
        tag_values.append(TagValue(level, tag, value))

    for tag_value in tag_values:
        if tag_value.tag == GedcomTag.HUSB:
            family.husb = tag_value.value
        elif tag_value.tag == GedcomTag.WIFE:
            family.wife = tag_value.value
        elif tag_value.tag == GedcomTag.CHIL:
            family.children.append(tag_value.value)
        else:
            family.add_data(tag_value.tag.name, tag_value.value)

    return family


def parse_header(data):
    header = {}
    for line in data:
        tag = line.split(" ")[1]
        value = " ".join(line.split(" ")[2:])
        header[tag] = value

    return header


def parse_trailer(data: list[str]) -> dict[str, str]:
    trailer = {}
    data = data[1:]  # Skip the 0 TRLR line
    for line in data:
        try:
            tag = line.split(" ")[1]
            value = " ".join(line.split(" ")[2:])
            trailer[tag] = value
        except IndexError:
            pass

    return trailer
