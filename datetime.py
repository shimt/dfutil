import pandas as pd

"""
日時関連ユーティリティを集めたモジュール
"""


def datetime_to_date(datetime_series):
    """datetimeをdateに変換する

    Args:
        datetime_series (pandas.Series):　numpy.datetime64を格納したSeries
    """

    assert isinstance(datetime_series, pd.Series)

    return pd.Series(
        datetime_series.values.astype("M8[D]"),
        index=datetime_series.index
    )
