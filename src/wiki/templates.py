from typing import List
from ..gedcom.tree import FamilyTree
from ..gedcom.person import Person
from ..gedcom.family import Family
from ..gedcom.fact import GedcomTag


def html_page(title: str, body_content: str) -> str:
    """A basic HTML wrapper."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>{title}</title>
    <style>
        body {{
            font-family: sans-serif;
            margin: 2em;
        }}
        header {{
            margin-bottom: 2em;
        }}
        nav a {{
            margin-right: 1em;
        }}
        h1, h2, h3 {{
            font-family: sans-serif;
        }}
        table {{
            border-collapse: collapse;
            margin: 1em 0;
        }}
        table, th, td {{
            border: 1px solid #ccc;
            padding: 0.5em;
        }}
        .facts {{
            margin-top: 1em;
        }}
        .facts li {{
            margin-bottom: 0.5em;
        }}
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="../index.html">Home</a>
        </nav>
    </header>
    {body_content}
</body>
</html>
"""


def render_index_page(family_tree: FamilyTree) -> str:
    """Render the main index page with header information and lists of families and people."""
    header_info = "<h2>Header Information</h2><ul>"
    for k, v in family_tree.header.items():
        header_info += f"<li><strong>{k}</strong>: {v}</li>"
    header_info += "</ul>"

    family_list = "<h2>Families</h2><ul>"
    for fam_id, family in family_tree.families.items():
        family_list += f'<li><a href="families/{fam_id}.html">{family.name}</a></li>'
    family_list += "</ul>"

    person_list = "<h2>People</h2><ul>"
    for person_id, person in family_tree.persons.items():
        name_display = person.name if person.name else person_id
        person_list += f'<li><a href="persons/{person_id}.html">{name_display}</a></li>'
    person_list += "</ul>"

    content = f"<h1>Family Tree Index</h1>{header_info}{family_list}{person_list}"
    return html_page("Family Tree Index", content)


def render_family_page(family_tree: FamilyTree, family: Family) -> str:
    """Render a family page with a list of its members and basic details."""
    husb_link = ""
    wife_link = ""
    children_links = []

    if family.husb and family.husb in family_tree.persons:
        husb = family_tree.persons[family.husb]
        husb_name = husb.name if husb.name else family.husb
        husb_link = f'<a href="../persons/{family.husb}.html">{husb_name}</a>'
    if family.wife and family.wife in family_tree.persons:
        wife = family_tree.persons[family.wife]
        wife_name = wife.name if wife.name else family.wife
        wife_link = f'<a href="../persons/{family.wife}.html">{wife_name}</a>'

    for c in family.children:
        if c in family_tree.persons:
            child = family_tree.persons[c]
            child_name = child.name if child.name else c
            children_links.append(f'<a href="../persons/{c}.html">{child_name}</a>')

    # Table of members
    members_section = "<h2>Family Members</h2><table><tr><th>Role</th><th>Name</th><th>Birth</th><th>Death</th><th>Sex</th></tr>"

    def person_row(role, p: Person):
        birth = p.birthday if p.birthday else ""
        death = p.death if p.death else ""
        sex = p.sex.value if p.sex else ""
        name_display = p.name if p.name else p.xref_id
        return f"<tr><td>{role}</td><td><a href='../persons/{p.xref_id}.html'>{name_display}</a></td><td>{birth}</td><td>{death}</td><td>{sex}</td></tr>"

    if family.husb and family.husb in family_tree.persons:
        members_section += person_row("Husband", family_tree.persons[family.husb])
    if family.wife and family.wife in family_tree.persons:
        members_section += person_row("Wife", family_tree.persons[family.wife])
    for c in family.children:
        if c in family_tree.persons:
            members_section += person_row("Child", family_tree.persons[c])

    members_section += "</table>"

    # Facts about the family if any
    facts_section = ""
    if family.facts or family.data:
        facts_section = "<h2>Family Facts</h2><ul>"
        for fact in family.facts:
            facts_section += f"<li>{fact}</li>"
        for tag, vals in family.data.items():
            for v in vals:
                facts_section += f"<li>{tag}: {v}</li>"
        facts_section += "</ul>"

    content = f"<h1>{family.xref_id}</h1>{members_section}{facts_section}"
    return html_page(f"Family {family.xref_id}", content)


def render_person_page(family_tree: FamilyTree, person: Person) -> str:
    """Render a person page with all their details and associated families."""
    name = person.name if person.name else person.xref_id
    sex = person.sex.value if person.sex else "Unknown"
    birth = person.birthday if person.birthday else "Unknown"
    death = person.death if person.death else "Present"

    # Associated families
    fams = person.fams  # as spouse
    famc = person.famc  # as child

    families_section = "<h2>Associated Families</h2><ul>"
    for fam_id in fams:
        if fam_id in family_tree.families:
            families_section += (
                f'<li>As spouse: <a href="../families/{fam_id}.html">{family_tree.families[fam_id].name}</a></li>'
            )
    for fam_id in famc:
        if fam_id in family_tree.families:
            families_section += (
                f'<li>As child: <a href="../families/{fam_id}.html">{family_tree.families[fam_id].name}</a></li>'
            )
    families_section += "</ul>"

    # Basic info
    basic_info = f"""
    <h2>Basic Information</h2>
    <table>
        <tr><th>Name</th><td>{name}</td></tr>
        <tr><th>Sex</th><td>{sex}</td></tr>
        <tr><th>Birth</th><td>{birth}</td></tr>
        <tr><th>Death</th><td>{death}</td></tr>
    </table>
    """

    # All facts
    facts_section = "<h2>All Facts</h2><ul class='facts'>"
    for fact in person.facts:
        # fact is Fact object: tag=GedcomTag, value=str, sub_facts=dict
        sub_facts_str = ""
        if fact.sub_facts:
            sub_facts_str = "<ul>"
            for sf_tag, sf_value in fact.sub_facts.items():
                sub_facts_str += f"<li>{sf_tag.value}: {sf_value.value}</li>"
            sub_facts_str += "</ul>"
        facts_section += f"<li>{fact.tag.value}: {fact.value}{sub_facts_str}</li>"
    facts_section += "</ul>"

    content = f"<h1>{name}</h1>{basic_info}{families_section}{facts_section}"
    return html_page(name, content)
