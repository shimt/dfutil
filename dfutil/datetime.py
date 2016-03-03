import pandas as pd

"""
日時関連ユーティリティ
"""

def datetime_to_date(datetime_series):
	assert isinstance(datetime_series, pd.Series)

	return pd.Series(
		datetime_series.values.astype("M8[D]"),
		index=datetime_series.index
	)
