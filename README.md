# Data Bootstrap Python SDK

## Tokens

```python 
from databootstrap import create_token, Databootstrap

# Give your credentials created on the website to get a token to use for the api
# You can save this token to use, but it will expire.  This can be refreshed.
token = create_token(email="me@corp.com",password="123")

# create the api
dbs = Databootstrap(token)

# Tokens are automatically cycled as you use the api
# You can save the latest token with an extended expiration 
dbs.latest_token
```

## Chat

```python
# Select the bucket you want to chat with
bucket_path = "biorxiv"
my_statement = "lorem ipsum"
response = dbs.chat_query(bucket_path, my_statement)

print(response.answer)
print(str(response.sources))
```
