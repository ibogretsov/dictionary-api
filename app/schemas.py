from pydantic import BaseModel

from app.google import data_parser


class DBBaseModel(BaseModel):

    class Config:
        orm_mode = True


# Because we declare schemas manually during parse response from
# translate.google page, we can reuse those schemas
class SynonymValueModel(data_parser.SynonymValue, DBBaseModel):
    pass


class DefinitionValueModel(data_parser.DefinitionValue, DBBaseModel):
    pass


class DefinitionsModel(data_parser.Definitions, DBBaseModel):
    pass


class TranslationsModel(data_parser.Translations, DBBaseModel):
    pass


class WordInfoModel(data_parser.WordInfo, DBBaseModel):
    pass
