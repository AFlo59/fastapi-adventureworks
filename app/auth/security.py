from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

# Contexte de hachage
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Création d'un token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Crée un token JWT valide pour une période donnée.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Vérification des mots de passe
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si un mot de passe clair correspond à un mot de passe haché.
    """
    return pwd_context.verify(plain_password, hashed_password)

# Vérification des tokens JWT
def verify_token(token: str):
    """
    Vérifie et décode un token JWT.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )
