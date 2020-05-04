import logging
import pandas as pd
import argparse
from jinja2 import Environment, FileSystemLoader

from weasyprint import HTML

from tekkieworden.config import config
from tekkieworden.processing.visual_helpers import create_spark_charts


_logger = logging.getLogger(__name__)


def read_tech_file(path, file) -> pd.DataFrame:
    df = pd.read_csv(filepath_or_buffer = path + "/" + file)
    return df


def add_spark_charts(input_df):
    tot_cols = ['tot_2015_duo', 'tot_2016_duo', 'tot_2017_duo',
                'tot_2018_duo', 'tot_2019_duo']
    df_agg = input_df.groupby(['instellingsnaam_duo', 'opleidingsnaam_duo'])[tot_cols].agg('sum').reset_index()

    spark_chart_list = []
    for row in df_agg[tot_cols].values:
        spark_chart_list.append(create_spark_charts(row))
    sparkline = pd.DataFrame(spark_chart_list).rename(columns={0: 'sparkline'})

    df_tech_report = pd.concat([df_agg, sparkline], axis=1)

    return df_tech_report


def create_PDF_report(input_df, output_file):
    template_vars = {"title": "GAP report Tekkieworden",
                     "tech_opleidingen_table": input_df.to_html()}

    env = Environment(loader=FileSystemLoader(str(config.PATH_TO_CSS_FILES) + "/"))
    print(env)
    template = env.get_template("gap_report.html")
    html_out = template.render(template_vars)
    font_config = FontConfiguration()
    HTML(string=html_out).write_pdf(str(config.PATH_TO_GAP_REPORT) + output_file,
                                    stylesheets=[str(config.PATH_TO_CSS_FILES) + "/style.css"],
                                    font_config=font_config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate GAP report')
    parser.add_argument('output_file', type=argparse.FileType('w'),
                        help="GAP output file in PDF")
    args = parser.parse_args()
    # Read in the file and get our pivot table summary
    df = read_tech_file(str(config.PATH_TO_MUNGED_DATA, file = "/opleidingen_tech_filtered.csv"))
    df_tech_report = add_spark_charts(input_df=df)
    create_PDF_report(input_df=df_tech_report, output_file=args.output_file.name)


