from fastapi import Request
import uuid


KEY = "shop_session"


def get_cart_id(request: Request) -> str:
    session = request.session
    cart_id = session.get(KEY)
    if not cart_id:
        cart_id = str(uuid.uuid4())
        session[KEY] = cart_id
        return cart_id
    else:
        return cart_id
