class GoogleTranslateClientError(Exception):
    """Google translate API not returned success status"""


class ParserError(Exception):
    """Error to raise if something in translated data could not parsed."""


class NotValidWordError(Exception):
    """
    Error to raise if there are no definitions, examples, translations for word.
    """
