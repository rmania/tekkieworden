import logging
import pandas as pd
import numpy as np
import os
import re
import pandas_profiling as pdp

from typing import List

from tekkieworden.config import config
from tekkieworden.processing.readers import open_tech_label_yaml
from tekkieworden.processing.writers import write_df_csv
from tekkieworden.processing.utilities import pandas_join_key_dual


_logger = logging.getLogger(__name__)


def prepare_sdb_opleidingen_file(
    path, file: str, data_quality_report=None
) -> pd.DataFrame:
    """
    Read in the Studiekeuze excel Opleidingen Sheet
    TODO: needs to point to the API calls
    :param path: path to SDB excel
    :param file: name of SDB excel file
    :param data_quality_report: generates and stores a Pandas profiling report
    :return: formatted SDB file
    """
    df = pd.read_excel(os.path.join(str(path), file), sheet_name="Opleidingen")

    if data_quality_report:

        logging.info(
            f"Generating Data quality report. Storing : {config.PATH_TO_DATA_QUALITY_REPORT}"
        )
        sdb_profile_report = pdp.ProfileReport(df)
        sdb_profile_report.to_file(
            config.PATH_TO_DATA_QUALITY_REPORT + "sdb_data_quality_report.html"
        )

    logging.info(f"dropping columns: \n {config.drop_studiekeuze_cols}")
    for col in config.drop_studiekeuze_cols:
        df = df.drop(col, axis=1)
    df.columns = df.columns.str.lower()
    # check with Tekkieworden
    # logging.info(f"putting filter on:{df.actieveopleiding.name} == 1.0")
    # df = df[df.actieveopleiding == 1.0]

    df.columns = df.columns + "_sdb"

    str_cols = ["brinnummer_sdb", "opleidingscode_sdb", "opleiding_sk123id_sdb"]
    for col in str_cols:
        df[col] = df[col].astype(str)
    df["soortopleiding_sdb"] = df["soortopleiding_sdb"].str.lower()  # like in DUO file
    df["soortho_sdb"] = df["soortho_sdb"].apply(lambda x: x.lower())  # like in DUO file

    # cat opleidingsvormen into one column
    df["opleidingsvorm_sdb"] = np.where(
        df.voltijd_sdb == 1,
        "voltijd onderwijs",
        (np.where(df.deeltijd_sdb == 1, "deeltijd onderwijs", "duaal onderwijs")),
    )
    for col in ["voltijd_sdb", "deeltijd_sdb", "duaal_sdb"]:
        df = df.drop(col, axis=1)

    logging.info(f"Studiekeuze opleidingen frame shape: {df.shape}")
    # logging.info(f'Extract \n: {df.head(5)}')

    return df


def prepare_duo_ho_files(path, file: str, ho_type: str) -> pd.DataFrame:
    """
    Reads in and formats DUO files
    :param path: path to DUO file
    :param file: name of Duo file
    :param ho_type: hbo or wo. Adds adequate column to dataset
    :return: formatted DUO file
    """
    df = pd.read_csv(os.path.join(str(path), file), sep=";")
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

    logging.info(f"Adding column: {ho_type}")
    df[f"ho_type"] = ho_type

    logging.info(f"{file} shape: {df.shape}")
    return df


def concat_unstack_duo_ho_files(years=List[int]) -> pd.DataFrame:
    """
    Pivotting the DUO file and totalling the student numbers on all years
    :param years: list of years to be summed e.g. [2017, 2018, 2019]
    :return: pivoted DUO file with summed inscriptions
    """

    hbo = prepare_duo_ho_files(
        path=config.PATH_TO_RAW_DATA, file=config.DUO_HBO_CSV, ho_type="hbo"
    )
    wo = prepare_duo_ho_files(
        path=config.PATH_TO_RAW_DATA, file=config.DUO_WO_CSV, ho_type="wo"
    )
    duo = pd.concat([wo, hbo], axis=0)
    logging.info(
        f"Concatting {config.DUO_HBO_CSV, config.DUO_WO_CSV}\n. Duo file shape: {duo.shape}"
    )

    gemeentes = (
        duo.groupby("brinnummer_duo")["gemeentenummer_duo"]
        .unique()
        .apply(list)
        .reset_index()
    )

    groupby_cols = [
        "brinnummer_duo",
        "instellingsnaam_duo",
        "croho_onderdeel_duo",
        "croho_subonderdeel_duo",
        "opleidingscode_duo",
        "opleidingsnaam_duo",
        "ho_type",
        "soortopleiding_duo",
        #'opleidingsvorm_duo', # voltijd vs deeltijd
        "geslacht",
    ]

    duo_ = (
        duo.groupby(groupby_cols)[str(years[-1])]
        .sum()
        .unstack("geslacht")
        .drop("man", axis=1)
        .drop("vrouw", axis=1)
    ).reset_index(drop=False)

    logging.info("Merge back the concatted gemeentes")
    duo_ = pd.merge(left=duo_, right=gemeentes, on=["brinnummer_duo"], how="left")

    logging.info(f"Duo file shape: {duo_.shape}")
    logging.info(f"Extract \n: {duo_.head(5)}")

    logging.info("summing MAN, VROUW into TOTAL")

    concatted_frame = []
    for y in years:
        duo_y = (
            duo.groupby(groupby_cols)[str(y)].sum().unstack("geslacht")
        ).reset_index(drop=False)
        duo_y[f"tot_{y}_duo"] = duo_y["man"].add(duo_y["vrouw"])
        concatted_frame.append(duo_y[f"tot_{y}_duo"])

    concatted_df = pd.concat([duo_, pd.concat(concatted_frame, axis=1)], axis=1)

    return concatted_df


