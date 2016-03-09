#! /usr/bin/env python

import functools

"""
データフレームのデータをあらかじめ定義したパターンに従って修正するモジュール
"""


class _SetKeyColumn(object):
    pass


def key_column(key_column):
    return (_SetKeyColumn(), key_column)


class _SetValueColumn(object):
    pass


def value_column(value_column):
    return (_SetValueColumn(), value_column)


class _SetSearcher(object):
    pass


def searcher(function):
    return (_SetSearcher(), function)


def _search_df(dataframe, key_column, condition):
    if callable(condition):
        return condition(dataframe[key_column])
    elif isinstance(condition, dict):
        return functools.reduce(
            lambda b1, b2: b1 & b2,
            [_search_df(dataframe, k, c) for k, c in condition.items()]
        )
    elif isinstance(condition, list) or isinstance(condition, tuple):
        return functools.reduce(
            lambda b1, b2: b1 | b2,
            [_search_df(dataframe, key_column, c) for c in condition]
        )
    else:
        return dataframe[key_column] == condition


def _patch_df(dataframe, matches, value_column, value):
    if callable(value):
        dataframe.loc[matches, value_column] = value(dataframe, matches)
    if isinstance(value, dict):
        for k, v in value.items():
            _patch_df(dataframe, matches, k, v)
    else:
        dataframe.loc[matches, value_column] = value


def _setup_searcher(condition, searcher):
    if callable(condition):
        return condition
    elif isinstance(condition, dict):
        return {k: _setup_searcher(c, searcher) for k, c in condition.items()}
    elif isinstance(condition, list) or isinstance(condition, tuple):
        return [_setup_searcher(c, searcher) for c in condition]
    else:
        return searcher(condition)


def patch(
    dataframe, patchset=[],
    key_column=None, value_column=None,
    searcher=None, search_dataframe=None, search_mask=None
):
    if search_dataframe is None:
        search_dataframe = dataframe

    for condition, patch in patchset:

        if isinstance(condition, _SetKeyColumn):
            key_column = patch
            continue
        elif isinstance(condition, _SetValueColumn):
            value_column = patch
            continue
        elif isinstance(condition, _SetSearcher):
            searcher = patch
            continue

        if searcher is not None:
            condition = _setup_searcher(condition, searcher)

        matches = _search_df(search_dataframe, key_column, condition)

        if search_mask is not None:
            matches = matches & search_mask

        _patch_df(dataframe, matches, value_column, patch)


def str_contains(*args, **kwargs):
    return lambda x: x.str.contains(*args, **kwargs)


str_contains_fixed = functools.partial(str_contains, regex=False)
str_contains_regex = functools.partial(str_contains, regex=True)


def str_startswith(*args, **kwargs):
    return lambda x: x.str.startswith(*args, **kwargs)


def str_endswith(*args, **kwargs):
    return lambda x: x.str.endswith(*args, **kwargs)
