from tekkieworden.processing.munge import prepare_duo_ho_files
from tekkieworden.config import config


def test_prepare_duo_ho_files():

    test_data = prepare_duo_ho_files(path = str(config.PATH_TO_RAW_DATA) + "/",
                                     file=config.DUO_HBO_CSV,
                                     ho_type='hbo')
    single_test_input = test_data[0:1]

    assert len(single_test_input.index) > 0
