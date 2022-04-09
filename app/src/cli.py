import argparse
import functools

import pydantic
from pydantic import FileUrl, stricturl, validator


AllowedUrl = FileUrl | stricturl(allowed_schemes=["tcp", "http"], tld_required=False)


class CliArgs(pydantic.BaseModel):
    bind: AllowedUrl
    cfg: str

    @validator("bind", pre=True)
    def set_bind(cls, bind):
        return bind or "http://localhost:9999"

    @validator("cfg", pre=True)
    def set_cfg(cls, cfg):
        return cfg or "cfg.yaml"


@functools.cache
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
