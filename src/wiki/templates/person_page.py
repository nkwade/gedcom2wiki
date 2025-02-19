import os
import re
from gedcom.tree import FamilyTree
from gedcom.person import Person
from gedcom.fact import GedcomTag, Fact
from .base_html import html_page
from datetime import datetime
from markupsafe import Markup
import html as html_package
from llm.llama import generate_bio


def extract_year_from_string(date_str: str) -> int | None:
    match = re.search(r"(\d{4})", date_str)
    if match:
        return int(match.group(1))
    return None


from collections import deque


def build_fact_adjacency_bfs(
    root_fact: Fact,
) -> tuple[dict[int, Fact], dict[int, list[int]]]:
    """
    Use BFS to collect every Fact reachable from 'root_fact' and build an adjacency map
    of parent_fact_id -> [child_fact_ids].

    :param root_fact: The top-level Fact for which we want to gather subfacts.
    :return: (facts_map, adjacency_map) where:
             - facts_map is fact_id -> Fact object
             - adjacency_map is fact_id -> list of child_fact_ids
    """
    queue = deque([root_fact])
    facts_map: dict[int, Fact] = {}
    adjacency_map: dict[int, list[int]] = {}

    while queue:
        current = queue.popleft()
        current_id = id(current)

        # If we have already visited this fact, skip it
        if current_id in facts_map:
            continue

        # Record the fact
        facts_map[current_id] = current
        adjacency_map[current_id] = []

        # Enqueue all subfacts
        for sfact in current.sub_facts:
            sfact_id = id(sfact)
            adjacency_map[current_id].append(sfact_id)
            queue.append(sfact)

    return facts_map, adjacency_map


def _path_to_url(path: str) -> str:
    """Convert OS path to URL format with forward slashes"""
    return path.replace(os.sep, "/")


def render_fact_li_bfs(root_fact: Fact, family_tree: FamilyTree) -> str:
    """
    Returns a nested <ul><li>...</li></ul> string for 'root_fact'
    and all subfacts, using BFS under the hood to gather them.
    """
    facts_map, adjacency_map = build_fact_adjacency_bfs(root_fact)

    def build_html(fact_id: int) -> str:
        fact = facts_map[fact_id]

        # Handle different fact types
        if fact.tag == GedcomTag.SOUR:
            # Handle source references like @S500010@
            source_id = fact.value
            if source_id in family_tree.sources:
                source = family_tree.sources[source_id]
                href = _path_to_url(os.path.join("..", "sources", f"{source_id}.html"))
                value_text = f'<a href="{href}">{source.display_name}</a>'
            else:
                value_text = fact.value
        elif fact.tag == GedcomTag.TEXT or fact.tag == GedcomTag.NOTE:
            # Double unescape text content and mark as safe HTML
            unescaped = html_package.unescape(html_package.unescape(fact.value))
            value_text = str(Markup(unescaped))
        else:
            value_text = html_package.unescape(fact.value)

        html = f"<li>{fact.tag.value}: {value_text}"

        children = adjacency_map.get(fact_id, [])
        if children:
            html += "<ul>"
            for child_id in children:
                html += build_html(child_id)
            html += "</ul>"

        html += "</li>"
        return html

    root_id = id(root_fact)
    return f"<ul>{build_html(root_id)}</ul>"


