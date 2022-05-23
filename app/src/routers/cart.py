from fastapi import APIRouter, Depends, Query

from src.services.cart import ICartService, CartService
from src.models.core.cart import ShoppingCart, TotalAmount

from src.lib import response_model

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("", summary="Current cart", responses=response_model(ShoppingCart))
async def get_cart(service: ICartService = Depends(CartService)):
    cart = await service.get_cart()
    return cart


@router.put(
    "/products/{product_id}",
    response_model=TotalAmount,
    summary="Stores products in a cart",
    description="You can control the number of items with "
    "the ```amount``` query parameter. For example, to remove completely all the products"
    " of the same kind, send ```amount``` equal to 0.",
    response_description="Total amount for the cart",
)
async def store_in_cart(
    product_id: int,
    amount: int = Query(1, ge=0, description="Amount of products to store"),
    service: ICartService = Depends(CartService),
):
    return await service.add_product(product_id, amount)


@router.post(
    "",
    responses=response_model(ShoppingCart),
    response_description="Final shopping cart",
    description="Finishes the order and cleans up the cart",
)
async def place_order(service: ICartService = Depends(CartService)):
    cart = await service.place_order()
    return cart
