from fastapi import FastAPI

from app import api


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
