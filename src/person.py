import enum
import datetime


class Person:
    def __init__(self, xref_id: str) -> None:
        self.xref_id: str = (
            xref_id  # The GEDCOM identifier for the individual, e.g. "@I1@"
        )
        self.names: list = []
        self.sex: str | None = None
        self.birth: dict = {}
        self.death: dict = {}
        self.famc: list = []  # Family where this person is a child
        self.fams: list = []  # Family where this person is a spouse
        # A dictionary to hold any other arbitrary data: keys = GEDCOM tag, value = list of entries
        self.data: dict = {}

    def add_data(self, tag, value):
        """Adds arbitrary GEDCOM data to the person's record."""
        if tag not in self.data:
            self.data[tag] = []
        self.data[tag].append(value)

    def __repr__(self):
        return f"Person({self.xref_id}, name={self.names}, sex={self.sex})"

class GedcomEvent(enum.Enum):
    BAPM = "Baptism"
    CHR = "Christening"
    BIRT = "Birth"
    BURI = "Burial"
    CREM = "Cremation"
    DEAT = "Death"
    ANUL = "Annulment"
    DIV = "Divorce"
    DIVF = "Divorce Filed"
    ENGA = "Engagement"
    SLGS = "LDS Spouse Sealing"
    MARR = "Marriage"
    MARB = "Marriage Bann"
    MARC = "Marriage Contract"
    MARL = "Marriage License"
    MARS = "Marriage Settlement"
    ADOP = "Adoption"
    CHRA = "Adult Christening"
    BARM = "Bar Mitzvah"
    BASM = "Bas Mitzvah"
    BLES = "Blessing"
    CAST = "Caste"
    CAUS = "Cause of Death"
    CENS = "Census"
    NCHI = "Children"
    CONF = "Confirmation"
    DSCR = "Description"
    EDUC = "Education"
    EMAIL = "Email"
    EMAI = "Email"
    EMIG = "Emigration"
    EVEN = "Event"
    FACT = "Fact"
    FAX = "Fax"
    FCOM = "First Communion"
    GRAD = "Graduation"
    IDNO = "ID Number"
    IMMI = "Immigration"
    BAPL = "LDS Baptism"
    SLGC = "LDS Child Sealing"
    CONL = "LDS Confirmation"
    ENDL = "LDS Endowment"
    WAC = "LDS Initiation"
    NMR = "Marriages"
    NATI = "National Origin"
    NATU = "Naturalization"
    NOTE = "Note"
    OCCU = "Occupation"
    ORDN = "Ordination"
    PROP = "Possessions"
    PROB = "Probate"
    REFN = "Reference Number"
    RELI = "Religious Affiliation"
    RESI = "Residence"
    RETI = "Retirement"
    SSN = "SSN"
    PHON = "Telephone"
    TITL = "Title"
    WWW = "Web Site"
    WILL = "Will"
    OTHER = "Other"

    @classmethod
    def _missing_(cls, value):
        return cls.OTHER


class Event:
    def __init__(self, name: str, date: str, place: str) -> None:
        self.name: str = name
        self.date: datetime.date
