import time
from typing import Dict
import jwt
from decouple import config
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def TokenResponse(token: str):
    return {
        "access_token": token
    }


def SignJwt(user_id: str) -> Dict[str, str]:
    """
    The SignJwt function signs a JWT token with the given user_id.
    The function returns a dictionary containing the signed token and an expiration time for it.
    
    :param user_id:str: Identify the user who is making the request
    :return: A dictionary containing the token
    """
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return TokenResponse(token)


def DecodeJwt(token: str) -> dict:
    """
    The DecodeJwt function takes a JWT token as an argument and returns the decoded token if it is valid.
    If the token is not valid, it returns an empty dictionary.
    
    :param token:str: Pass in the jwt token that is being decoded
    :return: A dictionary of the decoded token
    """
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}



class JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.VerifyJwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def VerifyJwt(self, jwtoken: str) -> bool:
        """
        The VerifyJwt function verifies that the JWT token is valid.
        It does this by decoding the JWT token and checking if it has expired.
        If it has not expired, then we know that the user is still authenticated.
        
        :param self: Access variables that belongs to the class
        :param jwtoken:str: Pass the jwtoken string that is passed into the verifyjwt function
        :return: True if the token is valid, and false otherwise
        """
        isTokenValid: bool = True

        try:
            payload = DecodeJwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
