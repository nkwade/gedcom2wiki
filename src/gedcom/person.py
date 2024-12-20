from typing import Any
from .fact import GedcomTag, Fact, TagValue
from .sex import Sex
from datetime import datetime
from PIL import Image
import requests
from io import BytesIO


class Person:
    def __init__(self, xref_id: str):
        self.xref_id = xref_id
        self.famc: list[str] = []  # Family IDs where this person is a child
        self.fams: list[str] = []  # Family IDs where this person is a spouse
        self.facts: list[Fact] = []  # List of facts that go with this person

        # Common facts that nearly everyone has:
        self.name: str | None = None
        self.sex: Sex | None = None
        self.birthday: datetime | str | None = None
        self.death: datetime | str = "Alive"
        self.images: list[Image.Image] = (
            []
        )  # all images for the person #TODO: attribute images to their respective fact

    def parse_tag_values(self, tvs: list[TagValue]) -> None:
        i = 0
        queue: list[tuple[int, Fact]] = []  # level, Fact

        while i < len(tvs):
            tv = tvs[i]
            while len(queue) > 0 and tv.level <= queue[-1][0]:
                level, done = queue.pop(-1)
                if (
                    level == 1
                ):  # all subfacts stored in fact so we only want to keep track of level 1 facts for people
                    self.parse_fact(done)

            fact = Fact(tv.tag, tv.value)

            if (
                fact.tag == GedcomTag.FORM
                and len(tvs) > i + 1
                and tvs[i + 1].tag == GedcomTag.FILE
            ):
                image: Image.Image | None = self.save_image(tvs[i + 1].value)
                if image is not None:
                    self.images.append(image)

            if len(queue) > 0:
                queue[-1][1].sub_facts[fact.tag] = fact

            queue.append((tv.level, fact))
            i += 1

        # Finish the last fact left in the queue
        while len(queue) != 0:
            level, done = queue.pop(-1)
            if level == 1:
                self.parse_fact(done)

    def parse_fact(self, fact: Fact) -> None:
        if fact.tag == GedcomTag.SEX:
            self.sex = Sex[fact.value]
        elif fact.tag == GedcomTag.BIRT and GedcomTag.DATE in fact.sub_facts.keys():
            # TODO: write gedcom date to datetime function
            self.birthday = fact.sub_facts[GedcomTag.DATE].value
        elif fact.tag == GedcomTag.DEAT and GedcomTag.DATE in fact.sub_facts.keys():
            self.death = fact.sub_facts[GedcomTag.DATE].value
        elif fact.tag == GedcomTag.NAME:
            fact.value = "".join([c for c in fact.value if c != "/"])
            if fact.value != "":
                self.name = fact.value
        # TODO: add any other facts I want to parse here

        self.facts.append(fact)

    def save_image(self, link: str) -> Image.Image | None:
        try:
            response = requests.get(link)
            image = Image.open(BytesIO(response.content))
            # image.show()
            return image
        except Exception as e:  # no access to images
            print(e.__str__())
            return None

    def __repr__(self) -> str:
        return f"Person({self.xref_id}, famc={self.famc}, fams={self.fams}, sex={self.sex}, birthday={self.birthday}, death={self.death}, facts={self.facts})"
