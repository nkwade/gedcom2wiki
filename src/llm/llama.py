from ollama import generate
from ollama import GenerateResponse, ResponseError, pull

from gedcom.tree import FamilyTree
from gedcom.fact import GedcomTag, Fact
from gedcom.family import Family
from gedcom.person import Person


def gather_context(person: Person, tree: FamilyTree) -> str:
    """Gather comprehensive context about a person for biography generation."""
    context = []

    # Basic information
    context.append(f"Subject: {person.name or 'Unknown'}")
    context.append(f"Sex: {person.sex.name if person.sex else 'Unknown'}")
    context.append(f"Birth: {person.birthday or 'Unknown'}")
    context.append(f"Death: {person.death or 'Living'}")

    # Childhood family
    if person.famc:
        for family_id in person.famc:
            family = tree.families[family_id]
            context.append("\nChildhood Family:")
            if family.husb and family.husb in tree.persons:
                father = tree.persons[family.husb]
                context.append(f"Father: {father.name or 'Unknown'}")
            if family.wife and family.wife in tree.persons:
                mother = tree.persons[family.wife]
                context.append(f"Mother: {mother.name or 'Unknown'}")
            siblings = [
                tree.persons[child]
                for child in family.children
                if child != person.xref_id and child in tree.persons
            ]
            if siblings:
                context.append("Siblings:")
                for sibling in siblings:
                    context.append(f"- {sibling.name or 'Unknown'}")

    # Adult families
    if person.fams:
        for family_id in person.fams:
            family = tree.families[family_id]
            context.append("\nFamily as Adult:")
            if (
                family.husb
                and family.husb != person.xref_id
                and family.husb in tree.persons
            ):
                spouse = tree.persons[family.husb]
                context.append(f"Husband: {spouse.name or 'Unknown'}")
            if (
                family.wife
                and family.wife != person.xref_id
                and family.wife in tree.persons
            ):
                spouse = tree.persons[family.wife]
                context.append(f"Wife: {spouse.name or 'Unknown'}")
            children = [
                tree.persons[child]
                for child in family.children
                if child in tree.persons
            ]
            if children:
                context.append("Children:")
                for child in children:
                    context.append(f"- {child.name or 'Unknown'}")

            # Marriage facts
            for fact in family.facts:
                if fact.tag == GedcomTag.MARR:
                    context.append("Marriage Details:")
                    for sub_fact in fact.sub_facts:
                        if sub_fact.tag == GedcomTag.DATE:
                            context.append(f"Marriage Date: {sub_fact.value}")
                        elif sub_fact.tag == GedcomTag.PLAC:
                            context.append(f"Marriage Place: {sub_fact.value}")

    # Additional facts about the person
    context.append("\nLife Events:")
    for fact in person.facts:
        if fact.tag not in [
            GedcomTag.SEX,
            GedcomTag.NAME,
            GedcomTag.BIRT,
            GedcomTag.DEAT,
        ]:
            context.append(f"{fact.tag.value}: {fact.value}")

    return "\n".join(context)


def generate_bio(person: Person, tree: FamilyTree):
    context: str = gather_context(person, tree)
    print(f"Generating Bio for: {person.name}")

    system_prompt = """You are a professional genealogist and biographer. Your task is to write a 
comprehensive but concise biography based on genealogical records. Follow these guidelines:

1. Write in a formal, professional tone
2. Present information chronologically when possible
3. Focus on key life events: birth, marriage, children, occupation, death
4. Mention family relationships and their significance
5. Use dates and locations when available
6. Avoid speculation unless clearly marked as such
7. Keep the biography factual and objective
8. Write in third person narrative style
9. Aim for 2-3 paragraphs of content
10. Start with birth and early life, then cover adult life and accomplishments
11. End with information about death if applicable
12. Use transitional phrases to connect different life events

Here are the facts about the subject:

"""

    model = "llama3.1:8b"

    try:
        response: GenerateResponse = generate(
            model=model,
            prompt=f"{system_prompt}{context}\n\nPlease write a biography based on these facts:",
        )
    except ResponseError as e:
        print("Error:", e.error)
        if e.status_code == 404:
            pull(model)

    return response.response
