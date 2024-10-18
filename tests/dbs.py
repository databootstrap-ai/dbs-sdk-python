import pytest 
from databootstrap import DataBootstrap, create_token
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture
def dbs():
    token = create_token(email=os.getenv('DBS_API_EMAIL'), password=os.getenv('DBS_API_PASSWORD'), api_url=os.getenv('DBS_API_URL'))
    return DataBootstrap(token=token, api_url=os.getenv('DBS_API_URL'))
