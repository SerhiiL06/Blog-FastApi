from dotenv import load_dotenv
import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi_mail import ConnectionConfig


load_dotenv(".env")


os.getenv("")

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


# Email config


MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_SERVER = os.getenv("MAIL_SERVER")

MAIL_SSL_TLS = os.getenv("MAIL_SSL_TLS")

MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")


MAIL_CONFIG = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    MAIL_PORT=465,
    MAIL_FROM=MAIL_FROM,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
)
