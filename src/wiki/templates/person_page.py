import os
import re
from gedcom.tree import FamilyTree
from gedcom.person import Person
from gedcom.fact import GedcomTag, Fact
from .base_html import html_page
from datetime import datetime


def extract_year_from_string(date_str: str) -> int | None:
    match = re.search(r"(\d{4})", date_str)
    if match:
        return int(match.group(1))
    return None


def render_fact_li(fact: Fact) -> str:
    sub_facts_str = ""
    if fact.sub_facts:
        sub_facts_str = "<ul>"
        for sf_fact in fact.sub_facts:
            sub_facts_str += f"<li>{sf_fact.tag.value}: {sf_fact.value}</li>"
        sub_facts_str += "</ul>"
    return f"<li>{fact.tag.value}: {fact.value}{sub_facts_str}</li>"


def render_person_page(family_tree: FamilyTree, person: Person) -> str:
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
        image_path = os.path.join(assets_dir, image_filename)
        image.save(image_path, format="PNG")
        image_paths.append(image_filename)

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
                families_section += (
                    f"<tr><td>Spouse</td><td><a href='../families/{fam_id}.html'>"
                    f"{family_tree.families[fam_id].name}</a></td></tr>"
                )
        for fam_id in famc:
            if fam_id in family_tree.families:
                families_section += (
                    f"<tr><td>Child</td><td><a href='../families/{fam_id}.html'>"
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
        date_fact = None
        for sub in fact.sub_facts:
            if sub.tag == GedcomTag.DATE:
                date_fact = sub
        if date_fact:
            fact_year = extract_year_from_string(date_fact.value)
            if fact_year is not None and birth_year is not None:
                if fact_year <= early_end:  # type: ignore
                    early_life_facts.append(fact)
                elif fact_year <= mid_end:  # type: ignore
                    mid_life_facts.append(fact)
                elif fact_year <= late_end:  # type: ignore
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
                    facts_section += render_fact_li(f)
                facts_section += "</ul>"

            if mid_life_facts:
                facts_section += f"<h3>Mid Life ({birth_year+19} - {birth_year+65})</h3><ul class='facts'>"
                for f in mid_life_facts:
                    facts_section += render_fact_li(f)
                facts_section += "</ul>"

            if late_life_facts:
                facts_section += f"<h3>Late Life ({birth_year+66} - {death_year})</h3><ul class='facts'>"
                for f in late_life_facts:
                    facts_section += render_fact_li(f)
                facts_section += "</ul>"
        if other_facts:
            facts_section += "<h3>Other Facts</h3><ul class='facts'>"
            for f in other_facts:
                facts_section += render_fact_li(f)
            facts_section += "</ul>"

    image_html = ""
    if image_paths:
        first_image_src = f"../assets/{image_paths[0]}"
        image_html = f'<img src="{first_image_src}" alt="{name}" style="max-width:200px; height:auto; border:1px solid #ccc; padding:5px; margin-top:1em;" />'

    info_section = f"""
    <div style="float:right; width:300px; margin-left:1em;">
        <h2>Basic Information</h2>
        {basic_info}
        {image_html}
    </div>
    """

    gallery_section = ""
    if image_paths:
        gallery_section = (
            "<h2>Gallery</h2><div style='display:flex; flex-wrap:wrap; gap:1em;'>"
        )
        for img_file in image_paths:
            img_src = f"../assets/{img_file}"
            gallery_section += f'<div><img src="{img_src}" alt="{name}" style="max-width:200px; height:auto; border:1px solid #ccc; padding:5px;"/></div>'
        gallery_section += "</div>"

    content = f"""
    <h1>{name}</h1>
    {info_section}
    {families_section}
    {facts_section}
    {gallery_section}
    <div style="clear:both;"></div>
    """

    return html_page(name, content)
