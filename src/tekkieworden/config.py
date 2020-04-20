from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent  # Assume this file lives in /src/tekkieworden!

# url + csv filenames for Hoger Onderwijs Ingeschrevenen
HBO_CSV_URL = "https://duo.nl/open_onderwijsdata/images/03b-eerstejaars-ingeschrevenen-hbo-domein-hbo-2019.csv"
WO_CSV_URL = "https://duo.nl/open_onderwijsdata/images/03b-eerstejaars-ingeschrevenen-wo-domein-wo-2019.csv"
HBO_FILE = "hbo_inscriptions"
WO_FILE = "wo_inscriptions"
FILE_YEAR = 2019

# General paths
PATH_TO_RAW_DATA = "../../data/raw/"
PATH_TO_MUNGED_DATA = "../../data/munged/"
PATH_TO_FINAL_DATA = "../../data/final/"