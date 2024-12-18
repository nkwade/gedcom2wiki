from ...gedcom.tree import FamilyTree
from ...gedcom.person import Person
from .base_html import html_page


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
            families_section += f'<li>As spouse: <a href="../families/{fam_id}.html">{family_tree.families[fam_id].name}</a></li>'
    for fam_id in famc:
        if fam_id in family_tree.families:
            families_section += f'<li>As child: <a href="../families/{fam_id}.html">{family_tree.families[fam_id].name}</a></li>'
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
