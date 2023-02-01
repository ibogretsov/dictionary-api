from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from app import api
from app import config
from app.exceptions import WordNotFoundError
from app.google.exceptions import GoogleTranslateClientError
from app.google.exceptions import NotValidWordError
from app.google.exceptions import ParserError


def _generate_description() -> str:
    """Simple description for the project"""
    from googletrans import constants

    settings = config.get_settings()
    source_language: str = constants.LANGUAGES.get(
        settings.DICTIONARY_API_SOURCE_LANGUAGE
    ).capitalize()
    target_language: str = constants.LANGUAGES.get(
        settings.DICTIONARY_API_TARGET_LANGUAGE
    ).capitalize()
    description: str = f"""Simple API which provides definitions, synonyms,
        examples for {source_language} words and translations from
        {target_language} for these words.
    """
    return description


app = FastAPI(
    title=config.get_settings().APP_NAME,
    description=_generate_description()
)
app.include_router(api.api_router)
add_pagination(app)


@app.get(
    '/',
    summary='Health Check',
    description=(
        'Simple healthchecker to be sure that everying was set up correct.'
    )
)
def index() -> dict[str, str]:
    return {'detail': 'HealthCheck'}


@app.exception_handler(GoogleTranslateClientError)
def google_translator_exception_handler(
    request: Request,
    exc: GoogleTranslateClientError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={'detail': str(exc)}
    )


@app.exception_handler(ParserError)
def parser_exception_handler(
    request: Request,
    exc: ParserError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={'detail': str(exc)}
    )


@app.exception_handler(WordNotFoundError)
def word_not_found_exception_handler(
    request: Request,
    exc: WordNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={'detail': str(exc)}
    )


@app.exception_handler(NotValidWordError)
def not_valid_word_exception_handler(
    request: Request,
    exc: WordNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={'detail': str(exc)}
    )
