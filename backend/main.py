from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from backend.api.base_classes.models import engine, Base
from backend.middleware.catch_exceptions import RequestHandlingMiddleware
from backend.middleware.process_time import ProcessTimerMiddleware


@asynccontextmanager
async def lifespan(app_: FastAPI):
    from backend.api.auth.router import auth_router
    from backend.api.user.routers import users_router

    [app_.include_router(router) for router in (auth_router, users_router)]

    from backend.api.user.models import User

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(RequestHandlingMiddleware)
app.add_middleware(ProcessTimerMiddleware)


if __name__ == '__main__':
    uvicorn.run(app)
