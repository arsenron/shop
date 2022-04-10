import uvicorn
from fastapi import FastAPI, Request
from importlib import import_module
from starlette.middleware.sessions import SessionMiddleware

from src import cli, database, routers

app = FastAPI()
SESSION_SECRET_KEY = "my_super_secret_key"


@app.middleware("http")
async def commit_db_session(request: Request, call_next):
    """
    Commit db_session before response is returned.
    """
    response = await call_next(request)
    db_session = request.state._state.get("db_session")  # noqa
    if db_session:
        await db_session.commit()
    return response


@app.on_event("shutdown")
async def close_database_connection_pools():
    await database.engine.dispose()


class Initializer:
    def initialize(self):
        self.add_routers_from_all_modules()
        app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

    def add_routers_from_all_modules(self):
        """
        Include routers from all modules if a module
        contains **router** global variable
        """
        routers_dir = "routers"
        for module_name in routers.modules:
            module = import_module(f"src.{routers_dir}.{module_name}")
            if hasattr(module, "router"):
                app.include_router(module.router)


Initializer().initialize()


def main():
    server = cli.cli_args.bind
    if server.scheme in ("tcp", "http"):
        uvicorn.run(app, host=server.host, port=int(server.port))
    elif server.scheme == "file":
        uvicorn.run(app, uds=server.path, forwarded_allow_ips="*", proxy_headers=True)


if __name__ == "__main__":
    main()
