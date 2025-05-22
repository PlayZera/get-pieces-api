from app.models.user import UserInDB
from app.core.security import verify_password, get_password_hash
from app.core.config import settings

fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": get_password_hash(settings.SECRET_KEY) 
    }
}

class AuthService:
    @staticmethod
    def authenticate_user(username: str, password: str):
        user = AuthService.get_user(username)
        if not user or not verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def get_user(username: str):
        if username in fake_users_db:
            user_dict = fake_users_db[username]
            return UserInDB(**user_dict)
        return None