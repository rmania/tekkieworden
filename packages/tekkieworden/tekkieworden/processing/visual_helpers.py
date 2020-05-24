import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
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


def melt_plot_facet_grid(input_df, dim: str, sexe: str,
                         hue_var: str, groupby_var: str,
                         plot_facet_grid=None) -> pd.DataFrame:
    """
    Function to melt pd.Dataframe for plotting purposes
    :param input_df: pd.DataFrame to be melted
    :param dim: dimension to plot:  choose: "i" for ingeschrevenen or "d" for gediplomeerden
    :param sexe: numeric sexe to plot: "man", "vrouw" or "total"
    :param hue_var: HUE variable on wich dimension to split in each plot
    :param groupby_var: value to groupby on
    :return: melted pd.DataFrame or FacetGrid
    """
    dim = dim
    # years differ per ingeschrevenen or gediplomeerden and per update. fix:
    dim_list = tech.filter(regex=rf'_{dim}$').columns.tolist()
    years = np.unique(list(map(lambda sub: int(''.join(
        [x for x in sub if x.isnumeric()])), dim_list)))

    if sexe == 'man':
        dim_cols = [f"{years[0]}_man_{dim}", f"{years[1]}_man_{dim}", f"{years[2]}_man_{dim}",
                    f"{years[3]}_man_{dim}", f"{years[4]}_man_{dim}"]
    elif sexe == 'vrouw':
        dim_cols = [f"{years[0]}_vrouw_{dim}", f"{years[1]}_vrouw_{dim}", f"{years[2]}_vrouw_{dim}",
                    f"{years[3]}_vrouw_{dim}", f"{years[4]}_vrouw_{dim}"]
    elif sexe == 'total':
        dim_cols = [f"{years[0]}_tot_{dim}", f"{years[1]}_tot_{dim}", f"{years[2]}_tot_{dim}",
                    f"{years[3]}_tot_{dim}", f"{years[4]}_tot_{dim}"]

    id_vars = [groupby_var, hue_var]
    value_name = "".join(["ingeschreven" if x == 'i' else 'gediplomeerden' for x in dim])

    melt_frame = (
        pd.melt(
            frame=input_df,
            id_vars=id_vars,
            value_vars=dim_cols,
            var_name=sexe,
            value_name=value_name
        )
            .sort_values(
            by=[
                groupby_var,
                hue_var,
                sexe,
            ]
        )
            .groupby([groupby_var, hue_var, sexe])
            .agg({value_name: "sum"})
            .reset_index()
    )
    melt_frame[sexe] = (melt_frame[sexe]
                        .apply(lambda x: re.sub("[^0-9]", " ", x)))
    melt_frame[sexe] = melt_frame[sexe].astype(int)

    if plot_facet_grid:

        no = len(melt_frame[hue_var].unique())
        palette = dict(zip(melt_frame[hue_var].unique(), sns.color_palette("rocket_r", no)))

        grid = sns.FacetGrid(
            melt_frame,
            col=groupby_var,
            palette=palette,
            col_wrap=4,
            hue=hue_var,
            sharex=False,
            sharey=False,
            height=5,
            aspect=1.5,
        )

        grid.map(plt.axhline, y=melt_frame[value_name].mean(), ls=":", c=".5")
        grid.map(plt.plot, sexe, value_name, marker="o")
        grid.add_legend()

        for ax in grid.axes.flat:
            _ = plt.setp(
                ax.get_xticklabels(), visible=True, size=12
            )  ## set proporty of an artist object
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        return grid

    return melt_frame


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


def add_value_labels(ax, spacing=5, rotation=90):
    """
    Add labels to the end of each bar in a bar chart.
    Args:
     ax (matplotlib.axes.Axes): The matplotlib object containing the axes
         of the plot to annotate.
     spacing (int): distance between the labels and the bars.
     roratation: rotation of labels in degrees
    """

    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        va = "bottom"

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = "top"

        # Use Y value as label and format number
        label = "{:.0f}".format(y_value)

        # Create annotation
        ax.annotate(
            label,  # Use `label` as label
            (x_value, y_value),  # Place label at end of the bar
            xytext=(0, space),  # Vertically shift label by `space`
            textcoords="offset points",  # Interpret `xytext` as offset in points
            ha="center",  # Horizontally center label
            va=va,  # Vertically align label differently for pos vs neg values.
            rotation=rotation,
        )  # rotation of text
