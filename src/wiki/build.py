import os
from .templates import (
    render_index_page,
    render_family_page,
    render_person_page,
    render_source_page,
)

from gedcom.tree import FamilyTree


def generate_wiki_pages(family_tree: FamilyTree, output_path: str) -> None:
    """
    Generate static HTML pages from the FamilyTree data structure.

    :param family_tree: A FamilyTree object as parsed from the GEDCOM file.
    :param output_path: The directory where the HTML pages will be generated.
    """
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)
    families_dir = os.path.join(output_path, "families")
    persons_dir = os.path.join(output_path, "persons")
    sources_dir = os.path.join(output_path, "sources")
    os.makedirs(families_dir, exist_ok=True)
    os.makedirs(persons_dir, exist_ok=True)
    os.makedirs(sources_dir, exist_ok=True)

    # Generate index page
    index_html = render_index_page(family_tree)
    with open(os.path.join(output_path, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # Generate family pages
    for fam_id, family in family_tree.families.items():
        family_html = render_family_page(family_tree, family)
        with open(
            os.path.join(families_dir, f"{fam_id}.html"), "w", encoding="utf-8"
        ) as f:
            f.write(family_html)

    # Generate person pages
    for person_id, person in family_tree.persons.items():
        person_html = render_person_page(family_tree, person)
        with open(
            os.path.join(persons_dir, f"{person_id}.html"), "w", encoding="utf-8"
        ) as f:
            f.write(person_html)

    # Generate source pages
    for source_id, source in family_tree.sources.items():
        source_html = render_source_page(family_tree, source)
        with open(
            os.path.join(sources_dir, f"{source_id}.html"), "w", encoding="utf-8"
        ) as f:
            f.write(source_html)
