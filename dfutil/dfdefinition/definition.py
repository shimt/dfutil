import io

import pandas
import yaml

from dfutil.dfdefinition.transformer import DFTransformer

class DFDefinition(object):

    def __init__(self, definition):
        assert isinstance(definition, dict)
        self.definition = definition

    def new_transformer(self, **transformer_kwargs):
        return DFTransformer(self.definition, **transformer_kwargs)

    def transform(self, df, **transform_kwargs):
        assert isinstance(df, pandas.DataFrame)

        return self.new_transformer().transform(df, **transform_kwargs)

    @classmethod
    def from_textiobase(cls, textiobase):
        assert isinstance(textiobase, io.TextIOBase)

        return cls(yaml.load(textiobase))

    @classmethod
    def from_file(cls, filename, **open_kwargs):
        assert isinstance(filename, str)

        with open(filename, **open_kwargs) as f:
            return cls.from_textiobase(f)

# alias

from_definition_file = DFDefinition.from_file
