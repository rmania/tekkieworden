import logging
import pandas as pd
import sys

sys.path.insert(0, "../")
sys.path.insert(0, "../db_config/")

from sdb_config import drop_studiekeuze_cols
from config import DUO_HBO_CSV, DUO_WO_CSV

PATH_TO_RAW_DATA = '../../../data/raw/'


def read_sdb_opleidingen(path, file):
    """
    Read in the Studiekeuze excel Opleidingen Sheet
    """
    df = pd.read_excel(path + file, sheet_name="Opleidingen")
    logging.info(f'dropping columns: \n {drop_studiekeuze_cols}')
    for col in drop_studiekeuze_cols:
        df = df.drop(col, axis=1)
    df.columns = df.columns.str.lower()
    # check with Tekkieworden
    logging.info(f'putting filter on:{df.actieveopleiding.name} == 1.0')
    df = df[df.actieveopleiding == 1.0]
    df.columns = df.columns + '_sdb'
    logging.info(f'Studiekeuze opledingen frame shape: {df.shape}')
    
    return df


def read_duo_ho_files(path, file):
    """
    Reads in and fprmats DUO files
    """
    df = pd.read_csv(path + file, sep=";")
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(" ", "_")
    for c in ['gemeentenummer', 'opleidingscode_actueel']:
        df[c] = df[c].map("{:.0f}".format).astype(str)
    
    rename_column_dict = {'gemeentenummer': 'gemeentenummer_duo',
                          'brin_nummer_actueel': 'brinnummer_duo',
                          'instellingsnaam_actueel': 'instellingsnaam_duo',
                          'opleidingscode_actueel': 'opleidingscode_duo',
                          'opleidingsnaam_actueel': 'opleidingsnaam_duo'}
    df = df.rename(columns = rename_column_dict)
    
    logging.info(f"{file} shape: {df.shape}")
    return df


def concat_unstack_duo_ho_files():
    
    hbo = read_duo_ho_files(path = PATH_TO_RAW_DATA, file = DUO_HBO_CSV)
    wo = read_duo_ho_files(path = PATH_TO_RAW_DATA, file = DUO_WO_CSV)
    duo = pd.concat([wo, hbo], axis=0)
    logging.info(f"Reading {DUO_HBO_CSV, DUO_WO_CSV}. Concatting files. \n. Duo file: {duo.shape}")
    
    logging.info('summing MAN, VROUW into TOTAL')
    duo_ = (duo.groupby(['brinnummer_duo' ,'instellingsnaam_duo','gemeentenummer_duo',
                     'opleidingsnaam_duo','opleidingscode_duo','geslacht'])['2019'].sum()
            .unstack('geslacht')).reset_index(drop=False)
    duo_['tot_2019_duo'] = duo_['man'].add(duo_['vrouw'])
    logging.info(f'Extract \n: {duo_.head(5)}')
    
    return duo_