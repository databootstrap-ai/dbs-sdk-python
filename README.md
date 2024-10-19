# Data Bootstrap Python SDK

## Get a Token

```python 
from databootstrap import create_token

# Give your credentials created on the website to get a token to use for the api
# You can save this token to use, but it will expire.  This can be refreshed.
token = create_token(email="me@corp.com",password="123")

print(token)
```

Please save this token.

## Use the Token to establish a connection

```python 
from databootstrap import DataBootstrap

# create the api
dbs = DataBootstrap(token)

# Tokens are automatically rotated as you use the api
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


## Search

```python
# Select the bucket you want to chat with
bucket_path = "biorxiv"
my_search = "lorem ipsum"
search_results = dbs.search_query(bucket_path, my_search)

for result in search_results:
    print(str(result))
```
