from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse

from app import api
from app.exceptions import GoogleTranslateClientError


app = FastAPI()
app.include_router(api.api_router)


@app.get(
    '/',
    summary='health check',
    description=(
        'Simple healthchecker to be sure that everying was set up correct.'
    )
)
async def index() -> dict[str, str]:
    return {'detail': 'HealthCheck'}


@app.exception_handler(GoogleTranslateClientError)
async def google_translator_exception_handler(
    request: Request,
    exc: GoogleTranslateClientError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={'message': str(exc)}
    )
