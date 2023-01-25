from fastapi import status
from fastapi.testclient import TestClient
import httpx
import pytest
from pytest_mock import MockerFixture

from app import constants
from tests import constants as test_constants
from tests import utils as test_utils


class TestGetWordDetails:

    URL = '/api/words/{word}'

    @pytest.mark.parametrize('word_value,', (
        ' ', ' word', 'word ', 'word and', '1'
    ))
    def test_api_get_word_details_not_valid_word_regrex(
            self,
            client: TestClient,
            word_value: str
    ) -> None:
        resp = client.post(self.URL.format(word=word_value))
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_api_get_word_details_word_is_not_real(
            self,
            client: TestClient,
            mocker: MockerFixture
    ) -> None:
        word = 'notexistingword'
        return_value = (
            test_constants.WORD_NOTEXISTINGWORD_EXP_RAW_TRANSLATE_DATA,
            httpx.Response(status_code=status.HTTP_200_OK)
        )
        resp = test_utils.get_word_details(client, mocker, word, return_value)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert resp.json()['detail'] == constants.NOT_VALID_WORD_TO_GET_INFO

    def test_api_get_word_details_first_from_api(
            self, client: TestClient, mocker: MockerFixture
    ) -> None:
        word = 'test'
        return_value = (
            test_constants.WORD_TEST_EXP_RAW_TRANSLATE_DATA,
            httpx.Response(status_code=status.HTTP_200_OK)
        )
        resp = test_utils.get_word_details(client, mocker, word, return_value)
        assert resp.status_code == status.HTTP_201_CREATED

    def test_api_get_word_details_word_exists_in_db(
            self, client: TestClient, word_word: httpx.Response) -> None:
        word = 'word'
        resp = client.post(self.URL.format(word=word))
        assert resp.status_code == status.HTTP_200_OK

    def test_api_get_word_details_something_went_wrong(
            self, client: TestClient, mocker: MockerFixture
    ) -> None:
        mock_path = 'googletrans.client.Translator.translate'
        mocker.patch(mock_path, side_effect=Exception('Bad request'))
        word = 'test'
        resp = client.post(self.URL.format(word=word))
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert resp.json()['message'] == constants.TRANSLATOR_CLIENT_ERROR


class TestDeleteWord:

    URL = '/api/words/{word}'

    def test_word_not_in_database(self, client: TestClient) -> None:
        word = 'word'
        resp = client.delete(self.URL.format(word=word))
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json()['detail'] == constants.WORD_NOT_FOUND.format(
            word=word
        )

    def test_success(
            self, client: TestClient, word_word: httpx.Response
    ) -> None:
        resp = client.delete(self.URL.format(word=word_word.json()['word']))
        assert resp.status_code == status.HTTP_204_NO_CONTENT

        resp = client.get('/api/words')
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()['total'] == 0


class TestGetWords:

    URL = '/api/words'

    def test_get_words_default_parameters_only_words(
            self, client: TestClient, word_word: httpx.Response
    ) -> None:
        resp = client.get(self.URL)
        assert resp.status_code == status.HTTP_200_OK
        for item in resp.json()['items']:
            assert len(item) == 1
            assert 'word' in item

    def test_get_words_filtering_words_by_pattern(
            self, client: TestClient,
            word_word: httpx.Response,
            word_five: httpx.Response,
            word_final: httpx.Response
    ) -> None:
        # TODO (ibogretsov): rename search to filter (check backend)
        search_pattern = 'fi'
        search_params = {'search': search_pattern}
        resp = client.get(self.URL, params=search_params)
        assert resp.status_code == status.HTTP_200_OK
        # should be 2 words final and five
        assert resp.json()['total'] == 2
        for item in resp.json()['items']:
            assert search_pattern in item['word']

    @pytest.mark.parametrize('field,', (
        'examples', 'definitions', 'translations'
    ))
    def test_get_words_with_additional_fields(
            self,
            client: TestClient,
            field: str,
            word_word: httpx.Response,
    ) -> None:
        query_params = {field: True}
        resp = client.get(self.URL, params=query_params)
        assert resp.status_code == status.HTTP_200_OK
        for item in resp.json()['items']:
            assert field in item

    def test_get_words_pagination(
            self, client: TestClient,
            word_word: httpx.Response,
            word_five: httpx.Response,
            word_final: httpx.Response
    ) -> None:
        # check size without query_params
        resp = client.get(self.URL)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()['items']) > 1
        # with parameters
        query_params = {'page': 1, 'size': 1}
        resp = client.get(self.URL, params=query_params)
        assert len(resp.json()['items']) == 1
