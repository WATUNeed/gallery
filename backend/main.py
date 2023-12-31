import subprocess
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from backend.api.base_classes.models import engine, Base
from backend.cache.redis_ import RedisContextManager
from backend.middleware.catch_exceptions import RequestHandlingMiddleware
from backend.middleware.process_time import ProcessTimerMiddleware


templates = Jinja2Templates(directory="frontend")


@asynccontextmanager
async def lifespan(app_: FastAPI):
    from backend.api.auth.routers import auth_router
    from backend.api.user.routers import users_router
    from backend.api.collection.routers import collection_router
    from backend.api.photo.routers import photo_router
    from backend.api.rate.routers import rating_router
    from backend.api.admin_panel.routers import admin_panel_router
    [app_.include_router(router) for router in (
        auth_router, users_router, collection_router, photo_router, rating_router, admin_panel_router
    )]

    from backend.api.user.models import User
    from backend.api.collection.models import Collection, CollectionDownloadQueryHistory
    from backend.api.photo.models import Photo, PhotoRate
    from backend.api.rate.models import Rate
    from backend.events.database import update_photo_rate_after_insert_in_rate
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with RedisContextManager() as redis:
        await redis.connect_fastapi_cache()

    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(RequestHandlingMiddleware)
app.add_middleware(ProcessTimerMiddleware)

if __name__ == '__main__':
    uvicorn.run(app)
