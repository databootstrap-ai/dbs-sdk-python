from databootstrap.camel_model import CamelModel
import requests
from datetime import datetime, timedelta
from urllib.parse import urlencode
import logging
from typing import List, Optional

DEFAULT_API_URL = 'https://databootstrap.com/api'

logger = logging.getLogger(__name__)



class ChatRequest(CamelModel):
    bucket_path: str
    query: str
    from_suggestion: bool

class SourceDetails(CamelModel):
    url: str
    author: str
    title: str
    tip_url: Optional[str] = None


class ChatResponse(CamelModel):
    answer: str
    sources: List[SourceDetails]

class DataBootstrap():
    def __init__(self, email, password, api_url=DEFAULT_API_URL):
        self._backend_base = api_url
        self._email = email 
        self._password = password
        self._token = ""
        self._refresh_token = ""
        self._expiration = None

    def _set_tokens(self, token: str, refresh_token: str, expire_minutes: int):
        self._token = token 
        self._refresh_token = refresh_token
        self._expiration = datetime.now() + timedelta(minutes=expire_minutes)

    def _login(self):
        url = f"{self._backend_base}/auth/login"
        try:
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            data = urlencode({
                'username': self._email,
                'password': self._password
            })
            
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            
            data = response.json()
            self._set_tokens(data['accessToken'], data['refreshToken'], data['expireMinutes'])
        except requests.RequestException:
            logger.exception(f"Error calling {url}")
            raise

    def _refresh_token(self):
        url = f"{self._backend_base}/auth/refresh_token"
        try:
            headers = {'Authorization': f'Bearer {self._refresh_token}'}
            
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            self._set_tokens(data['accessToken'], data['refreshToken'], data['expireMinutes'])
        except requests.RequestException:
            logger.exception("Error calling {url}")
            self._token = ""
            self._refresh_token = ""
            self._expiration = None
            raise

    def _get_authorization_header(self):
        if self._expiration is None:
            self._login()
        elif self._expiration and datetime.now() >= self._expiration:
            self._refresh_token()
 
        return {'Authorization': f'Bearer {self._token}'}


    def chat_query(self, bucket_path: str, query: str, from_suggestion: bool = False) -> ChatResponse:
        url = f"{self._backend_base}/chat_query"
        try:
            headers = {
                'Content-Type': 'application/json',
                **self._get_authorization_header()
            }
            
            request_data = ChatRequest(
                bucket_path=bucket_path,
                query=query,
                from_suggestion=from_suggestion
            )
            logger.info("making chat request")
            response = requests.post(url, headers=headers, json=request_data.model_dump())
            response.raise_for_status()
            
            return ChatResponse.model_validate_json(response.text)
        except requests.RequestException as e:
            logger.exception(f"Error in chat query {url}")
            raise Exception("Error in chat query") from e
