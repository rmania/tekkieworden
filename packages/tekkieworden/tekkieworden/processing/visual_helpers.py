import seaborn as sns
import matplotlib.pyplot as plt
import math

spark_chars = u"▁▂▃▄▅▆▇█"
"""Eight unicode characters of (nearly) steadily increasing height."""


def _isan(n):
    return not math.isnan(n)


def create_spark_charts(series, minimum=None, maximum=None):
    """
    Converts pd.Series to a sparkline string.

    Example:
    >>> create_spark_charts([ 0.5, 1.2, 3.5, 7.3, 8.0, 12.5, float("nan"), 15.0, 14.2,\
    11.8, 6.1 1.9 ])
    u'▁▁▂▄▅▇ ██▆▄▂'
    Raises ValueError if input data cannot be converted to float.
    Raises TypeError if series is not an iterable.
    """
    series = [float(n) for n in series]
    if all(math.isnan(n) for n in series):
        return u" " * len(series)

    minimum = min(filter(_isan, series)) if minimum is None else minimum
    maximum = max(filter(_isan, series)) if maximum is None else maximum
    data_range = maximum - minimum
    if data_range == 0.0:
        # Graph a baseline if every input value is equal.
        return u"".join([spark_chars[0] for i in series])
    coefficient = (len(spark_chars) - 1.0) / data_range

    def clamp(n):
        return min(max(n, minimum), maximum)

    def spark_for(n):
        return spark_chars[int(round(clamp(n) - minimum) * coefficient)]

    return u"".join(spark_for(n) if _isan(n) else " " for n in series)


def plot_facet_grid(input_df, hue_var, groupby_var):
    """
    create seaborn FacetGrid lineplot
    :param input_df: melted pd.DataFrame
    :param hue_var: HUE variable
    :param groupby_var: value to groupby on
    :return: Matplotlib ax
    """
    id_vars = ["instellingsnaam_duo", "opleidingsnaam_duo", groupby_var, hue_var]

    no = len(input_df[hue_var].unique())
    palette = dict(zip(input_df[hue_var].unique(), sns.color_palette("rocket_r", no)))

    grid = sns.FacetGrid(
        input_df,
        col=groupby_var,
        palette=palette,
        col_wrap=4,
        hue=hue_var,
        sharex=False,
        sharey=False,
        height=5,
        aspect=1.5,
    )

    grid.map(plt.axhline, y=0, ls=":", c=".5")

    grid.map(plt.plot, "variable", "inschrijvingen", marker="o")
    grid.add_legend()

    for ax in grid.axes.flat:
        _ = plt.setp(
            ax.get_xticklabels(), visible=True
        )  ## set proporty of an artist object

    return grid


def remove_borders(ax, left=False, bottom=False, right=True, top=True):
    """
    Remove chart junk from matplotlib plots.
    Args
    ----------
    axes : fi. plt.subplots()
    left : bool (default: `False`)
        Hide left axis spine if True.
    bottom : bool (default: `False`)
        Hide bottom axis spine if True.
    right : bool (default: `True`)
        Hide right axis spine if True.
    top : bool (default: `True`)
        Hide top axis spine if True.
    """

    ax.spines["top"].set_visible(not top)
    ax.spines["right"].set_visible(not right)
    ax.spines["bottom"].set_visible(not bottom)
    ax.spines["left"].set_visible(not left)
    if bottom:
        ax.tick_params(bottom=False, labelbottom=False)
    if top:
        ax.tick_params(top=False)
    if left:
        ax.tick_params(left=False, labelleft=False)
    if right:
        ax.tick_params(right=False)
