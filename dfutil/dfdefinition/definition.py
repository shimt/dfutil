import io

import pandas
import yaml

from dfutil.dfdefinition.transformer import DFTransformer

class DFDefinition(object):
    """データフレーム定義を保持するためのクラス

    Attributes:
        definition (dict): データフレーム定義
    """

    def __init__(self, definition):
        """DFDefinitionクラスのインスタンスを初期化

        Note:
            「Args」セクションに「self」パラメータは記述しない

        Args:
            definition (dict):　データフレーム定義
        """

        assert isinstance(definition, dict)
        self.definition = definition

    def new_transformer(self, **transformer_kwargs):
        """データフレーム定義を基にDFTransformerのインスタンスを作成

        Note:
            「Args」セクションに「self」パラメータは記述しない

        Args:
            transformer_kwargs (dict): DFTransformer.__init__に与えるキーワード引数
        """

        return DFTransformer(self.definition, **transformer_kwargs)

    def transform(self, df, **transform_kwargs):
        """データフレーム定義を基にデータフレームを変形

        Note:
            「Args」セクションに「self」パラメータは記述しない

        Args:
            df (pandas.DataFrame): データフレーム
            transform_kwargs (dict): DFTransformer.transformに与えるキーワード引数
        """

        assert isinstance(df, pandas.DataFrame)

        return self.new_transformer().transform(df, **transform_kwargs)

    @classmethod
    def new_instance_from_textiobase(cls, textiobase):
        """io.TextIOBase(YAMLフォーマット)を読み込みDFDefinitionクラスのインスタンスを作成

        Note:
            「Args」セクションに「cls」パラメータは記述しない

        Args:
            textiobase (io.TextIOBase): データフレーム定義を保持するio.TextIOBase
        """

        assert isinstance(textiobase, io.TextIOBase)

        return cls(yaml.load(textiobase))

    @classmethod
    def new_instance_from_file(cls, filename, **open_kwargs):
        """ファイル(YAMLフォーマット)を読み込みDFDefinitionクラスのインスタンスを作成

        Note:
            「Args」セクションに「cls」パラメータは記述しない

        Args:
            filename (str): ファイル名
            open_kwargs (dict): openに与えるキーワード引数
        """

        assert isinstance(filename, str)

        with open(filename, **open_kwargs) as f:
            return cls.new_instance_from_textiobase(f)

# alias

from_definition_file = DFDefinition.new_instance_from_file
