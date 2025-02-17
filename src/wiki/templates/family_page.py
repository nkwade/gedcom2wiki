from gedcom.tree import FamilyTree
from gedcom.family import Family
from gedcom.person import Person
from gedcom.fact import Fact, GedcomTag
from wiki.templates.base_html import html_page
import html as html_package
from markupsafe import Markup


def render_family_chart(family_tree: FamilyTree, family: Family) -> str:
    """Generate an SVG chart showing family structure with:
    - dynamic box widths based on name length
    - a line connecting the parents on their inside edges
    - a vertical line from parent midpoint down
    - horizontally spaced child boxes so they don't overlap.
    """

    # -----------------------------------------------------------------------
    # 1. Gather Names
    # -----------------------------------------------------------------------
    father_name = ""
    mother_name = ""
    if family.husb and family.husb in family_tree.persons:
        father_name = family_tree.persons[family.husb].name or "Unknown Father"
    if family.wife and family.wife in family_tree.persons:
        mother_name = family_tree.persons[family.wife].name or "Unknown Mother"

    children_names = [
        family_tree.persons[c].name if c in family_tree.persons else "Unknown Child"
        for c in family.children
    ]

    # -----------------------------------------------------------------------
    # 2. SVG / Box Layout Constants
    # -----------------------------------------------------------------------
    svg_width = 1000
    svg_height = 600
    box_height = 40
    vertical_gap = 50  # gap between parent box line and child branch line
    spacing_between_children = 40  # horizontal gap between child boxes
    PARENT_GAP = 100  # extra horizontal gap between father and mother if both present

    # Estimation function for text width:
    # We'll do length_of_text * CHAR_WIDTH + PADDING
    # Then ensure at least MIN_WIDTH
    CHAR_WIDTH = 7  # approximate width of each character
    PADDING = 20  # left/right padding inside the box
    MIN_WIDTH = 120  # minimum box width

    def measure_text_width(text: str) -> int:
        approximate = len(text) * CHAR_WIDTH + PADDING
        return max(approximate, MIN_WIDTH)

    # -----------------------------------------------------------------------
    # 3. Compute Dynamic Box Widths for Father & Mother
    # -----------------------------------------------------------------------
    father_box_width = measure_text_width(father_name) if father_name else 0
    mother_box_width = measure_text_width(mother_name) if mother_name else 0

    # -----------------------------------------------------------------------
    # 4. Place Parents (father_x, mother_x)
    #    - If both exist: father at 250, mother at father_right_x + PARENT_GAP
    #    - If only father, center father
    #    - If only mother, center mother
    # -----------------------------------------------------------------------
    parent_y = 50
    father_x: float | None = None
    mother_x: float | None = None

    if father_name and mother_name:
        # Both parents exist
        father_x = 250
        father_right_x = father_x + father_box_width
        mother_x = father_right_x + PARENT_GAP
    elif father_name and not mother_name:
        # Only father
        father_x = (svg_width - father_box_width) / 2.0
    elif mother_name and not father_name:
        # Only mother
        mother_x = (svg_width - mother_box_width) / 2.0

    # -----------------------------------------------------------------------
    # 5. Create <rect> + <text> Helper
    # -----------------------------------------------------------------------
    def create_person_box(x: float, y: float, w: float, h: float, name: str) -> str:
        rect = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="black" />'
        text_x = x + w / 2
        text_y = y + h / 2 + 5  # approximate centering in vertical dimension
        text = f'<text x="{text_x}" y="{text_y}" text-anchor="middle" alignment-baseline="middle">{name}</text>'
        return rect + "\n" + text

    svg_elements = []
    line_elements = []

    # -----------------------------------------------------------------------
    # 6. Draw Parent Boxes
    # -----------------------------------------------------------------------
    if father_x is not None and father_name:
        svg_elements.append(
            create_person_box(
                father_x, parent_y, father_box_width, box_height, father_name
            )
        )
    if mother_x is not None and mother_name:
        svg_elements.append(
            create_person_box(
                mother_x, parent_y, mother_box_width, box_height, mother_name
            )
        )

    # -----------------------------------------------------------------------
    # 7. Connect Parents (Inside Edges) or Single Parent
    # -----------------------------------------------------------------------
    parents_mid_x = None
    parents_mid_y = parent_y + box_height / 2

    both_parents = (father_x is not None and father_name) and (
        mother_x is not None and mother_name
    )
    if both_parents:
        # Father right edge
        father_right_x = father_x + father_box_width  # type: ignore
        father_mid_y = parents_mid_y
        # Mother left edge
        mother_left_x = mother_x
        mother_mid_y = parents_mid_y

        # Horizontal line: father’s right edge -> mother’s left edge
        line_elements.append(
            f'<line x1="{father_right_x}" y1="{father_mid_y}" x2="{mother_left_x}" y2="{mother_mid_y}" stroke="black" />'
        )

        # Midpoint of that line:
        parents_mid_x = (father_right_x + mother_left_x) / 2  # type: ignore

    else:
        # If only father
        if father_x is not None and father_name:
            parents_mid_x = father_x + father_box_width / 2
        # If only mother
        elif mother_x is not None and mother_name:
            parents_mid_x = mother_x + mother_box_width / 2
        # If neither, no parents at all
        else:
            parents_mid_x = None

    # -----------------------------------------------------------------------
    # 8. Vertical line down from the parents’ midpoint
    # -----------------------------------------------------------------------
    if parents_mid_x is not None:
        top_branch_y = parents_mid_y + vertical_gap
        line_elements.append(
            f'<line x1="{parents_mid_x}" y1="{parents_mid_y}" x2="{parents_mid_x}" y2="{top_branch_y}" stroke="black" />'
        )
    else:
        top_branch_y = None

    # -----------------------------------------------------------------------
    # 9. Children Layout (Dynamic box widths + consistent spacing)
    # -----------------------------------------------------------------------
    if top_branch_y is not None and children_names:
        # A. Compute each child's box width
        child_widths = [
            measure_text_width(name) for name in children_names if name is not None
        ]
        n_children = len(children_names)

        # B. Compute total width of all child boxes + spacing
        total_children_width = sum(child_widths) + spacing_between_children * (
            n_children - 1
        )

        # C. Center that row under parents_mid_x
        children_row_left = parents_mid_x - (total_children_width / 2)  # type: ignore
        child_box_y = top_branch_y + vertical_gap

        # D. Draw a horizontal "child branch" line from the leftmost child center to the rightmost child center
        #    We need the x-coord of the center of the 1st and last child box
        #    But first, let's figure out each child's x-left.
        child_x_positions = []
        current_x = children_row_left
        for w in child_widths:
            child_x_positions.append(current_x)
            current_x += w + spacing_between_children
        # The center of child i = child_x_positions[i] + child_widths[i] / 2

        # E. Horizontal line
        first_child_center_x = child_x_positions[0] + child_widths[0] / 2
        last_child_center_x = child_x_positions[-1] + child_widths[-1] / 2
        child_branch_y = top_branch_y  # horizontal line at top_branch_y
        line_elements.append(
            f'<line x1="{first_child_center_x}" y1="{child_branch_y}" '
            f'x2="{last_child_center_x}" y2="{child_branch_y}" stroke="black" />'
        )

        # F. For each child, draw vertical line + box
        for i, name in enumerate(children_names):
            cx_left = child_x_positions[i]
            w = child_widths[i]
            child_center_x = cx_left + w / 2

            # vertical line from child_branch_y to the top of the child's box
            line_elements.append(
                f'<line x1="{child_center_x}" y1="{child_branch_y}" '
                f'x2="{child_center_x}" y2="{child_box_y}" stroke="black" />'
            )

            # box + text
            svg_elements.append(
                create_person_box(
                    cx_left, child_box_y, w, box_height, name if name else "Unknown"
                )
            )

    # -----------------------------------------------------------------------
    # 10. Combine everything into the final SVG
    # -----------------------------------------------------------------------
    svg = f"""
<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
    {'\n'.join(svg_elements)}
    {'\n'.join(line_elements)}
</svg>
"""
    return svg


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

    def render_fact(fact: Fact):
        value_text = ""
        if fact.value:
            if fact.tag == GedcomTag.TEXT or fact.tag == GedcomTag.NOTE:
                # Double unescape: first for HTML entities in the stored value,
                # then for the HTML entities in the content itself
                unescaped = html_package.unescape(html_package.unescape(fact.value))
                value_text = f": {Markup(unescaped)}"
            elif fact.tag == GedcomTag.SOUR:
                # Handle source references like @S500010@
                source_id = fact.value
                if source_id in family_tree.sources:
                    source = family_tree.sources[source_id]
                    value_text = f': <a href="../sources/{source_id}.html">{source.display_name}</a>'
                else:
                    value_text = f": {fact.value}"
            else:
                value_text = f": {fact.value}"

        html_content = f"<li>{fact.tag.value}{value_text}"

        if fact.sub_facts:
            html_content += "<ul>"
            for sub_fact in fact.sub_facts:
                html_content += render_fact(sub_fact)
            html_content += "</ul>"
        html_content += "</li>"
        return html_content

    facts_section = ""
    if family.facts:
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

    # Add family chart visualization
    chart = render_family_chart(family_tree, family)
    content = f"""
    <h1>Family of {family.name}</h1>
    {members_section}
    {facts_section}
    <h2>Family Chart</h2>
    {chart}
    """
    return html_page(f"Family {family.name}", content, depth=1)
