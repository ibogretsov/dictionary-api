# Few additional tests for parser
import copy
from typing import Any

import pytest

from app.data_parser import Parser
from app.tests import test_translated_data as test_data


@pytest.fixture
def translated_data_translations() -> list[Any]:
    return [
        test_data.TRANSLATED_WORD,
        # definitions
        None,
        # examples
        None,
        None,
        None,
        # translations
        test_data.TRANSLATED_TRANSLATIONS
    ]

@pytest.fixture
def parsed_data_translations() -> dict[str, Any]:
    return {
        'examples': [],
        'definitions': [],
        'translations': test_data.PARSED_TRANSLATIONS
    }

@pytest.fixture
def translated_data_translations_and_examples(
    translated_data_translations
) -> list[Any]:
    data = copy.deepcopy(translated_data_translations)
    data[2] = test_data.TRANSLATED_EXAMPLES
    return data


@pytest.fixture
def parsed_data_translations_and_examples(parsed_data_translations):
    data = copy.deepcopy(parsed_data_translations)
    data['examples'] = test_data.PARSED_EXAMPLES
    return data


@pytest.fixture
def translated_data_all_fields(
    translated_data_translations_and_examples
) -> list[Any]:
    data = copy.deepcopy(translated_data_translations_and_examples)
    data[1] = test_data.TRANSLATED_DEFINITIONS
    return data


@pytest.fixture
def parsed_data_all_fields(parsed_data_translations_and_examples):
    data = copy.deepcopy(parsed_data_translations_and_examples)
    data['definitions'] = test_data.PARSED_DEFINITIONS
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
    raw_data = request.getfixturevalue(raw)
    exp_data = request.getfixturevalue(exp)
    parser = Parser(raw_data)
    parsed = parser.parse_data()
    assert parsed == exp_data
