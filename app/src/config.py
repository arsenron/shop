from typing import Any

import yaml
from pydantic import BaseSettings, Extra, validator

from src.cli import cli_args
from src.services.calculations.rules import DiscountRule, SameKindRule, ExceedingRule


class Database(BaseSettings):
    user: str
    password: str
    name: str
    host: str
    port: int = 5432
    pool_size: int = 5
    pool_max_size: int = 5
    max_inactive_connection_lifetime: int = 0


class CalculationRules(BaseSettings):
    same_kind_rule: SameKindRule | None = None
    exceeding_rule: ExceedingRule | None = None
    discount_rule: DiscountRule | None = None


class Config(BaseSettings):
    database: Database
    calculation_rules: CalculationRules

    @validator("calculation_rules", pre=True)
    def set_name(cls, v):
        return v or CalculationRules()

    class Config:
        extra = Extra.allow
        env_nested_delimiter = "_"
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            """
            Env settings are more prioritized than values from config
            """
            return (
                init_settings,
                env_settings,
                yaml_config_settings_source,
                file_secret_settings,
            )


def yaml_config_settings_source(_settings: BaseSettings) -> dict[str, Any]:
    with open(cli_args.cfg, "rb") as f:
        cfg = yaml.safe_load(f)
        return dict(database=cfg["database"], calculation_rules=cfg.get("calculation_rules"))


config = Config()