def render_person_page(
    family_tree: FamilyTree, person: Person, use_llm: bool = False
) -> str:
    out_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "out")
    )
    assets_dir = os.path.join(out_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    image_paths = []
    for i, image in enumerate(person.images):
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")

        image_filename = f"{person.xref_id}_{i}.png"
        image_paths.append(image_filename)
        # Note: actual image saving should be handled by the build process,
        # not the template renderer

    name = person.name if person.name else person.xref_id
    sex = person.sex.value if person.sex else "Unknown"
    birth = person.birthday if person.birthday else "Unknown"
    death = person.death if person.death else "Present"

    birth_year = extract_year_from_string(str(birth))
    death_year = extract_year_from_string(str(death))
    if death == "Alive" or death_year is None:
        death_year = datetime.now().year

    fams = person.fams
    famc = person.famc

    families_section = "<h2>Associated Families</h2>"
    if fams or famc:
        families_section += "<table>"
        families_section += "<tr><th>Relationship</th><th>Family</th></tr>"
        for fam_id in fams:
            if fam_id in family_tree.families:
                href = _path_to_url(os.path.join("..", "families", f"{fam_id}.html"))
                families_section += (
                    f'<tr><td>Spouse</td><td><a href="{href}">'
                    f"{family_tree.families[fam_id].name}</a></td></tr>"
                )
        for fam_id in famc:
            if fam_id in family_tree.families:
                href = _path_to_url(os.path.join("..", "families", f"{fam_id}.html"))
                families_section += (
                    f'<tr><td>Child</td><td><a href="{href}">'
                    f"{family_tree.families[fam_id].name}</a></td></tr>"
                )
        families_section += "</table>"
    else:
        families_section += "<p>No associated families found.</p>"

    basic_info = f"""
    <table>
        <tr><th>Name</th><td>{name}</td></tr>
        <tr><th>Sex</th><td>{sex}</td></tr>
        <tr><th>Birth</th><td>{birth}</td></tr>
        <tr><th>Death</th><td>{death}</td></tr>
    </table>
    """

    early_life_facts = []
    mid_life_facts = []
    late_life_facts = []
    other_facts = []

    if birth_year is not None:
        early_end = birth_year + 18
        mid_end = birth_year + 65
        late_end = death_year
    else:
        early_end = None
        mid_end = None
        late_end = None

    for fact in person.facts:
        if (
            fact.tag.name.startswith("_")
            or fact.tag == GedcomTag.OBJE
            or fact.tag == GedcomTag.RIN
            or fact.tag == GedcomTag.FAMC
            or fact.tag == GedcomTag.FAMS
        ):
            continue
        date_fact = None
        for sub in fact.sub_facts:
            if sub.tag == GedcomTag.DATE:
                date_fact = sub
        if date_fact:
            fact_year = extract_year_from_string(date_fact.value)
            if fact_year is not None and birth_year is not None:
                if early_end and fact_year <= early_end:
                    early_life_facts.append(fact)
                elif mid_end and fact_year <= mid_end:
                    mid_life_facts.append(fact)
                elif late_end and fact_year <= late_end:
                    late_life_facts.append(fact)
                else:
                    other_facts.append(fact)
            else:
                other_facts.append(fact)
        else:
            other_facts.append(fact)

    facts_section = ""
    if early_life_facts or mid_life_facts or late_life_facts or other_facts:
        facts_section += "<h2>All Facts</h2>"
        if birth_year is not None:
            if early_life_facts:
                facts_section += f"<h3>Early Life ({birth_year} - {birth_year+18})</h3><ul class='facts'>"
                for f in early_life_facts:
                    facts_section += render_fact_li_bfs(f, family_tree)
                facts_section += "</ul>"

            if mid_life_facts:
                facts_section += f"<h3>Mid Life ({birth_year+19} - {birth_year+65})</h3><ul class='facts'>"
                for f in mid_life_facts:
                    facts_section += render_fact_li_bfs(f, family_tree)
                facts_section += "</ul>"

            if late_life_facts:
                facts_section += f"<h3>Late Life ({birth_year+66} - {death_year})</h3><ul class='facts'>"
                for f in late_life_facts:
                    facts_section += render_fact_li_bfs(f, family_tree)
                facts_section += "</ul>"
        if other_facts:
            facts_section += "<h3>Other Facts</h3><ul class='facts'>"
            for f in other_facts:
                facts_section += render_fact_li_bfs(f, family_tree)
            facts_section += "</ul>"

    image_html = ""
    if image_paths:
        first_image_src = _path_to_url(os.path.join("..", "assets", image_paths[0]))
        image_html = f'<img src="{first_image_src}" alt="{name}" style="max-width:200px; height:auto; border:1px solid #ccc; padding:5px; margin-top:1em;" />'

    info_section = f"""
    <div class="info-panel">
        <h2>Basic Information</h2>
        <div class="info-content">
            <div class="info-table">
                {basic_info}
            </div>
            {image_html}
        </div>
    </div>
    """

    gallery_section = ""
    if image_paths:
        gallery_section = (
            "<h2>Gallery</h2><div style='display:flex; flex-wrap:wrap; gap:1em;'>"
        )
        for img_file in image_paths:
            img_src = _path_to_url(os.path.join("..", "assets", img_file))
            gallery_section += f'<div><img src="{img_src}" alt="{name}" style="max-width:200px; height:auto; border:1px solid #ccc; padding:5px;"/></div>'
        gallery_section += "</div>"

    bio_section = ""
    if use_llm:
        bio = generate_bio(person, family_tree)
        bio_section = f"<h2>Biography</h2><p>{bio}</p>"

    content = f"""
    <h1>{name}</h1>
    {info_section}
    {families_section}
    {bio_section}
    {facts_section}
    {gallery_section}
    <div style="clear:both;"></div>
    """

    missing_citations = []
    facts_needing_citations = [
        GedcomTag.BIRT,
        GedcomTag.DEAT,
        GedcomTag.MARR,
    ]
    for fact in person.facts:
        if (
            not any(sub.tag == GedcomTag.SOUR for sub in fact.sub_facts)
            and fact.tag in facts_needing_citations
        ):
            missing_citations.append(fact)

    if missing_citations:
        content += "<h2>Missing Source Citation</h2><ul>"
        for fact in missing_citations:
            content += f"<li>{fact.tag.value}</li>"
        content += "</ul>"

    return html_page(name, content, depth=1)
