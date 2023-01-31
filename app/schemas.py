from pydantic import BaseModel
from pydantic import Field


class SynonymValueModel(BaseModel):
    context: str = 'general'
    values: list[str]

    class Config:
        orm_mode = True


class DefinitionValueModel(BaseModel):
    contexts: list[str] | None = None
    value: str
    synonyms: list[SynonymValueModel] | None = None
    example: str | None = None

    class Config:
        orm_mode = True


class DefinitionsModel(BaseModel):
    speech_part: str | None = None
    values: list[DefinitionValueModel] = Field(default_factory=list)

    class Config:
        orm_mode = True


class TranslationsModel(BaseModel):
    speech_part: str | None = None
    values: list[str] = Field(default_factory=list)

    class Config:
        orm_mode = True


class WordInfoModel(BaseModel):
    word: str
    definitions: list[DefinitionsModel] | None = None
    examples: list[str] | None = None
    translations: list[TranslationsModel] | None = None

    class Config:
        orm_mode = True