def merge_duo_sdb_files(duo_file, sdb_file) -> pd.DataFrame:
    """
    Join the cleaned DUO file and Studiekeuze file and mutually fill missing values
    :param duo_file: the cleaned concatted DUO file.
    :param sdb_file: the cleaned studiekeuze database file
    :return: joined file ready to be filtered on Tech studies
    """
    sdb_groupby_cols = [
        "brinnummer_sdb",
        "opleidingscode_sdb",
        "naamopleiding_sdb",
        "soortopleiding_sdb",
        "soortho_sdb",
        "cluster_sdb",
        "sector_sdb",
        "titel_sdb",
        "actieveopleiding_sdb",
        "naamopleidingengels_sdb",
        # 'opleidingsvorm_sdb'
    ]
    logging.info(f"Group the {sdb_file} on : {sdb_groupby_cols}")
    sdb_agg = (
        sdb_file.groupby(sdb_groupby_cols)
        .agg({"eerstejaarsaantal_sdb": "sum", "studentenaantal_sdb": "sum"})
        .reset_index()
    )
    sdb_join_cols = ["brinnummer_sdb", "opleidingscode_sdb"]
    sdb_add_cols = [
        "cluster_sdb",
        "sector_sdb",
        "actieveopleiding_sdb",
        "naamopleidingengels_sdb",
        "eerstejaarsaantal_sdb",
        "studentenaantal_sdb",
    ]

    logging.info(f"Merging {duo_file} and aggregrated: {sdb_file} on : {sdb_join_cols}")
    logging.info(f"Adding following columns: {sdb_add_cols}")
    df = pandas_join_key_dual(
        left_df=duo_file,
        right_df=sdb_agg[sdb_join_cols + sdb_add_cols],
        left_key=["brinnummer_duo", "opleidingscode_duo"],
        right_key=sdb_join_cols,
        how="left",
    )
    df = df.drop(sdb_join_cols, axis=1)

    fill_cols = ["studentenaantal_sdb", "eerstejaarsaantal_sdb"]
    logging.info(
        f"Filling : {fill_cols} with data from : {duo_file} when data is missing"
    )
    df.loc[df.studentenaantal_sdb.isnull(), fill_cols] = df.loc[
        df.studentenaantal_sdb.isnull(), "tot_2018_duo"
    ]
    df.loc[df.tot_2018_duo.isnull(), "tot_2018_duo"] = df.loc[
        df.tot_2018_duo.isnull(), "eerstejaarsaantal_sdb"
    ]

    logging.info(
        f"put actieveopleiding_sdb to status active when succesfully merged with {duo_file}"
    )
    df.loc[df.actieveopleiding_sdb.isnull(), "actieveopleiding_sdb"] = 1.0

    logging.info(
        f"if English naamopleiding from {sdb_file} is missing, copy from : {duo_file}"
    )
    df.loc[(df.naamopleidingengels_sdb.isnull()), "naamopleidingengels_sdb"] = df.loc[
        (df.naamopleidingengels_sdb.isnull()), "opleidingsnaam_duo"
    ]

    logging.info(f"merged dataframe shape : {df.shape}")
    return df


def tag_tech_studies(input_df: pd.DataFrame, tech_keywords=List[str]) -> pd.DataFrame:
    """
    create a tech keywords column based on a tech_keywords list in config file
    :param input_df:
    :param tech_keywords: list of tech keyword strings
    :return: pd.DataFrame with additional tech_keyword column to filter on
    """
    cols_to_check = [
        "opleidingsnaam_duo",
        "croho_onderdeel_duo",
        "cluster_sdb",
        "sector_sdb",
        "naamopleidingengels_sdb",
    ]

    logging.info(f"Searching for tech keywords in : {cols_to_check}")
    for c in cols_to_check:
        input_df["tech_keyword"] = input_df[c].str.findall(
            r"|".join(config.tech_keywords), flags=re.IGNORECASE
        )
    input_df["tech_keyword"] = input_df.tech_keyword.apply(", ".join)
    input_df["tech_keyword"] = input_df["tech_keyword"].apply(lambda x: x.lower())

    return input_df


def label_tech_studies(input_df: pd.DataFrame) -> pd.DataFrame:
    """
    create a tech_label column based on a mapping in the tech_label.yml
    :param input_df: pd.Dataframe
    :return: pd.DataFrame with additional tech_label column to filter on
    """
    tech_label_dict = open_tech_label_yaml()["tech"]
    input_df["tech_label"] = input_df["opleidingsnaam_duo"].map(tech_label_dict)
    # tricky CHECK with TEKKIEWORDEN!
    input_df["tech_label"] = input_df["tech_label"].fillna("no_tech")

    return input_df


def filter_tech_studies(input_df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter the prepared duo, sdb file on tech studies using either the tech_label
    colomn or the tech_keyword column
    :return: filtered pd.DataFrame with ony tech-related studies
    """
    tech_filtered_df = input_df.query("tech_label != 'no_tech'")
    logging.info(f"Shape of tech-filtered DataFrame: {tech_filtered_df.shape}")

    return tech_filtered_df


def main():
    sdb = prepare_sdb_opleidingen_file(
        path=config.PATH_TO_RAW_DATA, file=config.SDB_FILE, data_quality_report=None
    )
    duo = concat_unstack_duo_ho_files(years=[2015, 2016, 2017, 2018, 2019])
    df = merge_duo_sdb_files(duo_file=duo, sdb_file=sdb)
    df = tag_tech_studies(input_df=df, tech_keywords=config.tech_keywords)
    write_df_csv(input_df=df, filename="opleidingen_total_munged.csv")
    tech_filtered_df = filter_tech_studies(input_df=df)
    write_df_csv(input_df=tech_filtered_df, filename="opleidingen_tech_filtered.csv")


if __name__ == "__main__":
    main()
