from typing import Any

from googletrans import Translator
from googletrans.models import Translated

from app import constants
from app import validators
from app.data_parser import Parser
from app.exceptions import GoogleTranslateClientError


class GoogleTranslateClient:

    def __init__(self) -> None:
        # Third party library to send request to the
        # https://translate.google.com . Works pretty good.
        self._translator = Translator(raise_exception=True)
        # It can be managed via environment variables.
        # TODO (ibogretsov) Add opportunity to set up target/source languages
        # via environment variables on startup.
        self._target_language = 'ru'
        self._source_language = 'en'

    @property
    def target_language(self) -> str:
        return self._target_language

    @property
    def source_language(self) -> str:
        return self._source_language

    def _translate_word(self, word: str) -> Translated:
        # Unfortunately translator does not have async feature. It can ben ran
        # in separate thread to simulate async code.
        # TODO (ibogretsov): add threading to run
        try:
            translated_data = self._translator.translate(
                word,
                dest=self._target_language,
                src=self._source_language
            )
        except Exception:
            raise GoogleTranslateClientError(constants.TRANSLATOR_CLIENT_ERROR)
        validators.validate_translated_word(translated_data)
        return translated_data

    def get_word_info(self, word: str) -> dict[str, str | Any]:
        translated_data = self._translate_word(word)
        parser = Parser(translated_data.extra_data['parsed'][3])
        parser.parse_data()
        return {
            'word': word,
            'definitions': parser.parsed_data['definitions'],
            'translations': parser.parsed_data['translations'],
            'examples': parser.parsed_data['examples']
        }
