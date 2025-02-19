import os
from pathlib import Path, PurePosixPath
from gedcom.tree import FamilyTree
from gedcom.family import Family
from gedcom.person import Person
from gedcom.fact import Fact, GedcomTag
from wiki.templates.base_html import html_page
import html as html_package
from markupsafe import Markup
from wiki.templates.person_page import render_fact_li_bfs


def _path_to_url(path: str | Path) -> str:
    """Convert OS path to URL format with forward slashes"""
    # Convert the path to a PurePosixPath to ensure forward slashes
    return str(PurePosixPath(path))


def _make_relative_url(*parts: str) -> str:
    """Create a URL-style path from parts"""
    return str(PurePosixPath(*parts))


def render_family_chart(family_tree: FamilyTree, family: Family) -> str:
    """Generate an HTML/CSS based family chart that's responsive and matches site theme."""

    # Gather family members
    father_name = "Unknown Father"
    father_id = None
    mother_name = "Unknown Mother"
    mother_id = None

    if family.husb and family.husb in family_tree.persons:
        father = family_tree.persons[family.husb]
        father_name = father.name or "Unknown Father"
        father_id = family.husb

    if family.wife and family.wife in family_tree.persons:
        mother = family_tree.persons[family.wife]
        mother_name = mother.name or "Unknown Mother"
        mother_id = family.wife

    children = []
    for child_id in family.children:
        if child_id in family_tree.persons:
            child = family_tree.persons[child_id]
            children.append({"name": child.name or "Unknown Child", "id": child_id})

    # Generate HTML structure with CSS Grid layout
    chart = """
        <div class="family-chart">
            <div class="parents">
                <div class="parent-wrapper">
    """

    # Add father
    if father_id:
        href = _make_relative_url("..", "persons", f"{father_id}.html")
        chart += f"""
            <div class="parent father">
                <a href="{href}" class="member-card">
                    {father_name}
                </a>
            </div>
        """
    else:
        chart += f"""
            <div class="parent father">
                <div class="member-card empty">
                    {father_name}
                </div>
            </div>
        """

    # Add mother
    if mother_id:
        href = _make_relative_url("..", "persons", f"{mother_id}.html")
        chart += f"""
            <div class="parent mother">
                <a href="{href}" class="member-card">
                    {mother_name}
                </a>
            </div>
        """
    else:
        chart += f"""
            <div class="parent mother">
                <div class="member-card empty">
                    {mother_name}
                </div>
            </div>
        """

    chart += """
                </div>
            </div>
    """

    # Add children section
    if children:
        chart += """
            <div class="children">
                <div class="child-wrapper">
        """

        for child in children:
            href = _make_relative_url("..", "persons", f"{child['id']}.html")
            chart += f"""
                <div class="child">
                    <a href="{href}" class="member-card">
                        {child['name']}
                    </a>
                </div>
            """

        chart += """
                </div>
            </div>
        """

    chart += "</div>"

    # Add CSS styles specific to the family chart
    styles = """
        <style>
            .family-chart {
                margin: 2rem 0;
                padding: 2rem;
                background: var(--bg-secondary);
                border-radius: 8px;
                box-shadow: var(--card-shadow);
            }

            .parents, .children {
                display: flex;
                justify-content: center;
                position: relative;
            }

            .parent-wrapper, .child-wrapper {
                display: flex;
                gap: 2rem;
                flex-wrap: wrap;
                justify-content: center;
            }

            .parents::after {
                content: "";
                position: absolute;
                bottom: -2rem;
                left: 50%;
                transform: translateX(-50%);
                width: 2px;
                height: 2rem;
                background: var(--accent);
            }

            .children {
                margin-top: 2rem;
                position: relative;
            }

            .children::before {
                content: "";
                position: absolute;
                top: -2rem;
                left: 50%;
                transform: translateX(-50%);
                width: 50%;
                height: 2px;
                background: var(--accent);
            }

            .member-card {
                display: block;
                padding: 1rem 1.5rem;
                background: var(--bg-primary);
                border: 2px solid var(--accent);
                border-radius: 6px;
                color: var(--text-primary);
                text-decoration: none;
                transition: all 0.2s;
                min-width: 200px;
                text-align: center;
            }

            .member-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(79, 109, 245, 0.2);
                border-color: var(--accent-hover);
            }

            .member-card.empty {
                border-style: dashed;
                opacity: 0.7;
            }

            @media (max-width: 768px) {
                .parent-wrapper, .child-wrapper {
                    flex-direction: column;
                    gap: 1rem;
                }

                .parents::after {
                    height: 3rem;
                    bottom: -3rem;
                }

                .children {
                    margin-top: 3rem;
                }

                .member-card {
                    min-width: unset;
                    width: 100%;
                }
            }
        </style>
    """

    return styles + chart


def render_family_page(family_tree: FamilyTree, family: Family) -> str:
    husb_link = ""
    wife_link = ""
    children_links = []

    if family.husb and family.husb in family_tree.persons:
        husb = family_tree.persons[family.husb]
        husb_name = husb.name if husb.name else family.husb
        href = _make_relative_url("..", "persons", f"{family.husb}.html")
        husb_link = f'<a href="{href}">{husb_name}</a>'
    if family.wife and family.wife in family_tree.persons:
        wife = family_tree.persons[family.wife]
        wife_name = wife.name if wife.name else family.wife
        href = _make_relative_url("..", "persons", f"{family.wife}.html")
        wife_link = f'<a href="{href}">{wife_name}</a>'

    for c in family.children:
        if c in family_tree.persons:
            child = family_tree.persons[c]
            child_name = child.name if child.name else c
            href = _make_relative_url("..", "persons", f"{c}.html")
            children_links.append(f'<a href="{href}">{child_name}</a>')

    members_section = "<h2>Family Members</h2><table><tr><th>Role</th><th>Name</th><th>Birth</th><th>Death</th><th>Sex</th></tr>"

    def person_row(role, p: Person):
        birth = p.birthday if p.birthday else ""
        death = p.death if p.death else ""
        sex = p.sex.value if p.sex else ""
        name_display = p.name if p.name else p.xref_id
        href = _make_relative_url("..", "persons", f"{p.xref_id}.html")
        return f'<tr><td>{role}</td><td><a href="{href}">{name_display}</a></td><td>{birth}</td><td>{death}</td><td>{sex}</td></tr>'

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
        facts_section = '<h2>Family Facts</h2><div class="panel"><ul class="facts">'
        for fact in family.facts:
            if (
                fact.tag.name.startswith("_")
                or fact.tag == GedcomTag.OBJE
                or fact.tag == GedcomTag.RIN
                or fact.tag == GedcomTag.FAMC
                or fact.tag == GedcomTag.FAMS
            ):
                continue
            facts_section += render_fact_li_bfs(fact, family_tree)
        facts_section += "</ul></div>"

    # Add family chart visualization
    try:
        chart = render_family_chart(family_tree, family)
    except:
        print("Unable to generate family chart")
        chart = ""

    content = "".join(
        [
            "<h1>Family of ",
            family.name if family.name else "Unknown Family",
            "</h1>\n",
            members_section,
            "\n",
            facts_section,
            "\n",
            "<h2>Family Chart</h2>\n",
            chart,
        ]
    )

    return html_page(f"Family {family.name}", content, depth=1)
