from typing import Generator

from fastapi import status
from fastapi.testclient import TestClient
import httpx
import pymongo
from pymongo.database import Database
import pytest
from pytest import FixtureRequest
from pytest_mock import MockerFixture

from app import config
from app.main import app
from tests import constants as test_constants
from tests import utils as test_utils


def get_settings_override() -> config.Settings:
    return config.Settings(db_name='testdb')  # type: ignore


app.dependency_overrides[config.get_settings] = get_settings_override


@pytest.fixture
def mongodb(request: FixtureRequest) -> Database:
    """Simple mongodb fixture which is used in tests instead of "production"
    database.

    After each test clean up database (remove all collections created in test).
    To avoid unexpected results.
    """

    def theardown() -> None:
        for collection in db.list_collections():
            db.drop_collection(collection['name'])

    settings = get_settings_override()
    client = pymongo.MongoClient(settings.dictionary_api_mongodb_url)
    db = getattr(client, settings.db_name)
    request.addfinalizer(theardown)
    return db


@pytest.fixture
def client(mongodb: Database) -> Generator:
    with TestClient(app=app) as cl:
        yield cl


@pytest.fixture
def word_word(client: TestClient, mocker: MockerFixture) -> httpx.Response:
    word = 'word'
    return_value = (
        test_constants.WORD_WORD_EXP_RAW_TRANSLATE_DATA,
        httpx.Response(status_code=status.HTTP_200_OK)
    )
    resp = test_utils.get_word_details(client, mocker, word, return_value)
    assert resp.status_code == status.HTTP_201_CREATED
    return resp


@pytest.fixture
def word_final(client: TestClient, mocker: MockerFixture) -> httpx.Response:
    word = 'final'
    return_value = (
        test_constants.WORD_FINAL_EXP_RAW_TRANSLATE_DATA,
        httpx.Response(status_code=status.HTTP_200_OK)
    )
    resp = test_utils.get_word_details(client, mocker, word, return_value)
    assert resp.status_code == status.HTTP_201_CREATED
    return resp


@pytest.fixture
def word_five(client: TestClient, mocker: MockerFixture) -> httpx.Response:
    word = 'five'
    return_value = (
        test_constants.WORD_FIVE_EXP_RAW_TRANSLATE_DATA,
        httpx.Response(status_code=status.HTTP_200_OK)
    )
    resp = test_utils.get_word_details(client, mocker, word, return_value)
    assert resp.status_code == status.HTTP_201_CREATED
    return resp
