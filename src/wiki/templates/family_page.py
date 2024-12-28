from gedcom.tree import FamilyTree
from gedcom.family import Family
from gedcom.person import Person
from gedcom.fact import Fact, GedcomTag
from wiki.templates.base_html import html_page


def render_family_page(family_tree: FamilyTree, family: Family) -> str:
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

    members_section = "<h2>Family Members</h2><table><tr><th>Role</th><th>Name</th><th>Birth</th><th>Death</th><th>Sex</th></tr>"

    def person_row(role, p: Person):
        birth = p.birthday if p.birthday else ""
        death = p.death if p.death else ""
        sex = p.sex.value if p.sex else ""
        name_display = p.name if p.name else p.xref_id
        return f"<tr><td>{role}</td><td><a href='../persons/{p.xref_id}.html'>{name_display}</a></td><td>{birth}</td><td>{death}</td><td>{sex}</td></tr>"

    if family.husb and family.husb in family_tree.persons:
        members_section += person_row("Father", family_tree.persons[family.husb])
    if family.wife and family.wife in family_tree.persons:
        members_section += person_row("Mother", family_tree.persons[family.wife])
    for c in family.children:
        if c in family_tree.persons:
            members_section += person_row("Child", family_tree.persons[c])

    members_section += "</table>"

    facts_section = ""
    if family.facts:

        def render_fact(fact: Fact):
            html = f"<li>{fact.tag.value}: {fact.value}"
            if fact.sub_facts:
                html += "<ul>"
                for sub_fact in fact.sub_facts:
                    html += render_fact(sub_fact)
                html += "</ul>"
            html += "</li>"
            return html

        facts_section = "<h2>Family Facts</h2><ul>"
        for fact in family.facts:
            if (
                fact.tag.name.startswith("_")
                or fact.tag == GedcomTag.OBJE
                or fact.tag == GedcomTag.RIN
                or fact.tag == GedcomTag.FAMC
                or fact.tag == GedcomTag.FAMS
            ):
                continue
            facts_section += render_fact(fact)
        facts_section += "</ul>"

    content = f"<h1>Family Of {family.name}</h1>{members_section}{facts_section}"
    return html_page(f"Family {family.name}", content, depth=1)
