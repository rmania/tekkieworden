import logging
import yaml
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
    print(f"writing to destination: {destination}")
    input_df.to_csv(destination, index=False)


def write_excel_to_yaml(input_df, filename):
    """
    writes tech labeling from clusters_tech_labeling.xlsx to yaml file
    :param input_df: excel containing the studies labeling
    :param filename: name to give to the ouputted yaml file
    :return: yaml file (dict)
    """
    tech = pd.read_excel(input_df, usecols=[1, 2, 3]).fillna("no_tech")
    tech["tech"] = tech["tech"].apply(lambda x: x.lower())
    tech_yaml = (
        tech[["opleidingsnaam_duo", "tech"]].set_index("opleidingsnaam_duo").to_dict()
    )

    with open(str(config.PATH_TO_CONFIG) + "/" + filename, "w") as f:
        yaml.dump(tech_yaml, f, default_flow_style=False, indent=2)
