from .person import Person
from .family import Family


class FamilyTree:
    def __init__(self) -> None:
        self.persons: dict[str, Person] = {}
        self.families: dict[str, Family] = {}
        self.header: dict = {}
        self.trailer: dict = {}

    def link_families(self) -> None:
        """After parsing all individuals and families, link them."""
        for fam_id, family in self.families.items():
            if family.husb in self.persons:
                self.persons[family.husb].fams.append(fam_id)
            if family.wife in self.persons:
                self.persons[family.wife].fams.append(fam_id)
            for c in family.children:
                if c in self.persons:
                    self.persons[c].famc.append(fam_id)

    def __repr__(self) -> str:
        return f"FamilyTree(persons={len(self.persons)}, families={len(self.families)})"
