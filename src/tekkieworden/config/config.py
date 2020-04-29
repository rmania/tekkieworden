from pathlib import Path

import tekkieworden

# Assume PROJECT_ROOT = /tekkieworden/src/tekkieworden
PROJECT_ROOT = Path(tekkieworden.__file__).resolve().parent

# General paths
PATH_TO_RAW_DATA = PROJECT_ROOT / "../../data/raw/"
PATH_TO_MUNGED_DATA = PROJECT_ROOT / "../../data/munged/"
PATH_TO_FINAL_DATA = PROJECT_ROOT / "../../data/final/"
PATH_TO_DATA_QUALITY_REPORT = PROJECT_ROOT / "../../docs/data_quality_report/"

# url + csv filenames for Hoger Onderwijs Ingeschrevenen from DUO.nl
HBO_CSV_URL = "https://duo.nl/open_onderwijsdata/images/03b-eerstejaars-ingeschrevenen-hbo-domein-hbo-2019.csv"
WO_CSV_URL = "https://duo.nl/open_onderwijsdata/images/03b-eerstejaars-ingeschrevenen-wo-domein-wo-2019.csv"

HBO_FILE = "hbo_inscriptions"
WO_FILE = "wo_inscriptions"
DUO_HBO_CSV = "hbo_inscriptions_2019.csv"
DUO_WO_CSV = "wo_inscriptions_2019.csv"
FILE_YEAR = 2019

# studiekeuze123_all_20200417.xlsx columns to be dropped
drop_studiekeuze_cols = [
    "IndicatieIntensiefProgramma",
    "SelectieEisenIntensiefProgramma",
    "VerhoogdCollegegeldIntensiefProgramma",
    "BezoekadresStraat",
    "BezoekadresNummer",
    "BezoekadresPostcode",
    "Bekostiging",
    "AssociateDegree",
    "JointDegree",
    "BSAopmerking",
    "Studielast",
    "AlgemeenOordeel",
    "SourceURL",  # soms URL gevuld --> mogelijk nieuwe bronnen ?
    "TitelHodex",
    "Afstandonderwijs",
    "Avondonderwijs",
    "HeeftBindendStudieAdvies",
    "HeeftExtraInstroommoment",
    "ExtraStudiekosten",
    "LangeBeschrijvingOpleiding",
    "Opleidingswebsite",
    "PercentageStudentenNaarBuitenland",
    "PercentageStudentenUitBuitenland",  # mogelijk interessant voor techstudies ?
    "PercentageDocentenUitBuitenland",
    "PercentageDocentenNaarBuitenland",
    "PercentageAfstandsonderwijs",
    "PercentageAvondonderwijs",
    "WerkgroepGrootte",
    "IsKoepelOpleiding",
    "StudiekeuzecheckNaam",
    "StudiekeuzecheckBeleidVoor1Mei",
    "StudiekeuzecheckBeleidNa1Mei",
    "StudiekeuzecheckVerplicht",
    "StudiekeuzecheckUrl",
    "StudiekeuzecheckOmschrijving",
    "HeeftHonoursProgramma",
    "InstroomVoltijd",
    "InstroomDeeltijd",
    "InstroomDuaal",
    "InstroomTotaal",
    "InstroomMan",
    "InstroomVrouw",
    "AantalStudentenVoltijd",
    "AantalStudentenDuaal",
    "AantalStudentenTotaal",
    "PercentageMannelijkeStudenten",
    "PercentageVrouwelijkeStudenten",
    "AlgemeenOordeel01Wx",
    "nAlgemeenOordeel01",
    "AlgemeenOordeel01aWPrc",
    "AlgemeenOordeel01bWPrc",
    "AlgemeenOordeel01cWPrc",
    "AlgemeenOordeel01dWPrc",
    "AlgemeenOordeel01eWPrc",
    "ContacttijdEersteJaarVoltijd",
    "ContacttijdEerstejaarsVoltijdAantal",
    "WettelijkeVooropleidingseisenVwo",
    "OpmerkingenBijWettelijkeVooropleidingseisenVwo",
    "WettelijkeAanvullendeEisenVwo",
    "WettelijkeVooropleidingseisenHavo",
    "OpmerkingenBijWettelijkeVooropleidingseisenHavo",
    "WettelijkeAanvullendeEisenHavo",
    "ToelatingsEisenMbo",
    "ToelatingseisenHboWoBachelor",
    "maxjaar1CIJFHO",
    "AfstandsonderwijsPrc",
    "AvondonderwijsPrc",
    "NSEEnqueteJaar",
]


# mogelijke keywords om techstudies te filteren
tech_keywords = [
    "data",
    "Intelligence",
    "Data Science",
    "Kunstmatige Intelligentie",
    "computer science",
    "analytic",
    "analist",
    "artificial",
    "statistic",
    "developer",
    "online",
    "design",
    "media",
    "multimedia",
    "online",
    "marketing",
    "e-commerce",
    "grafisch",
    "web",
    "software",
    "hardware",
    "ontwikkelaar",
    "content",
    "creative",
    "digital",
    "ontwerp",
    "information",
    "ict",
    "cyber",
    "hack",
    "engineer",
    "informatica",
    "systeem",
    "beheerder" "technische",
    "wiskunde",
    "mathematics",
    "applied",
    "quantitative",
    "computer",
    "technology",
]