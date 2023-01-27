from typing import Generator

from fastapi import status
from fastapi.testclient import TestClient
import httpx
from pydantic import PostgresDsn
import pytest
from pytest import FixtureRequest
from pytest_mock import MockerFixture
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app import config
from app.db import models
from app.main import app
from tests import constants as test_constants
from tests import utils as test_utils


@pytest.fixture(scope='session')
def sqlalchemy_connect_url() -> PostgresDsn | None:
    return config.get_settings().SQLALCHEMY_DATABASE_URI


@pytest.fixture()
def db(request: FixtureRequest, connection: Engine) -> Session:

    def fin() -> None:
        session.query(models.Word).delete()
        session.commit()

    session: Session = sessionmaker()(bind=connection)
    request.addfinalizer(fin)
    return session


@pytest.fixture
def client(db: Session) -> Generator:
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
