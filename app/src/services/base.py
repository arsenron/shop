from typing import Type, TypeVar, Callable
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.deps import get_db

Service = TypeVar("T", bound="BaseService")


class BaseService:
    def __init__(self, db: AsyncSession):
        self.db = db


def get_service(
    service_type,
):
    def _get_service(db: AsyncSession = Depends(get_db)) -> Service:
        service = service_type(db=db)
        return service

    return _get_service
