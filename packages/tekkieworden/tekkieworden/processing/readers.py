import csv
import requests
import logging
import yaml

from tekkieworden.config import config


_logger = logging.getLogger(__name__)


def download_student_inscriptions(url, file: str):
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


def open_tech_label_yaml():
    """
    reads the tech_label.yml in config dir
    """
    with open(str(config.PATH_TO_CONFIG) + "/tech_label.yml", "r") as f:
        try:
            tech_label_dict = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)
    return tech_label_dict


if __name__ == "__main__":
    download_student_inscriptions(url=config.MBO_CSV_URL, file=config.DUO_MBO_FILE)
    download_student_inscriptions(url=config.HBO_CSV_URL, file=config.DUO_HBO_FILE)
    download_student_inscriptions(url=config.WO_CSV_URL, file=config.DUO_WO_FILE)
