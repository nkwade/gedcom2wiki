from datetime import datetime
from collections import defaultdict
from gedcom.tree import FamilyTree


def validate_family_tree(family_tree: FamilyTree) -> dict:
    """
    Perform global and structural checks for the entire family tree.
    Returns a dictionary of issues categorized by type.
    """
    current_year = datetime.now().year
    issues = defaultdict(list)

    # Cyclical Relationships
    visited = set()

    def detect_cycles(person_id, ancestors):
        if person_id in ancestors:
            issues["Cyclical Relationships"].append(
                f"Person {person_id} is part of a cycle in the tree."
            )
            return

        if person_id in visited:
            return

        visited.add(person_id)
        ancestors.add(person_id)

        if person_id in family_tree.persons:
            person = family_tree.persons[person_id]
            for fam_id in person.famc:
                if fam_id in family_tree.families:
                    family = family_tree.families[fam_id]
                    if family.husb:
                        detect_cycles(family.husb, ancestors)
                    if family.wife:
                        detect_cycles(family.wife, ancestors)

        ancestors.remove(person_id)

    for person_id in family_tree.persons:
        detect_cycles(person_id, set())

    # Missing or Broken Links
    for family_id, family in family_tree.families.items():
        if family.husb and family.husb not in family_tree.persons:
            issues["Broken Links"].append(
                f"Family {family_id} references missing husband {family.husb}."
            )
        if family.wife and family.wife not in family_tree.persons:
            issues["Broken Links"].append(
                f"Family {family_id} references missing wife {family.wife}."
            )
        for child_id in family.children:
            if child_id not in family_tree.persons:
                issues["Broken Links"].append(
                    f"Family {family_id} references missing child {child_id}."
                )

    for person_id, person in family_tree.persons.items():
        for fam_id in person.famc + person.fams:
            if fam_id not in family_tree.families:
                issues["Broken Links"].append(
                    f"Person {person_id} references missing family {fam_id}."
                )

    # Unlinked Individuals
    for person_id, person in family_tree.persons.items():
        if not person.famc and not person.fams:
            issues["Unlinked Individuals"].append(
                f"Person {person_id} is not linked to any family."
            )

    # Duplicate or Conflicting Records
    person_data = defaultdict(list)
    for person_id, person in family_tree.persons.items():
        key = (person.name, person.birthday, person.death)
        person_data[key].append(person_id)
    for key, ids in person_data.items():
        if len(ids) > 1:
            issues["Duplicate Records"].append(
                f"Duplicate individuals found: {', '.join(ids)}."
            )

    # Invalid or Highly Unusual Date Ranges
    for person_id, person in family_tree.persons.items():
        try:
            birth_year = int(str(person.birthday).split()[-1])
            death_year = (
                int(str(person.death).split()[-1])
                if person.death != "Alive"
                else current_year
            )

            if death_year - birth_year > 120:
                issues["Unusual Lifespans"].append(
                    f"Person {person_id} lived an implausible {death_year - birth_year} years."
                )
            if birth_year > current_year:
                issues["Invalid Dates"].append(
                    f"Person {person_id} has a birth year in the future ({birth_year})."
                )
            if death_year > current_year:
                issues["Invalid Dates"].append(
                    f"Person {person_id} has a death year in the future ({death_year})."
                )
        except (ValueError, TypeError):
            pass

    # Inconsistent Generational Gaps
    for family_id, family in family_tree.families.items():
        if family.husb in family_tree.persons and family.wife in family_tree.persons:
            husband = family_tree.persons[family.husb]
            wife = family_tree.persons[family.wife]
            husband_birth = extract_year(husband.birthday)
            wife_birth = extract_year(wife.birthday)
            for child_id in family.children:
                if child_id in family_tree.persons:
                    child = family_tree.persons[child_id]
                    child_birth = extract_year(child.birthday)
                    if (
                        husband_birth
                        and child_birth
                        and child_birth - husband_birth < 12
                    ):
                        issues["Inconsistent Generational Gaps"].append(
                            f"Husband {family.husb} ({husband.name}) is too young to have child {child_id} ({child.name})."
                        )
                    if wife_birth and child_birth and child_birth - wife_birth < 12:
                        issues["Inconsistent Generational Gaps"].append(
                            f"Wife {family.wife} ({wife.name}) is too young to have child {child_id} ({child.name})."
                        )

    # Check for missing common facts
    missing_common_facts = []
    for person_id, person in family_tree.persons.items():
        missing = []
        if not person.name or len(person.name.strip().split(" ")) < 2:
            missing.append("Name")
        if not person.birthday:
            missing.append("Birth")
        if person.death == "Alive" and not person.death:
            missing.append("Death")
        elif person.death != "Alive" and not person.death:
            missing.append("Death")
        if missing:
            missing_common_facts.append(
                {
                    "id": person_id,
                    "name": person.name if person.name else "Unknown",
                    "missing_facts": missing,
                }
            )

    if missing_common_facts:
        issues["Missing Common Facts"] = missing_common_facts

    return issues


def extract_year(date_str: str | None) -> int | None:
    """Extract year from a date string."""
    try:
        return int(str(date_str).split()[-1])
    except (ValueError, AttributeError, IndexError):
        return None


def generate_validation_html(family_tree: FamilyTree) -> str:
    """Generate an HTML report of validation issues."""
    issues = validate_family_tree(family_tree)
    html = ""

    if not issues:
        html += "<p>No issues found in the family tree!</p>"
    else:
        for category, problems in issues.items():
            if category != "Missing Common Facts":
                html += f"<h2>{category}</h2><ul>"
                # Sort the problems if they involve person names
                if category in [
                    "Broken Links",
                    "Unlinked Individuals",
                    "Duplicate Records",
                ]:
                    sorted_problems = sorted(
                        problems, key=lambda x: extract_sortable_name(x)
                    )
                    for problem in sorted_problems:
                        html += f"<li>{problem}</li>"
                else:
                    for problem in problems:
                        html += f"<li>{problem}</li>"
                html += "</ul>"

        # Add Missing Common Facts Section
        if "Missing Common Facts" in issues:
            sorted_missing = sorted(
                issues["Missing Common Facts"],
                key=lambda x: extract_sortable_name(x["name"]),
            )
            html += "<h2>Missing Common Facts</h2><ul>"
            for entry in sorted_missing:
                name = entry["name"]
                person_id = entry["id"]
                missing = ", ".join(entry["missing_facts"])
                html += f"<li>{person_id}: Missing {missing}</li>"
            html += "</ul>"

    return html


def extract_sortable_name(name: str) -> tuple:
    """Extract last name and first name for sorting."""
    parts = name.split()
    if len(parts) >= 2:
        return (parts[-1].lower(), " ".join(parts[:-1]).lower())
    return (parts[0].lower(), "")
