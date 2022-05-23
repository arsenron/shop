import argparse

import pydantic
from pydantic import validator, HttpUrl



class CliArgs(pydantic.BaseModel):
    bind: HttpUrl
    cfg: str

    @validator("bind", pre=True)
    def set_bind(cls, bind):
        return bind or "http://0.0.0.0:80"

    @validator("cfg", pre=True)
    def set_cfg(cls, cfg):
        return cfg or "cfg.yaml"


def get_cli_args() -> CliArgs:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bind",
        required=False,
    )
    parser.add_argument("--cfg", required=False)
    args, _unknown = parser.parse_known_args()
    return CliArgs(bind=args.bind, cfg=args.cfg)


cli_args = get_cli_args()
