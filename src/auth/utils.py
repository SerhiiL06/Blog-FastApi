from passlib.context import CryptContext
from core.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

bearer = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "82e3ff118bcf72358fe6c67c0690c5ed"
ALGORITHM = "HS256"
