from .person import Person
from .family import Family
from .tree import FamilyTree
from .fact import GedcomTag, TagValue, Fact
from .source import Source


def parse_gedcom(gedcom_text: str) -> FamilyTree:
    lines = gedcom_text.splitlines()
    ft = FamilyTree()

    # Initialize variables
    i = 0
    start_header = None
    start_people = None
    start_families = None
    start_sources = None
    start_trailer = None

    # Loop through lines to find section starts
    while i < len(lines):
        line = lines[i]
        if start_header is None and not line.startswith("0 @"):
            start_header = i
        elif start_people is None and line.startswith("0 @I"):
            start_people = i
        elif start_families is None and line.startswith("0 @F"):
            start_families = i
        elif start_sources is None and line.startswith("0 @S"):
            start_sources = i
        elif start_trailer is None and line.startswith("0 TRLR"):
            start_trailer = i
            break
        i += 1

    # Parse the header
    if start_header is not None and start_people is not None:
        header_data = lines[start_header:start_people]
        header = parse_header(header_data)
        ft.header = header

    # Parse all the people
    if start_people is not None:
        if start_families is not None:
            people_data = lines[start_people:start_families]
        elif start_trailer is not None:
            people_data = lines[start_people:start_trailer]
        else:
            people_data = lines[start_people:]
        persons = parse_persons(people_data)
        ft.persons = {p.xref_id: p for p in persons}

    # Parse all the families
    if start_families is not None:
        if start_sources is not None:
            families_data = lines[start_families:start_sources]
        else:
            families_data = lines[start_families:]
        families = parse_families(families_data)
        ft.families = {f.xref_id: f for f in families}

    # Link the families
    ft.link_families()

    if start_sources is not None:
        if start_trailer is not None:
            source_data = lines[start_sources:start_trailer]
        else:
            source_data = lines[start_sources:]

        sources = parse_sources(source_data)

        ft.sources = sources

    # Parse the trailer
    if start_trailer is not None:
        trailer_data = lines[start_trailer:]
        trailer = parse_trailer(trailer_data)
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


def parse_sources(data: list[str]) -> dict:
    sources: dict[str, Source] = {}  # key: xref_id, value: Source
    queue: list[tuple[int, Fact]] = []  # level, Fact
    curr_source: Source = None  # type: ignore

    i = 0
    while i < len(data):
        line = data[i].split(" ")
        level = int(line[0])
        if level == 0:  # source
            if curr_source is not None:
                curr_source.parse_facts()
            curr_source = Source(line[1])
            sources[line[1]] = curr_source
        else:  # fact
            fact = Fact(GedcomTag[line[1]], " ".join(line[2:]))
            while len(queue) > 0 and level <= queue[-1][0]:
                l, done = queue.pop(-1)
                if l == 1:
                    curr_source.facts.append(done)

            if len(queue) > 0:
                queue[-1][1].sub_facts[fact.tag] = fact

            queue.append((level, fact))
        i += 1

    return sources


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
