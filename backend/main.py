from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from backend.api.base_classes.models import engine, Base
from backend.middleware.catch_exceptions import RequestHandlingMiddleware
from backend.middleware.process_time import ProcessTimerMiddleware


@asynccontextmanager
async def lifespan(app_: FastAPI):
    from backend.api.auth.routers import auth_router
    from backend.api.user.routers import users_router
    from backend.api.collection.routers import collection_router
    from backend.api.photo.routers import photo_router
    [app_.include_router(router) for router in (auth_router, users_router, collection_router, photo_router)]

    from backend.api.user.models import User
    from backend.api.collection.models import Collection
    from backend.api.photo.models import Photo, PhotoRate
    from backend.api.rate.models import Rate
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(RequestHandlingMiddleware)
app.add_middleware(ProcessTimerMiddleware)


if __name__ == '__main__':
    uvicorn.run(app)
