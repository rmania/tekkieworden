import pathlib
import pandas as pd
import tekkieworden

pd.options.display.max_rows = 10
pd.options.display.max_columns = 10

# paths
PACKAGE_ROOT = pathlib.Path(tekkieworden.__file__).resolve().parent
PATH_TO_RAW_DATA = PACKAGE_ROOT / "datasets/raw/"
PATH_TO_MUNGED_DATA = PACKAGE_ROOT / "datasets/munged/"
PATH_TO_FINAL_DATA = PACKAGE_ROOT / "datasets/final/"
PATH_TO_CONFIG = PACKAGE_ROOT / "config"
PATH_TO_DATA_QUALITY_REPORT = PACKAGE_ROOT / "docs/data_quality_report/"
PATH_TO_GAP_REPORT = PACKAGE_ROOT / "gap_report/"
PATH_TO_CSS_FILES = PACKAGE_ROOT / "app/"

FILE_YEAR = 2019

# url + csv filenames for Hoger Onderwijs Ingeschrevenen (_I) and Gediplomeerden (_D) from DUO.nl
DUO_MAIN_URL = "https://duo.nl/open_onderwijsdata/images/"
MBO_CSV_URL = DUO_MAIN_URL + "08-deelnemers-per-instelling-bestuur-gemeente-kenniscentrum-sector-bedrijfstak-type-mbo-opleiding-verblijfsjaar-2015-2019.csv"
HBO_CSV_I_URL = DUO_MAIN_URL + "03b-eerstejaars-ingeschrevenen-hbo-domein-hbo-2019.csv"
HBO_CSV_D_URL = DUO_MAIN_URL + "05-gediplomeerden-hbo-2019.csv"
WO_CSV_I_URL = DUO_MAIN_URL + "03b-eerstejaars-ingeschrevenen-wo-domein-wo-2019.csv"
WO_CSV_D_URL = DUO_MAIN_URL + "05-gediplomeerden-wo-2019.csv"

# files
SDB_FILE = "studiekeuze123_all_20200417.xlsx"
DUO_MBO_FILE = "mbo_inscriptions"
DUO_HBO_I_FILE = "hbo_inscriptions"
DUO_HBO_D_FILE = "hbo_gediplomeerden"
DUO_WO_I_FILE = "wo_inscriptions"
DUO_WO_D_FILE = "wo_gediplomeerden"
DUO_MBO_CSV = f"mbo_inscriptions_{FILE_YEAR}.csv"
DUO_HBO_I_CSV = f"hbo_inscriptions_{FILE_YEAR}.csv"
DUO_HBO_D_CSV = f"hbo_gediplomeerden_{FILE_YEAR}.csv"
DUO_WO_I_CSV = f"wo_inscriptions_{FILE_YEAR}.csv"
DUO_WO_D_CSV = f"wo_gediplomeerden_{FILE_YEAR}.csv"


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
    "intelligence",
    "data science",
    "kunstmatige intelligentie",
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
