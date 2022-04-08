from fastapi import APIRouter, Depends
from src.services.products import IProductService, ProductService
from src.models.core.products import ProductIn, AllProducts
from src.lib import default_response, default_response_example

router = APIRouter(prefix="/products")


@router.get("/all", response_model=AllProducts)
async def get_all_products(svc: IProductService = Depends(ProductService)):
    return await svc.get_products()


@router.get("/{product_id}")
async def get_product(product_id: int, svc: IProductService = Depends(ProductService)):
    return await svc.get_product_by_id(product_id)


@router.put("", responses=default_response_example)
async def create_product(
    product: ProductIn, svc: IProductService = Depends(ProductService)
):
    await svc.create_product(product)
    return default_response


@router.delete("/{product_id}", responses=default_response_example)
async def remove_product(
    product_id: int, svc: IProductService = Depends(ProductService)
):
    await svc.remove_product(product_id)
    return default_response
