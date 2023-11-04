# ENDPOINT

# POST /sign-up/
```python
body = {
    'login': ...,
    'password': ...
}

response = {
    'status': 201,
    'token': ...,
}
```

# POST /sign-in/
```python
body = {
    'login': ...,
    'password': ...
}

response = {
    'status': 202,
    'token': ...,
}
```

# DELETE /logout/
```python
response = {
    'status': 202,
}
```


# GET /users/
```python
response = {
    'status': 200,
    'content': [
        {
            'id': ...,
            'name': ...,
            'surname': ...,
            'patronymic': ...,
        }
    ]
}
```

# PUT /users/
```python
body = {
    ''
}

response = {
    'status': 200,
    'content': [
        {
            'id': ...,
            'name': ...,
            'surname': ...,
            'patronymic': ...,
        }
    ]
}
```


# POST /galleries/

# GET /galleries/

# PUT /galleries/

# DELETE /galleries/


# POST /galleries/photos/

# GET /galleries/photos/

# PUT /galleries/photos/

# DELETE /galleries/photos/