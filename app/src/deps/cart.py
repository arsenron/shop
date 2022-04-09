import uuid

from fastapi import Request


KEY = "shop_session"


def get_session_id(request: Request) -> str:
    session = request.session
    session_id = session.get(KEY)
    if not session_id:
        session_id = str(uuid.uuid4())
        session[KEY] = session_id
        return session_id
    else:
        return session_id
