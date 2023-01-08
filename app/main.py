from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from app import api
from app.core import config
from app.exceptions import GoogleTranslateClientError
from app.exceptions import ParserError


def _generate_description():
    from googletrans import constants

    settings = config.get_settings()
    source_language = constants.LANGUAGES.get(
        settings.dictionary_api_source_language
    ).capitalize()
    target_language = constants.LANGUAGES.get(
        settings.dictionary_api_target_language
    ).capitalize()
    description = f"""Simple API which provides for words for source
        language {source_language} translations from {target_language},
        definitions, synonyms and examples.
    """
    return description


app = FastAPI(description=_generate_description())
app.include_router(api.api_router)
add_pagination(app)


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
def google_translator_exception_handler(
    request: Request,
    exc: ParserError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={'message': str(exc)}
    )
