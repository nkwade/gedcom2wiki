import os
import re
from wiki.templates.base_html import html_page
from gedcom.tree import FamilyTree


def render_report_page(data_validation_html: str, family_tree: FamilyTree) -> str:
    """Render the data validation report into an HTML page with hyperlinks for person/family IDs."""

    def replace_tag(match):
        tag_type = match.group(1)
        if tag_type == "I":
            person = family_tree.persons.get(match.group(0))
            name = person.name if person and person.name else match.group(0)
            return f'<a href="./persons/{match.group(0)}.html">{name}</a>'
        elif tag_type == "F":
            family = family_tree.families.get(match.group(0))
            name = family.name if family and family.name else match.group(0)
            return f'<a href="./families/{match.group(0)}.html">{name}</a>'
        return match.group(0)  # No change if not I or F

    # Replace @Ixxx@ and @Fxxx@ with hyperlinks
    data_validation_html = re.sub(r"@([IF])(\w+)@", replace_tag, data_validation_html)

    content = f"""
    <h1>Data Validation Report</h1>
    {data_validation_html}
    """
    return html_page("Data Validation Report", content, depth=0)
