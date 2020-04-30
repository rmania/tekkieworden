import csv
import requests
import logging

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
    with open(str(config.PATH_TO_RAW_DATA) + "/" + file + "_" + str(config.FILE_YEAR) + ".csv", "w") as f:
        writer = csv.writer(f)
        for line in response.iter_lines():
            writer.writerow(line.decode("utf-8").split(","))


if __name__ == "__main__":
    download_student_inscriptions(url=config.HBO_CSV_URL, file=config.HBO_FILE)
    download_student_inscriptions(url=config.WO_CSV_URL, file=config.WO_FILE)
