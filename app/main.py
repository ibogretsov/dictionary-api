from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from app import api
from app.exceptions import GoogleTranslateClientError
from app.exceptions import ParserError


app = FastAPI()
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
