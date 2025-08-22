from app.core.database import session
from app.services.auth_service import AuthService

def get_auth_service() -> AuthService : 
    return AuthService()

def get_session():
    db = session()
    try:
        yield db
    finally:
        db.close()

