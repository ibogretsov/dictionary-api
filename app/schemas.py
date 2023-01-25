from pydantic import BaseModel


class SynonymValueModel(BaseModel):
    context: str
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


class DefinitionModel(BaseModel):
    speech_part: str | None = None
    values: list[DefinitionValueModel] | None = None

    class Config:
        orm_mode = True


class Translation(BaseModel):
    speech_part: str | None = None
    values: list[str]

    class Config:
        orm_mode = True


class WordInfo(BaseModel):
    word: str
    definitions: list[DefinitionModel] | None = None
    examples: list[str] | None = None
    translations: list[Translation] | None = None

    class Config:
        orm_mode = True
