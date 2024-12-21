from enum import Enum, EnumMeta


class CustomEnumMeta(EnumMeta):
    def __getitem__(cls, name):
        try:
            return super().__getitem__(name)
        except KeyError:
            # print(f"Missing name: {name}")  # Handle the missing name case
            return cls.OTHER  # Fallback value


class GedcomTag(Enum, metaclass=CustomEnumMeta):
    HEAD = "Header"
    TRLR = "Trailer"
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
    ABBR = "Abbreviation"
    ADDR = "Address"
    ADR1 = "Address Line 1"
    ADR2 = "Address Line 2"
    AGE = "Age"
    AUTH = "Author"
    CHAR = "Character Set"
    CHIL = "Child"
    CITY = "City"
    CONC = "Concatenation"
    CORP = "Corporation"
    CTRY = "Country"
    DATA = "Data"
    DATE = "Date"
    DEST = "Destination"
    FAMC = "Family Child"
    FAMS = "Family Spouse"
    FILE = "File"
    FORM = "Format"
    GEDC = "GEDCOM Version"
    GIVN = "Given Name"
    HUSB = "Husband"
    LANG = "Language"
    NAME = "Name"
    NICK = "Nickname"
    NSFX = "Name Suffix"
    OBJE = "Object"
    PAGE = "Page"
    PLAC = "Place"
    POST = "Postal Code"
    PUBL = "Publication"
    QUAY = "Quality of Data"
    RIN = "Record ID Number"
    ROLE = "Role"
    SEX = "Sex"
    SOUR = "Source"
    STAE = "State"
    SURN = "Surname"
    TEXT = "Text"
    TYPE = "Type"
    VERS = "Version"
    WIFE = "Wife"
    _AKA = "Also Known As"
    _ALBUM = "Album"
    _CUTOUT = "Cutout"
    _DATE = "Date"
    _EXPORTED_FROM_SITE_ID = "Exported From Site ID"
    _FILESIZE = "File Size"
    _MARNM = "Married Name"
    _MEDI = "Media"
    _PARENTPHOTO = "Parent Photo"
    _PARENTRIN = "Parent RIN"
    _PERSONALPHOTO = "Personal Photo"
    _PHOTO_RIN = "Photo RIN"
    _PLACE = "Place"
    _POSITION = "Position"
    _PRIM = "Primary"
    _PRIM_CUTOUT = "Primary Cutout"
    _PROJECT_GUID = "Project GUID"
    _RNAME = "Repository Name"
    _RTLSAVE = "Right-to-Left Save"
    _UID = "Unique ID"
    _UPD = "Update"
    _TYPE = "Source Type"
    FAM = "Family"
    INDI = "Individual"

    @classmethod
    def _missing_(cls, value):
        # print(f"Missing value: {value[0:100]}")  # only first 100 char
        return cls.OTHER


class Fact:
    def __init__(self, level: int, tag: GedcomTag, value: str) -> None:
        self.tag: GedcomTag = tag
        self.value: str = value
        self.level: int = level
        self.sub_facts: list[Fact] = []  # Details about this Gedcom Tag

    def __str__(self):
        out = f"{self.tag.value}: {self.value}\n"
        for fact in self.sub_facts:
            out += f"\t{fact.tag.value}: {fact.value}\n"

        return out

    def __repr__(self):
        return f"tag={self.tag}, value={self.value}, sub_facts={self.sub_facts}"
