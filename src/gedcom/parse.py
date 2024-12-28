from gedcom.tree import FamilyTree
from gedcom.fact import GedcomTag, Fact


def parse(gedcom_path: str) -> FamilyTree | None:
    facts: list[Fact] = []
    non_fact_tags: list[GedcomTag] = [
        GedcomTag.FAM,
        GedcomTag.INDI,
        GedcomTag.SOUR,
    ]  # this should probably be dynamic but it is what is it right now

    with open(gedcom_path, "r", encoding="utf-8", errors="ignore") as file:
        text = file.read()
        lines = text.splitlines()
        lines[0] = "0 HEAD"  # weird hardcode to get this to work
        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue  # Skip empty lines

            if parts[0].isdigit():
                # Start of a new fact
                level = int(parts[0])
                if len(parts) > 1:
                    tag = GedcomTag[parts[1]]
                    if (
                        level == 0
                        and tag == GedcomTag.OTHER
                        and len(parts) >= 3
                        and GedcomTag[parts[2]] in non_fact_tags
                    ):
                        tag = GedcomTag[parts[2]]
                        value = parts[1]
                    else:
                        value = " ".join(parts[2:]) if len(parts) > 2 else ""

                    if tag == GedcomTag.CONC:
                        facts[-1].value += value
                    else:
                        facts.append(Fact(level, tag, value))
            else:
                # Continuation of the previous fact value
                if facts:
                    facts[-1].value += f" {line.strip()}"

    if len(facts) == 0:
        return None

    # Determine subfacts based on levels
    queue: list[Fact] = []
    queue.append(facts.pop(0))
    final_facts: list[Fact] = []
    while queue and facts:
        fact = facts.pop(0)

        while len(queue) > 0 and fact.level <= queue[-1].level:
            done = queue.pop(-1)
            if done.level == 0:
                final_facts.append(done)

        if len(queue) > 0:
            queue[-1].sub_facts.append(fact)

        queue.append(fact)

    # queue should be empty because the final fact in a gedcom file is "0 TRLR"

    ft = FamilyTree(final_facts)
    return ft