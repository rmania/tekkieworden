import csv
import requests
from config import PATH_TO_RAW_DATA, FILE_YEAR, HBO_CSV_URL, WO_CSV_URL, HBO_FILE, WO_FILE


def download_student_inscriptions(url, file):
    """
    :param url:  https://duo.nl/open_onderwijsdata/databestanden/ho/ingeschreven/
    :param file: hbo_inscriptions + wo_inscriptions
    :return: downloaded csv saved to RAW data folder
    """
    response = requests.get(url)

    with open(PATH_TO_RAW_DATA + file + "_" + str(FILE_YEAR) + ".csv", 'w') as f:
        writer = csv.writer(f)
        for line in response.iter_lines():
            writer.writerow(line.decode('utf-8').split(','))


if __name__ == '__main__':
    download_student_inscriptions(url = HBO_CSV_URL, file=HBO_FILE)
    download_student_inscriptions(url=WO_CSV_URL, file=WO_FILE)

