from dotenv import load_dotenv
import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


# Authentication logic

# Hashed password with passlib library

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# decode jwt token

bearer = OAuth2PasswordBearer(tokenUrl="token")

# Secret Key and Algorithm for JTW token

SECRET_KEY = "82e3ff118bcf72358fe6c67c0690c5ed"
ALGORITHM = "HS256"


# List of admin user roles
ADMIN_LIST = ["is_staff", "is_superuser"]
