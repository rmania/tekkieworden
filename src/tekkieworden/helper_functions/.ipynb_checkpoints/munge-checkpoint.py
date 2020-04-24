import logging
import pandas as pd
import numpy as np
import sys
import re
import string

from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

sys.path.insert(0, "../")
sys.path.insert(0, "../db_config/")

from sdb_config import drop_studiekeuze_cols
from config import DUO_HBO_CSV, DUO_WO_CSV

PATH_TO_RAW_DATA = "../../../data/raw/"


def prepare_sdb_opleidingen_file(path, file):
    """
    Read in the Studiekeuze excel Opleidingen Sheet
    TODO: needs to point to the API calls
    :param path: path to SDB excel
    :param file: name of SDB excel file
    :return: formatted SDB file
    """
    df = pd.read_excel(path + file, sheet_name="Opleidingen")
    logging.info(f"dropping columns: \n {drop_studiekeuze_cols}")
    for col in drop_studiekeuze_cols:
        df = df.drop(col, axis=1)
    df.columns = df.columns.str.lower()
    # check with Tekkieworden
    logging.info(f"putting filter on:{df.actieveopleiding.name} == 1.0")
    df = df[df.actieveopleiding == 1.0]

    df.columns = df.columns + "_sdb"

    df["brinnummer_sdb"] = df["brinnummer_sdb"].astype(str)
    df["soortopleiding_sdb"] = df["soortopleiding_sdb"].str.lower()  # like in duo file

    # cat opleidingsvormen into one column
    df["opleidingsvorm_sdb"] = np.where(
        df.voltijd_sdb == 1,
        "voltijd onderwijs",
        (np.where(df.deeltijd_sdb == 1, "deeltijd onderwijs", "duaal onderwijs")),
    )
    for col in ["voltijd_sdb", "deeltijd_sdb", "duaal_sdb"]:
        df = df.drop(col, axis=1)

    logging.info(f"Studiekeuze opledingen frame shape: {df.shape}")
    # logging.info(f'Extract \n: {df.head(5)}')

    return df


def prepare_duo_ho_files(path, file: str):
    """
    Reads in and formats DUO files
    :param path: path to DUO file
    :param file: name of Duo file
    :return: formatted DUO file
    """
    df = pd.read_csv(path + file, sep=";")
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    for c in ["gemeentenummer", "opleidingscode_actueel"]:
        df[c] = df[c].map("{:.0f}".format).astype(str)

    empty_col_name = "brin_nummer_actueel"
    logging.info(
        f"Dropping {len(df[df[empty_col_name].isnull()].index)} rows where <{empty_col_name}> is empty"
    )
    df = df.dropna(subset=["brin_nummer_actueel"], how="any")

    drop_cols = ["gemeentenaam", "soort_instelling"]
    logging.info(f"Dropping columns: {drop_cols}")
    for col in drop_cols:
        df = df.drop(col, axis=1)

    rename_column_dict = {
        "provincie": "provincie_duo",
        "gemeentenummer": "gemeentenummer_duo",
        "type_hoger_onderwijs": "soortopleiding_duo",
        "brin_nummer_actueel": "brinnummer_duo",
        "instellingsnaam_actueel": "instellingsnaam_duo",
        "croho_onderdeel": "croho_onderdeel_duo",
        "croho_subonderdeel": "croho_subonderdeel_duo",
        "opleidingscode_actueel": "opleidingscode_duo",
        "opleidingsnaam_actueel": "opleidingsnaam_duo",
        "opleidingsvorm": "opleidingsvorm_duo",
    }
    logging.info(f"Renaming columns: {rename_column_dict}")
    df = df.rename(columns=rename_column_dict)

    df.brinnummer_duo = df.brinnummer_duo.astype(str)

    regex_pattern = "\s(.*)"  # extract string after first whitespace
    df["opleidingsnaam_duo"] = df["opleidingsnaam_duo"].str.extract(regex_pattern)

    logging.info(f"{file} shape: {df.shape}")
    return df


def concat_unstack_duo_ho_files(year: int):
    """
    Pivotting the duo file and totalling the student numbers on year
    :param year: totalling inschrijvingsdata from this year
    :return: pivotted duo file with student totals
    """

    hbo = prepare_duo_ho_files(path=PATH_TO_RAW_DATA, file=DUO_HBO_CSV)
    wo = prepare_duo_ho_files(path=PATH_TO_RAW_DATA, file=DUO_WO_CSV)
    duo = pd.concat([wo, hbo], axis=0)
    logging.info(f"Concatting {DUO_HBO_CSV, DUO_WO_CSV}\n. Duo file shape: {duo.shape}")

    gemeentes = (
        duo.groupby("brinnummer_duo")["gemeentenummer_duo"]
        .unique()
        .apply(list)
        .reset_index()
    )

    logging.info("summing MAN, VROUW into TOTAL")
    duo_ = (
        duo.groupby(
            [
                "brinnummer_duo",
                "instellingsnaam_duo",
                "opleidingsnaam_duo",
                "croho_onderdeel",
                "croho_subonderdeel",
                # 'opleidingsvorm_duo',
                # 'gemeentenummer_duo',
                "soortopleiding_duo",
                "geslacht",
            ]
        )[str(year)]
        .sum()
        .unstack("geslacht")
    ).reset_index(drop=False)
    duo_[f"tot_{year}_duo"] = duo_["man"].add(duo_["vrouw"])

    logging.info("Merge back the concatted gemeentes")
    duo_ = pd.merge(left=duo_, right=gemeentes, on=["brinnummer_duo"], how="left")

    logging.info(f"Duo file shape: {duo_.shape}")
    logging.info(f"Extract \n: {duo_.head(5)}")

    return duo_


def clean_string_fields(x):

    stopwords_nl = set(stopwords.words("dutch"))
    punctuation = string.punctuation

    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()

    x = (
        x.lower()
        .replace("\r\n\r\n", " ")
        .replace(" \xa0", "")
        .replace("?s", "")
        .replace("’", "")
        .replace("‘", "")
        .replace("“", "")
        .replace("”", "")
        .replace("—", "")
    )
    x = "".join(word for word in x if word not in punctuation)
    x = word_tokenize(x)
    x = " ".join(word for word in x if word not in stopwords_nl)
    x = re.sub(r"\d+", "", x)
    x = stemmer.stem(x)
    x = lemmatizer.lemmatize(x)

    return x
