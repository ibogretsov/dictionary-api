from typing import Any


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

    def __init__(self, raw_data: Any) -> None:
        self._raw_data: list[Any] = raw_data
        self._parsed_data: dict[str, Any] = {}

    @property
    def raw_data(self) -> list[Any]:
        return self._raw_data

    @property
    def raw_examples(self) -> list[Any]:
        """Get raw examples. Always stored on place with index 2."""
        return self._raw_data[2][0] if self._raw_data[2] else []

    @property
    def raw_translations(self) -> list[Any]:
        """Get raw translations. Always stored on place with index 5."""
        return self._raw_data[5][0] if self._raw_data[5] else []

    @property
    def raw_definitions(self) -> list[Any]:
        """Get raw definitions. Always stored on place with index 1.

        Definitions store synonyms as well. It is logical, because synonyms
        without definitions are not very helpfull.
        """
        return self._raw_data[1][0] if self._raw_data[1] else []

    @property
    def parsed_data(self) -> dict[str, Any]:
        return self._parsed_data

    def parse_data(self) -> dict[str, list[Any]]:
        """Process and return parsed data.

        Get and process examples. Save it as examples.
        Get and process translations. Save it as translations.
        Get and process definitions. Save it as definitions.
        """
        self.parsed_data['examples'] = self.__process_examples(
            self.raw_examples
        )
        self.parsed_data['translations'] = self.__process_translations(
            self.raw_translations
        )
        self.parsed_data['definitions'] = self.__get_definitions(
            self.raw_definitions
        )
        return self.parsed_data

    def __process_examples(self, raw_examples: list[list[str]]) -> list[str]:
        """Process examples.

        Workflow is very simple. Just iterate through raw examples and extract
        example text. Also added removing tags for bold font.
        """
        processed_exemples: list[str] = []
        for raw_example in raw_examples:
            # Example data is always on place with index 1
            example: str = raw_example[1]
            # remove tags for bold font
            example = example.replace('<b>', '').replace('</b>', '')
            processed_exemples.append(example)
        return processed_exemples

    def __process_translations(
            self,
            raw_translations: list[Any]
    ) -> list[dict[str, str | list[str]]]:
        """Process translations.

        Workflow pretty similar with exceptions just with one exclusion.
        Translations are grouped by part of speech ('verb', 'noun', etc).
        """
        processed_translations: list[dict[str, str | list[str]]] = []
        for raw_translation in raw_translations:
            speech_part: str = raw_translation[0]
            processed_translations.append({
                'speech_part': speech_part,
                'values': [tr[0] for tr in raw_translation[1]]
            })
        return processed_translations

    def __get_definitions(
            self,
            raw_definitions: list[Any]
    ) -> list[dict[str, Any]]:
        """Process definitions. Slightly complicated process.

        Synonyms are presented in definitions, so they will be stored with
        definitions, because synonym without definition does not have logical
        reason.
        """

        def _is_general_definition(definition: list[Any]) -> bool:
            return (
                len(raw_definition) < 5 or
                not isinstance(raw_definition[4], list)
            )

        processed_definitions: list[dict[str, Any]] = []
        for group_raw_definitions in raw_definitions:
            speech_part: str = group_raw_definitions[0]
            speech_part_definitions: dict[str, str | list[Any]] = {
                'speech_part': speech_part,
                'values': []
            }
            raw_definitions_data = group_raw_definitions[1]
            for raw_definition in raw_definitions_data:
                definition: dict[str, str | list[Any]] = {
                    'type': 'general',
                    'value': raw_definition[0]
                }
                if not _is_general_definition(raw_definition):
                    definition['type'] = raw_definition[4][0][0]

                if len(raw_definition) >= 2:
                    definition['example'] = raw_definition[1]

                # There are synonyms. Synonyms are on place with index 6
                if len(raw_definition) >= 6:
                    definition['synonyms'] = self.__get_synonyms(
                        raw_definition[5]
                    )

                speech_part_definitions['values'].append(definition)

            processed_definitions.append(speech_part_definitions)

        return processed_definitions

    def __get_synonyms(
            self,
            raw_synonyms_data: list[Any]
    ) -> list[dict[str, str | list[str]]]:
        """Process synonyms for each definition."""
        processed_synonyms: list[dict[str, str | list[str]]] = []
        # First process general synonyms, e.g. Synonyms withou any additional
        # info like 'informal', 'archaic' etc (on transalte page these words
        # are highlighted with italic)
        general_synonyms: dict[str, str | list[str]] = {
            'type': 'general',
            'values': []
        }
        for raw_synonym in raw_synonyms_data[0]:
            if isinstance(raw_synonym, list):
                for _raw_synonym in raw_synonym:
                    general_synonyms['values'].append(_raw_synonym[0])
            else:
                general_synonyms['values'].append(raw_synonym[0])
        processed_synonyms.append(general_synonyms)

        # After general synonyms process all other synonyms (informal, archaic
        # etc). At the end of each list is stored synonym type.
        for other in raw_synonyms_data[1:]:
            processed_synonyms.append({
                'type': other[-1][0][0],
                'values': [i[0] for i in other[:-1][0]]
            })

        return processed_synonyms
