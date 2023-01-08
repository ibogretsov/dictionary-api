from typing import Generator

from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
import pymongo
from pymongo.database import Database
import pytest
from pytest import FixtureRequest
from pytest_mock import MockerFixture

from app import deps
from app.main import app
from app.settings.config import Settings
from app.tests import constants as test_constants
from app.tests import utils as test_utils


def get_settings_override() -> Settings:
    return Settings(db_name='testdb') # type: ignore


app.dependency_overrides[deps.get_settings] = get_settings_override


@pytest.fixture
def mongodb(request: FixtureRequest) -> Database:

    def theardown():
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
def word_word(client: TestClient, mocker: MockerFixture) -> Response:
    word = 'word'
    return_value = (
        test_constants.WORD_WORD_EXP_RAW_TRANSLATE_DATA,
        Response(status_code=status.HTTP_200_OK)
    )
    resp = test_utils.get_word_details(client, mocker, word, return_value)
    assert resp.status_code == status.HTTP_201_CREATED
    return resp


@pytest.fixture
def word_final(client: TestClient, mocker: MockerFixture) -> Response:
    word = 'final'
    return_value = (
        test_constants.WORD_FINAL_EXP_RAW_TRANSLATE_DATA,
        Response(status_code=status.HTTP_200_OK)
    )
    resp = test_utils.get_word_details(client, mocker, word, return_value)
    assert resp.status_code == status.HTTP_201_CREATED
    return resp


@pytest.fixture
def word_five(client: TestClient, mocker: MockerFixture) -> Response:
    word = 'five'
    return_value = (
        test_constants.WORD_FIVE_EXP_RAW_TRANSLATE_DATA,
        Response(status_code=status.HTTP_200_OK)
    )
    resp = test_utils.get_word_details(client, mocker, word, return_value)
    assert resp.status_code == status.HTTP_201_CREATED
    return resp
