from gedcom.tree import FamilyTree
from gedcom.source import Source
from .base_html import html_page


def render_source_page(family_tree: FamilyTree, source: Source) -> str:
    title = source.title if source.title else source.xref_id
    origin = source.origin if source.origin else "Unknown"
    publisher = source.publisher if source.publisher else "Unknown"

    basic_info = f"""
    <h2>Basic Information</h2>
    <table>
        <tr><th>Title</th><td>{title}</td></tr>
        <tr><th>Origin</th><td>{origin}</td></tr>
        <tr><th>Publisher</th><td>{publisher}</td></tr>
    </table>
    """

    content = f"<h1>{title}</h1>{basic_info}"
    return html_page(title, content)
