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
