from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import UserModel

def jwt_required_middleware(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            
            # Check also user actually exist in the database
            user_id = get_jwt_identity()
            UserModel.find_by_id(user_id)  
        except Exception as e:
            # If the token is missing or invalid, return an error response
            return {"message": "Missing or invalid JWT token", "error": str(e)}, 401

        return fn(*args, **kwargs)
    
    return wrapper