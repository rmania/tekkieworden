import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import altair as alt
from tekkieworden.config import config
from tekkieworden.processing.visual_helpers import remove_borders

groupby_cols = ['instellingsnaam_duo', 'opleidingsnaam_duo', 'ho_type', 'tech_label']

@st.cache
def load_data():

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
st.image(str(config.PATH_TO_PICS) + "/tech_profielen.png", width=600)\

analysis = st.sidebar.selectbox("Choose Analysis", ["Ingeschrevenen", "Gediplomeerden"])

if analysis == "Ingeschrevenen":

    agg_i_cols, _ , df = load_data()

    dimvar = st.sidebar.selectbox("select dimension", (groupby_cols))

    filter_vars = st.sidebar.multiselect(
                f"Select {dimvar}",
                df[dimvar].unique())

    agg_df = df.groupby([dimvar])[agg_i_cols].sum().reset_index()
    agg_melt = pd.melt(frame=agg_df, id_vars=dimvar,
                       value_vars=agg_i_cols, value_name='ingeschrevenen')
    for name in filter_vars:
        c1 = alt.Chart(agg_melt[agg_melt[dimvar] == name]).properties(height=400, width=200).mark_line().encode(
             x=alt.X("variable:O", title="Variable"),
             y=alt.Y('ingeschrevenen:Q', title="ingeschrevenen"),
             color=alt.Color('tech_label:N', title=name)
        )

    top15 = df.groupby(['instellingsnaam_duo'])[agg_i_cols].sum().sum(axis=1).sort_values(ascending=False)[:15]
    top15 = top15.to_frame().rename(columns={0: 'ingeschrevenen'})
    c2 = alt.Chart(top15.reset_index()).properties(width=75).mark_bar().encode(
        x=alt.X("ingeschrevenen:Q", title="ingeschrevenen"),
        y=alt.Y("instellingsnaam_duo:N", title="instellingsnaam_duo", sort=None),
        color=alt.Color('instellingsnaam_duo:N', title="instellingsnaam_duo"),
        tooltip=[alt.Tooltip('instellingsnaam_duo:N', title='instellingsnaam_duo'),
                 alt.Tooltip('ingeschrevenen:Q', title='ingeschrevenen')]
    )
st.altair_chart(alt.hconcat(c1,c2) , use_container_width=True)


if st.sidebar.checkbox("Show Raw Data"):
    st.markdown("### Raw Data")
    st.write(agg_melt)

st.info("""\
        [Tekkieworden Github repo](https://github.com/rmania/tekkieworden) 
        | data sources: [Studiekeuze123 (website)](https://www.studiekeuze123.nl/studiekeuzedatabase).
        and [DUO (website)] (https://duo.nl/open_onderwijsdata/databestanden/ho/ingeschreven/) 
    """)