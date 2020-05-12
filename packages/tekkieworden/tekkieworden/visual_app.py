import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import pandas as pd
import streamlit as st
import altair as alt
from tekkieworden.config import config
from tekkieworden.processing.munge import prepare_mbo_file
from tekkieworden.processing.readers import open_tech_label_yaml
from tekkieworden.processing.visual_helpers import remove_borders, add_value_labels

groupby_cols = ['instellingsnaam_duo', 'opleidingsnaam_duo',
                'ho_type', 'tech_label', 'soortopleiding_duo']

@st.cache
def load_data_mbo():

    mbo_opl_agg = prepare_mbo_file(groupby_col = 'tech_label')
    return mbo_opl_agg

@st.cache
def load_data_ho():

    data = pd.read_csv(str(config.PATH_TO_MUNGED_DATA) + "/opleidingen_tech_filtered.csv")
    agg_i_cols = data.filter(regex="tot_i", axis=1).columns.tolist()
    agg_d_cols = data.filter(regex="tot_d", axis=1).columns.tolist()
    data = data.groupby(groupby_cols)[agg_i_cols + agg_d_cols].sum().reset_index()
    return agg_i_cols, agg_d_cols, data

# app
st.title('Tech Studies NL aanbod')
st.markdown("""\
        This app illustrates the supply side of tech studies in the Netherlands
    """)
st.image(str(config.PATH_TO_PICS) + "/go_happy_go_tekkie.png", width=300)\

analysis = st.sidebar.selectbox("Choose Analysis", ["Ingeschrevenen", "Gediplomeerden"])

dimvar = st.sidebar.selectbox("select dimension", (groupby_cols))

# matplotlib grid spec
f = plt.figure(figsize=(12, 8))
plt.subplots_adjust(hspace=.4)
gridsize = (3, 2)
ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=1, rowspan=2)
ax2 = plt.subplot2grid(gridsize, (0, 1), colspan=1, rowspan=2)
ax3 = plt.subplot2grid(gridsize, (2, 0), colspan=2)
line_specs = {'kind': 'line', 'marker': 'o', 'cmap': 'Set1', 'alpha': .6}
hline_specs= {'c': 'darkgray', 'linewidth':2, 'zorder': 0, 'alpha': .8, 'linestyle' : "--"}
legend_specs = {'loc': 'best', 'ncol': 2, 'frameon': False}

if analysis == "Ingeschrevenen":
    # data plot 1
    agg_i_cols, _ , df = load_data_ho()
    filter_vars = st.sidebar.multiselect(
                f"Select {dimvar}",
                df[dimvar].unique())

    rename_dict = {'2015_tot_i': '2015',
                   '2016_tot_i': '2016',
                   '2017_tot_i': '2017',
                   '2018_tot_i': '2018',
                   '2019_tot_i': '2019'}
    agg_cols = ['2015', '2016', '2017', '2018', '2019']

    agg_df = df.groupby([dimvar])[agg_i_cols].sum().reset_index()
    agg_df = agg_df.rename(columns=rename_dict)
    agg_melt = pd.melt(frame=agg_df, id_vars=dimvar,
                       value_vars=agg_cols, value_name='ingeschrevenen')

    for name in filter_vars:
        plotset = agg_df[agg_df[dimvar] == name][agg_cols].reset_index(drop=True).T.rename(columns={0: name})
        plotset.plot(ax=ax1, label=name, **line_specs)
    ax1.legend(**legend_specs)
    ax1.set(title='ho')
    # data plot 2
    mbo_opl_agg = load_data_mbo()
    mbo_opl_agg.T.plot(ax=ax2, **line_specs)
    ax2.set(title='mbo')
    # data plot 3
    top = df.groupby([dimvar])['2019_tot_i'].sum().sort_values(ascending=False)
    mean_ = top.mean()
    top15 = top[:15].to_frame().rename(columns={'2019_tot_i': 'ingeschrevenen'})
    top15.plot(kind='bar', ax=ax3, color='indianred', alpha=.4)
    ax3.axhline(y=mean_, **hline_specs)
    # add_value_labels(ax=ax3, spacing=-30)
    ax3.set(ylim=(0, (1.2 * top15.ingeschrevenen.max())))
    ax3.grid(axis="y", linestyle="--")

    for ax in [ax1, ax2, ax3]:
        _ = plt.setp(ax.get_xticklabels(), fontsize=12)
        remove_borders(ax)
        ax.get_yaxis().set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    for ax in [ax1, ax2]:
        _ = plt.setp(ax.get_xticklabels(), rotation='horizontal')

    st.pyplot()

elif analysis == "Gediplomeerden":

    _, agg_d_cols, df = load_data_ho()
    filter_vars = st.sidebar.multiselect(
                f"Select {dimvar}",
                df[dimvar].unique())

    rename_dict = {'2014_tot_d': '2014',
                   '2015_tot_d': '2015',
                   '2016_tot_d': '2016',
                   '2017_tot_d': '2017',
                   '2018_tot_d': '2018'}
    agg_cols = ['2014', '2015', '2016', '2017', '2018']
    # data plot 1
    agg_df = df.groupby([dimvar])[agg_d_cols].sum().reset_index()
    agg_df = agg_df.rename(columns=rename_dict)
    agg_melt = pd.melt(frame=agg_df, id_vars=dimvar,
                       value_vars=agg_cols, value_name='gediplomeerden')
    for name in filter_vars:
        plotset = agg_df[agg_df[dimvar] == name][agg_cols].reset_index(drop=True).T.rename(columns={0: name})
        plotset.plot(ax=ax1, label=name, **line_specs)
    ax1.legend(**legend_specs)
    ax1.set(title='ho')
    # data plot 2
    mbo_opl_agg = load_data_mbo()
    mbo_opl_agg.T.plot(ax=ax2, **line_specs)
    ax2.set(title='mbo')
    # data plot 3
    top = df.groupby([dimvar])['2018_tot_d'].sum().sort_values(ascending=False)
    mean_ = top.mean()
    top15 = top[:15].to_frame().rename(columns={'2018_tot_d': 'gediplomeerden'})
    top15.plot(kind='bar', ax=ax3, color='indianred', alpha=.4)
    ax3.axhline(y=mean_, **hline_specs)
    # add_value_labels(ax=ax3, spacing=-30)
    ax3.set(ylim=(0, (1.2 * top15.gediplomeerden.max())))
    ax3.grid(axis="y", linestyle="--")

    for ax in [ax1, ax2, ax3]:
        _ = plt.setp(ax.get_xticklabels(), fontsize=12)
        remove_borders(ax)
        ax.get_yaxis().set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    for ax in [ax1, ax2]:
        _ = plt.setp(ax.get_xticklabels(), rotation='horizontal')

    st.pyplot()


if st.sidebar.checkbox("Show Data"):
    st.markdown("### Raw Data")
    st.write(agg_df)

if st.sidebar.checkbox("summary"):
    st.markdown("### Summary")
    st.text('summary')

st.info("""\
        [Tekkieworden Github repo](https://github.com/rmania/tekkieworden) 
        | data sources: [Studiekeuze123 (website)](https://www.studiekeuze123.nl/studiekeuzedatabase).
        and [DUO (website)] (https://duo.nl/open_onderwijsdata/databestanden/ho/ingeschreven/) 
    """)
