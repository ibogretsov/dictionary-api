import enum


# single 'I' is also a word
SINGLE_WORD_REGEX = r'(^[a-z]*|I)$'

# Error messages
NOT_VALID_WORD_TO_GET_INFO = (
    'Not valid word to get info. Please check if it is real word.'
)
TRANSLATOR_CLIENT_ERROR = (
    'Something went wrong. Please try one more time later.'
)
WORD_NOT_FOUND = "Word '{word}' not found."


class SortTypeEnum(str, enum.Enum):
    asc = 'asc'
    desc = 'desc'
