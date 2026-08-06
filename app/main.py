import uvicorn

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.base.exception import BaseError
from app.core.settings import settings

from app.security.auth.router import router as auth

from app.features.roles.router import router as roles
from app.features.users.router import router as users
from app.features.statuses.router import router as statuses
from app.features.orders.router import router as orders
from app.features.executors.router import router as executors


def exception_handler(_, exc: BaseError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.detail})


def main():
    app = FastAPI(title='Order management API', summary='This is a simple API for order management')

    for router in [auth, executors, statuses, roles, orders, users]:
        for route in router.routes:
            route.operation_id = route.name

        app.include_router(router)

    app.add_exception_handler(BaseError, exception_handler)

    uvicorn.run(app, host=settings.uvicorn_host, port=settings.uvicorn_port, root_path=settings.uvicorn_root_path)


if __name__ == '__main__':
    main()
