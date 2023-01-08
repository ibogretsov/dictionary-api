from fastapi import status
from fastapi.testclient import TestClient
import pymongo
import pytest

from app import deps
from app.main import app
from app.settings.config import Settings


def get_settings_override():
    return Settings(db_name='testdb')


app.dependency_overrides[deps.get_settings] = get_settings_override


@pytest.fixture
def client() -> TestClient:
    with TestClient(app=app) as cl:
        yield cl


@pytest.fixture
def mongodb(request):

    def theardown():
        for collection in db.list_collections():
            db.drop_collection(collection['name'])

    settings = get_settings_override()
    client = pymongo.MongoClient(settings.dictionary_api_mongodb_url)
    db = getattr(client, settings.db_name)
    request.addfinalizer(theardown)
    return db


@pytest.fixture
def word_word(client, mongodb):
    word = 'word'
    resp = client.post(f'/api/words/{word}')
    assert resp.status_code == status.HTTP_201_CREATED
    return resp.json()


@pytest.fixture
def word_word(client, mongodb):
    word = 'word'
    resp = client.post(f'/api/words/{word}')
    assert resp.status_code == status.HTTP_201_CREATED
    return resp.json()

@pytest.fixture
def word_final(client, mongodb):
    word = 'final'
    resp = client.post(f'/api/words/{word}')
    assert resp.status_code == status.HTTP_201_CREATED
    return resp.json()


@pytest.fixture
def word_five(client, mongodb):
    word = 'five'
    resp = client.post(f'/api/words/{word}')
    assert resp.status_code == status.HTTP_201_CREATED
    return resp.json()
