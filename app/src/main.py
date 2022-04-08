from types import ModuleType

import uvicorn
from fastapi import FastAPI, Request
from importlib import import_module

import cli
import database
import routers

app = FastAPI()


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

    def add_routers_from_all_modules(self):
        """
        Include routers from all modules and packages if python file
        contains **router** global variable
        """
        routers_dir = "routers"
        for module_name in routers.modules:
            module = import_module(f"{routers_dir}.{module_name}")
            self.include_router(module)

    def include_router(self, module: ModuleType):
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
