from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend

from config import JWT_TOKEN

cookie_transport = CookieTransport(cookie_name='libraries', cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=JWT_TOKEN, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name = "raffle",
    transport = cookie_transport,
    get_strategy = get_jwt_strategy,
)