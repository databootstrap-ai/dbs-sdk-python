from databootstrap.camel_model import CamelModel
import requests
from datetime import datetime, timedelta
import logging
from typing import List, Optional
from databootstrap.constants import DEFAULT_API_URL
from databootstrap.auth import refresh_token, Token

logger = logging.getLogger(__name__)

class ChatRequest(CamelModel):
    bucket_path: str
    query: str
    from_suggestion: bool

class SourceDetails(CamelModel):
    url: str
    author: Optional[str]
    title: str
    tip_url: Optional[str] = None


class ChatResponse(CamelModel):
    answer: str
    sources: List[SourceDetails]


class SearchRequest(CamelModel):
    bucket_path: str
    query: str

class SearchResult(CamelModel):
    url: str
    relevant_text: str
    title: Optional[str]
    author: Optional[str]

class SearchResponse(CamelModel):
    search_results: List[SearchResult]

class DataBootstrap():
    def __init__(self, token: str, api_url: str=DEFAULT_API_URL):
        self.latest_token = token  # this is the refresh token
        self._api_url = api_url
        self._token_info: Token = None
        self._expiration = datetime.now()

    def _refresh_token(self):
        self._token_info = refresh_token(self._api_url, self.latest_token)
        self.latest_token = self._token_info.refresh_token
        self._expiration = datetime.now() + timedelta(minutes=self._token_info.expire_minutes)

    def _get_authorization_header(self):
        if self._token_info is None or datetime.now() >= self._expiration:
            self._refresh_token()
 
        return {'Authorization': f'Bearer {self._token_info.access_token}'}


    def chat_query(self, bucket_path: str, query: str, from_suggestion: bool = False) -> ChatResponse:
        url = f"{self._api_url}/chat_query"
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
            response = requests.post(url, headers=headers, json=request_data.model_dump())
            response.raise_for_status()
            
            return ChatResponse.model_validate_json(response.text)
        except requests.RequestException as e:
            logger.exception(f"Error in chat query {url}")
            raise Exception("Error in chat query") from e

    def search_query(self, bucket_path: str, query: str) -> List[SearchResult]:
        url = f"{self._api_url}/search_query"
        try:
            headers = {
                'Content-Type': 'application/json',
                **self._get_authorization_header()
            }
            
            request_data = SearchRequest(
                bucket_path=bucket_path,
                query=query,
            )
            response = requests.post(url, headers=headers, json=request_data.model_dump())
            response.raise_for_status()
            
            return SearchResponse.model_validate_json(response.text).search_results
        except requests.RequestException as e:
            logger.exception(f"Error in search query {url}")
            raise Exception("Error in search query") from e
