from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from app import api
from app import config
from app import database
from app.db import models
from app.exceptions import GoogleTranslateClientError
from app.exceptions import ParserError


def _generate_description() -> str:
    """Simple description for the project"""
    from googletrans import constants

    settings = config.get_settings()
    source_language: str = constants.LANGUAGES.get(
        settings.dictionary_api_source_language
    ).capitalize()
    target_language: str = constants.LANGUAGES.get(
        settings.dictionary_api_target_language
    ).capitalize()
    description: str = f"""Simple API which provides definitions, synonyms,
        examples for {source_language} words and translations from
        {target_language} for these words.
    """
    return description


app = FastAPI(description=_generate_description())
app.include_router(api.api_router)
add_pagination(app)

# TODO (ibogretsov): use alembic
models.Base.metadata.create_all(bind=database.engine)


@app.get(
    '/',
    summary='health check',
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
        status_code=status.HTTP_400_BAD_REQUEST, content={'message': str(exc)}
    )


@app.exception_handler(ParserError)
def parser_exception_handler(
    request: Request,
    exc: ParserError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={'message': str(exc)}
    )
