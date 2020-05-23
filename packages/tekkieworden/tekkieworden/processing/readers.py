import csv
import requests
import logging
import yaml

from tekkieworden.config import config


_logger = logging.getLogger(__name__)


def download_duo_files(url, file: str):
    """
    :param url:  https://duo.nl/open_onderwijsdata/databestanden/ho/ingeschreven/
    :param file: Hoger Onderwijs hbo_inscriptions + wo_inscriptions
    :return: downloaded csv saved to RAW data folder
    """
    response = requests.get(url)
    print(f"Downloading: {file}, writing to {config.PATH_TO_RAW_DATA}")
    with open(
        str(config.PATH_TO_RAW_DATA)
        + "/"
        + file
        + "_"
        + str(config.FILE_YEAR)
        + ".csv",
        "w",
    ) as f:
        writer = csv.writer(f)
        for line in response.iter_lines():
            writer.writerow(line.decode("ISO-8859-1").split(","))


def open_tech_label_yaml(yaml_file):
    """
    reads the tech_label.yml in config dir
    :param yaml_file: name of the yaml file to open
    """
    with open(str(config.PATH_TO_CONFIG) + "/" + yaml_file, "r") as f:
        tech_label_dict = yaml.safe_load(f)
    return tech_label_dict


if __name__ == "__main__":
    download_duo_files(
        url=config.HBO_CSV_I_URL, file=config.DUO_HBO_I_FILE
    )  # hbo ingeschrevenen
    download_duo_files(
        url=config.HBO_CSV_D_URL, file=config.DUO_HBO_D_FILE
    )  # hbo gediplomeerden
    download_duo_files(
        url=config.WO_CSV_I_URL, file=config.DUO_WO_I_FILE
    )  # wo ingeschrevenen
    download_duo_files(
        url=config.WO_CSV_D_URL, file=config.DUO_WO_D_FILE
    )  # wo gediplomeerden
    download_duo_files(
        url=config.MBO_CSV_I_URL, file=config.DUO_MBO_I_FILE
    )  # mbo ingeschrevenen (deelnemers)
    download_duo_files(
        url=config.MBO_CSV_D_URL, file=config.DUO_MBO_D_FILE
    )  # mbo gediplomeerden
