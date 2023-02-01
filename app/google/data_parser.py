from typing import Any

import pydantic

from app.google import constants
from app.google.exceptions import ParserError


class SynonymValue(pydantic.BaseModel):
    context: str = 'general'
    values: list[str] = pydantic.Field(default_factory=list)


class DefinitionValue(pydantic.BaseModel):
    value: str
    # One definition can be the same for different contexts.
    # Google API returns it as list, so store it as list as well
    contexts: list[str] | None = None
    synonyms: list[SynonymValue] | None = None
    example: str | None = None


class Definitions(pydantic.BaseModel):
    speech_part: str | None = None
    values: list[DefinitionValue] = pydantic.Field(default_factory=list)


class Translations(pydantic.BaseModel):
    speech_part: str | None = None
    values: list[str] = pydantic.Field(default_factory=list)


class WordInfo(pydantic.BaseModel):
    word: str
    definitions: list[Definitions] | None = None
    examples: list[str] | None = None
    translations: list[Translations] | None = None


class Parser:
    """Parser to extract definitions, translations and examples from data.

        Googletransate library does enough good work to process response from
    translate.google public API. But it is not enough for this microservice.
    It allows gets definitions, synonyms, translation and examples from data
    to save it move user frendly. By default data fetched from google api is
    list of list of list of ... strings or something like this. Each type of
    data is exactly on their correct place. It is good practice to reduce data
    transferring between server and clients, but this microservice should return
    more readable data.
    """

    def __init__(self, word: str, translated_data: Any) -> None:
        self._word = word
        self._data_to_parse: list[Any] = translated_data

    @property
    def raw_examples(self) -> list[Any]:
        """Get raw examples. Always stored on place with index 2."""
        return self._data_to_parse[2][0] if self._data_to_parse[2] else []

    @property
    def raw_translations(self) -> list[Any]:
        """Get raw translations. Always stored on place with index 5."""
        return self._data_to_parse[5][0] if self._data_to_parse[5] else []

    @property
    def raw_definitions(self) -> list[Any]:
        """Get raw definitions. Always stored on place with index 1.

        Definitions store synonyms as well. It is logical, because synonyms
        without definitions are not very helpfull.
        """
        return self._data_to_parse[1][0] if self._data_to_parse[1] else []

    def parse_data(self) -> WordInfo:
        """Process and return parsed data.

        Get and process examples. Save it as examples.
        Get and process translations. Save it as translations.
        Get and process definitions. Save it as definitions.
        """
        word_info = WordInfo(word=self._word)
        try:
            word_info.examples = self.__process_examples()
            word_info.translations = self.__process_translations()
            word_info.definitions = self.__get_definitions()
        # Need to avoid unexpected failure. So catch exceptions which can be
        # raised during paring. And raise ParserError which will be handled
        # in exception handler
        except (KeyError, ValueError, IndexError, TypeError):
            raise ParserError(constants.TRANSLATOR_CLIENT_ERROR)
        return word_info

    def __process_examples(self) -> list[str]:
        """Process examples.

        Workflow is very simple. Just iterate through raw examples and extract
        example text. Also added removing tags for bold font.
        """
        processed_exemples: list[str] = []
        for raw_example in self.raw_examples:
            # Example data is always on place with index 1
            example: str = raw_example[1]
            # remove tags for bold font
            example = example.replace('<b>', '').replace('</b>', '')
            processed_exemples.append(example)
        return processed_exemples

    def __process_translations(self) -> list[Translations]:
        """Process translations.

        Workflow is pretty similar as we do for words examples just with one
        exclusion. Translations are grouped by part of speech ('verb', 'noun',
        etc).
        """
        processed_translations: list[Translations] = []
        for raw_translation in self.raw_translations:
            speech_part: str = raw_translation[0]
            values: list[str] = [rt[0] for rt in raw_translation[1]]
            tr = Translations(
                speech_part=speech_part,
                values=values
            )
            processed_translations.append(tr)
        return processed_translations

    def __get_definitions(self) -> list[Definitions]:
        """Process definitions. Slightly complicated process.

        Synonyms and some examples are presented in definitions, so they will
        be stored with definitions, because synonym without definition does not
        have logical reason.
        """

        def _is_general_definition(definition: list[Any]) -> bool:
            return (len(definition) < 5 or not isinstance(definition[4], list))

        processed_definitions: list[Definitions] = []
        # definitions are grouped by part of speech. So iterate by these groups
        for group_raw_definitions in self.raw_definitions:
            speech_part: str = group_raw_definitions[0]
            speech_part_definitions = Definitions(
                speech_part=speech_part
            )
            raw_definitions_data = group_raw_definitions[1]
            # Within part of speech iterate by each raw definition which
            # contains itself definition, possible synonyms and possible example
            for raw_definition in raw_definitions_data:
                definition = DefinitionValue(
                    value=raw_definition[0]
                )
                if not _is_general_definition(raw_definition):
                    definition.contexts = [
                        context[0] for context in raw_definition[4]
                    ]

                if len(raw_definition) >= 2 and raw_definition[1]:
                    definition.example = raw_definition[1]

                # There are synonyms. Synonyms are on place with index 6
                if len(raw_definition) >= 6:
                    definition.synonyms = self.__get_synonyms(
                        raw_definition[5]
                    )

                speech_part_definitions.values.append(definition)

            processed_definitions.append(speech_part_definitions)

        return processed_definitions

    def __get_synonyms(
            self,
            synonyms_data: list[Any]
    ) -> list[SynonymValue]:
        """Process synonyms for each definition."""
        processed_synonyms: list[SynonymValue] = []
        # First process synonyms in general context, e.g. synonyms without any
        # additional info like 'informal:', 'archaic:' etc (on transalte page
        # these words are highlighted with italic)
        for synonyms in synonyms_data[0]:
            values: list[str] = [syn[0] for syn in synonyms]
            synonym: SynonymValue = SynonymValue(
                values=values
            )
            processed_synonyms.append(synonym)
        # After general synonyms process all other synonyms (informal, archaic
        # etc). At the end of each list is stored synonym context.
        for synonyms in synonyms_data[1:]:
            values: list[str] = [i[0] for i in synonyms[:-1][0]]
            context = synonyms[-1][0][0]
            synonym = SynonymValue(context=context, values=values)
            processed_synonyms.append(synonym)

        return processed_synonyms
