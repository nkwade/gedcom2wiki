from gedcom.tree import FamilyTree
from gedcom.fact import GedcomTag, Fact
import time

non_fact_tags: list[GedcomTag] = [
    GedcomTag.FAM,
    GedcomTag.INDI,
    GedcomTag.SOUR,
]  # this should probably be dynamic but it is what is it right now


def extract_fact(line: str) -> Fact | None:
    parts = line.strip().split()
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

            return Fact(level, tag, value)
    return None


def parse(gedcom_path: str) -> FamilyTree | None:
    facts: list[Fact] = []
    final_facts: list[Fact] = []

    start = time.time()

    with open(gedcom_path, "r", encoding="utf-8", errors="ignore") as file:
        text = file.read()
        lines = text.splitlines()
        lines[0] = "0 HEAD"  # weird hardcode to get this to work

        for line in lines:
            if len(line) > 0 and line[0].isdigit():
                fact = extract_fact(line)
                if fact and fact.tag == GedcomTag.CONC:
                    facts[-1].value += fact.value
                elif fact:
                    while len(facts) > 0 and fact.level <= facts[-1].level:
                        done = facts.pop(-1)
                        if done.level == 0:
                            final_facts.append(done)

                    if len(facts) > 0:
                        facts[-1].sub_facts.append(fact)
                    facts.append(fact)
            else:
                # Continuation of the previous fact value
                if facts:
                    facts[-1].value += f" {line.strip()}"

    print(f"Time to parse: {time.time() - start}")
    start = time.time()

    if len(final_facts) > 0:
        ft = FamilyTree(final_facts)
        print(f"Time to create tree: {time.time() - start}")
        return ft
    else:
        return None
