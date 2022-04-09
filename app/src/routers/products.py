from fastapi import APIRouter, Depends

from src.services.products import ProductService
from src.models.core.products import ProductIn, Products, Product, ProductId
from src.lib import default_response, default_response_example

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=Products, summary="Return all the available products")
async def get_all_products(service: ProductService = Depends()):
    return await service.get_products()


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int, service: ProductService = Depends()):
    return await service.get_product_by_id(product_id)


@router.put(
    "",
    response_model=ProductId,
    response_description="Id of the product",
    summary="Creates a new or updates a current product",
)
async def create_or_update_product(
    product: ProductIn, service: ProductService = Depends()
):
    return await service.create_or_update_product(product)


@router.delete("/{product_id}", responses=default_response_example)
async def remove_product(product_id: int, service: ProductService = Depends()):
    await service.remove_product(product_id)
    return default_response
