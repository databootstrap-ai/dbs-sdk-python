from databootstrap.camel_model import CamelModel
from databootstrap.constants import DEFAULT_API_URL
from urllib.parse import urlencode
import requests
from logging import getLogger

logger = getLogger(__name__)

class Token(CamelModel):
    access_token: str
    refresh_token: str
    expire_minutes: int


def create_token(email: str, password: str, api_url: str = DEFAULT_API_URL) -> str:
    """
    Create a token to access the system.  This token expires.
    """
    url = f"{api_url}/auth/login"
    try:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = urlencode({
            'username': email,
            'password': password
        })

        # return refresh token - which as longer expiration, can make that configurable in the future

        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        
        token = Token.model_validate_json(response.text)
        return token.refresh_token
    except requests.RequestException:
        logger.exception(f"Error calling {url}")
        raise


def refresh_token(api_url: str, refresh_token: str) -> Token:
    url = f"{api_url}/auth/refresh_token"
    try:
        headers = {'Authorization': f'Bearer {refresh_token}'}
        
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        
        return Token.model_validate_json(response.text)
    except requests.RequestException:
        logger.exception("Error calling {url}")
        raise
