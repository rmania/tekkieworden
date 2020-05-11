import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from tekkieworden.config import config
from tekkieworden.processing.visual_helpers import remove_borders


filter_regex_i = "tot_i"
filter_regex_d = "tot_d"

st.title('Tech Studies NL')

@st.cache
def load_data():
    data = pd.read_csv(str(config.PATH_TO_MUNGED_DATA) + "/opleidingen_tech_filtered.csv")
    agg_i_cols = data.filter(regex=filter_regex_i, axis=1).columns.tolist()
    agg_d_cols = data.filter(regex=filter_regex_d, axis=1).columns.tolist()
    data = data.groupby(['instellingsnaam_duo', 'opleidingsnaam_duo'])[agg_i_cols + agg_d_cols].sum().reset_index()
    return agg_i_cols, agg_d_cols, data

agg_i_cols, agg_d_cols, df = load_data()

dimvar = st.sidebar.selectbox("select dimension", ('opleidingsnaam_duo', 'instellingsnaam_duo'))
print (dimvar)

varname = st.sidebar.selectbox(
    "Select Variable",
    (agg_i_cols, agg_d_cols)
)


filter_vars = st.sidebar.multiselect(
    f"Select {dimvar}",
    df[dimvar].unique()
)


f, ax = plt.subplots(figsize=(12,8))
remove_borders(ax)

agg_df = df.groupby([dimvar])[varname].sum().reset_index()

for name in filter_vars:
    plotset = agg_df[agg_df[dimvar] == name][varname].T
    ax.plot(plotset, marker="o", label=name)
ax.legend(frameon=False, loc='upper center', ncol=2)
st.pyplot()

if st.sidebar.checkbox("Show Raw Data"):
    st.markdown("### Raw Data")
    st.write(agg_df)
