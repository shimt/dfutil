import pandas as pd


def _process_column_name(df, d):
    assert isinstance(d, (dict, list, tuple))

    l = df.columns
    if isinstance(d, dict):
        l = l.map(lambda v: d[v] if v in d else v)
    elif isinstance(d, (list, tuple)):
        l = d

    df.columns = l


def _process_additional_column_names(df, d):
    assert isinstance(d, (list, tuple))

    for cn in d:
        if cn not in df.columns:
            df[cn] = None


def _process_index(df, d):
    if "index_column" in d:
        set_index_kwargs = {"inplace": True}
        if "set_index_kwargs" in d:
            set_index_kwargs.update(d["set_index_kwargs"])
        df.set_index(keys=d["index_column"], **set_index_kwargs)

    if "sort" in d:
        if d["sort"]:
            df.sort_index(inplace=True)


def _call_function(function_map, func_or_str, v):
    assert isinstance(function_map, dict)
    assert callable(func_or_str) or isinstance(func_or_str, str)

    function = None

    if callable(func_or_str):
        function = func_or_str
    elif isinstance(func_or_str, str) and func_or_str in function_map:
        function = function_map[func_or_str]
    else:
        function = eval(func_or_str)

    assert callable(function)

    return function(v)


class DFTransformer(object):

    def __init__(
        self, definition,
        convert_function_map={},
        derived_function_map={},
    ):
        assert isinstance(definition, dict)
        assert isinstance(convert_function_map, dict)
        assert isinstance(derived_function_map, dict)

        self.definition = definition
        self.convert_function_map = convert_function_map
        self.derived_function_map = derived_function_map

    def __call_processer(self, df, name, processer, **kwargs):
        if name in self.definition and self.definition[name] is not None:
            processer(df, self.definition[name], **kwargs)

    def __process_column(self, df, d):
        assert isinstance(d, dict)

        for cn, cd in d.items():
            if isinstance(cn, tuple):
                cn = list(cn)

            if cd is None:
                next
            elif "default_value" in cd:
                if pd.isnull(df[cn]).all():
                    df[cn] = cd["default_value"]
            elif "base_column" in cd:
                if "derived_function" in cd:
                    df[cn] = _call_function(
                        self.derived_function_map,
                        cd["derived_function"],
                        df[cd["base_column"]]
                    )
                else:
                    df[cn] = df[cd["basename"]]
            elif "convert_function" in cd:
                df[cn] = _call_function(
                    self.convert_function_map,
                    cd["convert_function"],
                    df[cn]
                )
            elif "category" in cd:
                if cd["category"]:
                    categories = None
                    if isinstance(cd["category"], (list, tuple)):
                        categories = cd["category"]
                    df[cn] = pd.Categorical(df[cn], categories=categories)
            elif "category_piece" in cd:
                categories = None
                if isinstance(cd["category_piece"], (list, tuple)):
                    categories = list(cd["category_piece"])
                    categories.extend(
                        set(df[cn].dropna().drop_duplicates()) -
                        set(categories)
                    )

                df[cn] = pd.Categorical(df[cn], categories=categories)

    def rename_column(self, dataframe):
        assert isinstance(dataframe, pd.DataFrame)
        assert "column_rename_map" in self.definition

        rename_map = self.definition["column_rename_map"]

        assert isinstance(rename_map, dict)

        dataframe.columns = dataframe.columns.map(
            lambda v: rename_map.get(v, v)
        )

    def rename_column_r(self, dataframe):
        assert isinstance(dataframe, pd.DataFrame)
        assert "column_rename_map" in self.definition

        rename_map = {
            v: k for k, v in self.definition["column_rename_map"].items()
        }

        dataframe.columns = dataframe.columns.map(
            lambda v: rename_map.get(v, v)
        )

    def transform(self, dataframe):
        assert isinstance(dataframe, pd.DataFrame)

        df = dataframe.copy()

        if "convert_function_map" in self.definition:
            self.convert_function_map.update(
                self.definition["convert_function_map"]
            )

        if "derived_function_map" in self.definition:
            self.derived_function_map.update(
                self.definition["derived_function_map"]
            )

        # カラム名設定
        self.__call_processer(
            df, "base_column_names",
            _process_column_name
        )

        # カラム追加
        self.__call_processer(
            df, "additional_column_names",
            _process_additional_column_names
        )

        names = []
        names.append("basic_column")
        names.extend(["basic_column{0}".format(i) for i in range(1, 9)])
        names.append("derived_column")
        names.extend(["derived_column{0}".format(i) for i in range(1, 9)])
        names.append("column")
        names.extend(["column{0}".format(i) for i in range(1, 9)])

        for n in names:
            if n in self.definition:
                self.__process_column(df, self.definition[n])

        # インデックス設定

        self.__call_processer(df, "index", _process_index)

        return df

    # 特殊メソッド

    def __call__(*args, **kwargs):
        return DFTransformer.transform(*args, **kwargs)

    def __copy__(self):
        return DFTransformer(
            self.definition.copy(),
            convert_function_map=self.convert_function_map.copy(),
            derived_function_map=self.derived_function_map.copy(),
        )
