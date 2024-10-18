from databootstrap import DataBootstrap, create_token
from dotenv import load_dotenv
import os

load_dotenv()

def test_chat():
    token = create_token(email=os.getenv('DBS_API_EMAIL'), password=os.getenv('DBS_API_PASSWORD'), api_url=os.getenv('DBS_API_URL'))
    dbs = DataBootstrap(token=token, api_url=os.getenv('DBS_API_URL'))
    res = dbs.chat_query("nd","summarize the declaration of independence")
    print(str(res))