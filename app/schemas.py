from typing import List, Optional

from pydantic import BaseModel


class SynonymValueModel(BaseModel):
    type: str
    values: List[str]


class DefinitionValueModel(BaseModel):
    type: str
    value: str
    synonyms: Optional[List[SynonymValueModel]]
    example: Optional[str]


class DefinitionModel(BaseModel):
    speech_part: Optional[str] = None
    values: Optional[List[DefinitionValueModel]]


class Translation(BaseModel):
    speech_part: Optional[str] = None
    values: List[str]


class WordInfo(BaseModel):
    word: str
    definitions: Optional[List[DefinitionModel]]
    examples: Optional[List[str]]
    translations: Optional[List[Translation]]
