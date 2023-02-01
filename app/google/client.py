from googletrans import Translator
from googletrans.models import Translated

from app.google import constants
from app.google.data_parser import Parser
from app.google.data_parser import WordInfo
from app.google.exceptions import GoogleTranslateClientError
from app.google.exceptions import NotValidWordError


class GoogleTranslateClient:

    def __init__(self, source_language: str, target_language: str) -> None:
        # Third party library to send request to the
        # https://translate.google.com . Works pretty good.
        self._translator = Translator(raise_exception=True)
        self._target_language = target_language
        self._source_language = source_language

    def _translate_word(self, word: str) -> Translated:
        try:
            translated_data = self._translator.translate(
                word,
                dest=self._target_language,
                src=self._source_language
            )
        except Exception:
            raise GoogleTranslateClientError(constants.TRANSLATOR_CLIENT_ERROR)
        # If word is not valid then parsed data will have length less than 4.
        # In this case we don't need to save data in the database or return some
        # details about not existing word. Raise exception.
        if len(translated_data.extra_data['parsed']) < 4:
            raise NotValidWordError(constants.NOT_VALID_WORD_TO_GET_INFO)
        return translated_data

    def get_word_info(self, word: str) -> WordInfo:
        translated_data = self._translate_word(word)
        parser = Parser(word, translated_data.extra_data['parsed'][3])
        word_info = parser.parse_data()
        return word_info
