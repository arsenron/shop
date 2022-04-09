from fastapi import APIRouter, Depends, Query
from src.services.cart import ICartService, CartService
from src.models.core.cart import ShoppingCart, TotalAmount

router = APIRouter(prefix="/cart")


@router.put("/add/{product_id}", response_model=TotalAmount)
async def add_to_cart(
    product_id: int, amount: int = Query(1, ge=0), svc: ICartService = Depends(CartService)
):
    return await svc.add_product(product_id, amount)


@router.post("/place", response_model=ShoppingCart)
async def place_order(svc: ICartService = Depends(CartService)):
    cart = await svc.place_order()
    return cart
