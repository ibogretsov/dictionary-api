# Few additional tests for parser
import copy
from typing import Any

import pytest

from app.data_parser import Parser
from tests import constants


@pytest.fixture
def translated_data_translations() -> list[Any]:
    return [
        constants.TRANSLATED_WORD,
        # definitions
        None,
        # examples
        None,
        None,
        None,
        # translations
        constants.TRANSLATED_TRANSLATIONS
    ]


@pytest.fixture
def parsed_data_translations() -> dict[str, Any]:
    return {
        'examples': [],
        'definitions': [],
        'translations': constants.PARSED_TRANSLATIONS
    }


@pytest.fixture
def translated_data_translations_and_examples(
    translated_data_translations
) -> list[Any]:
    data = copy.deepcopy(translated_data_translations)
    data[2] = constants.TRANSLATED_EXAMPLES
    return data


@pytest.fixture
def parsed_data_translations_and_examples(parsed_data_translations):
    data = copy.deepcopy(parsed_data_translations)
    data['examples'] = constants.PARSED_EXAMPLES
    return data


@pytest.fixture
def translated_data_all_fields(
    translated_data_translations_and_examples
) -> list[Any]:
    data = copy.deepcopy(translated_data_translations_and_examples)
    data[1] = constants.TRANSLATED_DEFINITIONS
    return data


@pytest.fixture
def parsed_data_all_fields(parsed_data_translations_and_examples):
    data = copy.deepcopy(parsed_data_translations_and_examples)
    data['definitions'] = constants.PARSED_DEFINITIONS
    return data


@pytest.mark.parametrize('raw,exp', (
    ('translated_data_translations', 'parsed_data_translations'),
    (
        'translated_data_translations_and_examples',
        'parsed_data_translations_and_examples'
    ),
    ('translated_data_all_fields', 'parsed_data_all_fields'),
))
def test_parse_data(request, raw, exp):
    translated_data = request.getfixturevalue(raw)
    exp_data = request.getfixturevalue(exp)
    parser = Parser(translated_data)
    parsed = parser.parse_data()
    assert parsed == exp_data
