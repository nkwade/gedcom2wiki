from .base_html import html_page
from gedcom.tree import FamilyTree, Fact


def render_index_page(family_tree: FamilyTree) -> str:
    """Render the main index page with header information and lists of families, people, and sources."""
    header_info = "<h2>Family Tree Information</h2>"

    # Handle the header as a single Fact or None
    if family_tree.header:
        header_info += (
            f"<p>{family_tree.header.tag.value}: {family_tree.header.value}</p>"
        )
        if family_tree.header.sub_facts:
            header_info += "<ul>"
            for sfact in family_tree.header.sub_facts:
                header_info += f"<li>{sfact.tag.value}: {sfact.value}</li>"
            header_info += "</ul>"
    else:
        header_info += "<p>No header found.</p>"

    # If desired, we could also show trailer info similarly
    if family_tree.trailer:
        header_info += f"<h3>Trailer Information</h3><p>{family_tree.trailer.tag.value}: {family_tree.trailer.value}</p>"
        if family_tree.trailer.sub_facts:
            header_info += "<ul>"
            for sfact in family_tree.trailer.sub_facts:
                header_info += f"<li>{sfact.tag.value}: {sfact.value}</li>"
            header_info += "</ul>"

    family_list = "<h2>Families</h2><ul>"
    for fam_id, family in family_tree.families.items():
        family_list += f'<li><a href="families/{fam_id}.html">{family.name}</a></li>'
    family_list += "</ul>"

    person_list = "<h2>People</h2><ul>"
    # Sort people by last word in their name if available
    sorted_persons = sorted(
        family_tree.persons.items(),
        key=lambda item: (
            item[1].name.split()[-1]
            if item[1].name and item[1].name.split()
            else item[0]
        ),
    )
    for person_id, person in sorted_persons:
        name_display = person.name if person.name else person_id
        person_list += f'<li><a href="persons/{person_id}.html">{name_display}</a></li>'
    person_list += "</ul>"

    source_list = "<h2>Sources</h2><ul>"
    sorted_sources = sorted(
        family_tree.sources.items(),
        key=lambda item: item[1].title if item[1].title else item[0],
    )
    for source_id, source in sorted_sources:
        title_display = source.title if source.title else source_id
        source_list += (
            f'<li><a href="sources/{source_id}.html">{title_display}</a></li>'
        )
    source_list += "</ul>"

    content = (
        f"<h1>Family Tree Index</h1>"
        f"{header_info}"
        f"{family_list}"
        f"{person_list}"
        f"{source_list}"
    )
    return html_page("Family Tree Wiki", content)
