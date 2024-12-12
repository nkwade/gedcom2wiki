class FamilyTree:
    def __init__(self) -> None:
        # Store persons and families by their @XREF@ IDs
        self.persons: dict = {}
        self.families: dict = {}
        self.header: dict = {}
        self.trailer: dict = {}

    def link_families(self) -> None:
        """After parsing all individuals and families, link them by references."""
        for fam_id, family in self.families.items():
            # Link spouses
            if family.husb in self.persons:
                self.persons[family.husb].fams.append(fam_id)
            if family.wife in self.persons:
                self.persons[family.wife].fams.append(fam_id)
            # Link children
            for c in family.children:
                if c in self.persons:
                    self.persons[c].famc.append(fam_id)
