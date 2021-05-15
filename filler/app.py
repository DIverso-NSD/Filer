from fastapi.openapi.utils import get_openapi

from filler.core.redis import close_redis
import filler.core.settings


def create_app():
    from fastapi import FastAPI

    app = FastAPI()

    from filler.core.routes import router

    app.include_router(router)

    return app


app = create_app()


@app.on_event("shutdown")
async def shutdown_event():
    await close_redis()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Filler",
        version="1.0.0",
        description="API to upload files",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5500)
