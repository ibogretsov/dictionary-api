from fastapi.testclient import TestClient
import httpx
from pytest_mock import MockerFixture


def get_word_details(
        client: TestClient,
        mocker: MockerFixture,
        word: str,
        return_value: tuple[str, httpx.Response]
) -> httpx.Response:
    """Simple function which returns mocked response for test words."""
    mock_path = 'googletrans.client.Translator._translate'
    mocker.patch(mock_path, return_value=return_value)
    resp = client.post(f'/api/words/{word}')
    return resp
