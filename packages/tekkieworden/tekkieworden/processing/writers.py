import logging
import pandas as pd
from tekkieworden.config import config


_logger = logging.getLogger(__name__)


def write_df_csv(input_df, filename):
    """
    Write a pd.Dataframe to csv
    :param input_df: pd.Dataframe to be saved to csv
    :param filename: name of the csv
    :return: outputted csv
    """
    logging.info(f"Writing {len(input_df)} records to {filename}")
    destination = f"{config.PATH_TO_MUNGED_DATA}/{filename}"
    print (f'writing to destination: {destination}')
    input_df.to_csv(destination, index=False)
