import enum


# single 'I' is also a word
SINGLE_WORD_PATTERN = r'(^[a-z]*|I)$'

# Error messages
WORD_NOT_FOUND = "Word '{word}' not found."


class SortTypeEnum(str, enum.Enum):
    asc = 'asc'
    desc = 'desc'
