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
params = {
    'id': ...,
}

body = {
    'name': ...,
    'surname': ...,
    'patronymic': ...,
}

response = {
    'status': 200,
    'content': {
        'id': ...,
        'name': ...,
        'surname': ...,
        'patronymic': ...,
    }
}
```


# POST /galleries/
```python
body = {
    'name': ...,
    'description': ...,
    'photos_ids': [...,],
}

response = {
    'status': 201,
    'content': {
        'name': ...,
        'description': ...,
        'photos': [
            {
                'id': ...,
                'name': ...,
                'description': ...,
                'file': ...,
                'rate': ..., 
                'author': {
                    'id': ...,
                    'name': ...,
                    'surname': ...,
                    'patronymic': ...,
                },
            }
        ],
    }
}
```


# GET /galleries/
```python
params = {
    'order_by': ...,
}

response = {
    'status': 200,
    'content': [
        {
            'name': ...,
            'description': ...,
            'photos': [
                {
                    'id': ...,
                    'name': ...,
                    'description': ...,
                    'file': ...,
                    'rate': ..., 
                    'author': {
                        'id': ...,
                        'name': ...,
                        'surname': ...,
                        'patronymic': ...,
                    },
                }
            ],
        }
    ]
}
```


# PUT /galleries/
```python
body = {
    'name': ...,
    'description': ...,
}

response = {
    'status': 200,
    'content': {
        'name': ...,
        'description': ...,
        'photos': [
            {
                'id': ...,
                'name': ...,
                'description': ...,
                'file': ...,
                'rate': ..., 
                'author': {
                    'id': ...,
                    'name': ...,
                    'surname': ...,
                    'patronymic': ...,
                },
            }
        ],
    }
}
```

# PATCH /galleries/photos/append/
```python
body = {
    'photos': [...,],
}

response = {
    'status': 200,
    'content': {
        'name': ...,
        'description': ...,
        'photos': [
            {
                'id': ...,
                'name': ...,
                'description': ...,
                'file': ...,
                'rate': ..., 
                'author': {
                    'id': ...,
                    'name': ...,
                    'surname': ...,
                    'patronymic': ...,
                },
            }
        ],
    }
}
```

# DELETE /galleries/photos/pop/
```python
body = {
    'photos': [...,],
}

response = {
    'status': 200,
    'content': {
        'name': ...,
        'description': ...,
        'photos': [
            {
                'id': ...,
                'name': ...,
                'description': ...,
                'file': ...,
                'rate': ..., 
                'author': {
                    'id': ...,
                    'name': ...,
                    'surname': ...,
                    'patronymic': ...,
                },
            }
        ],
    }
}
```

# DELETE /galleries/
```python
params = {
    'gallery_id': ...,
}

response = {
    'status': 204,
}
```

# POST /galleries/photos/
```python
body = {
    'id': ...,
    'name': ...,
    'description': ...,
    'file': ...,
    'author_id': ...,
}

response = {
    'status': 201,
    'content': {
        'id': ...,
        'name': ...,
        'description': ...,
        'file': ...,
        'rate': ..., 
        'author': {
            'id': ...,
            'name': ...,
            'surname': ...,
            'patronymic': ...,
        },
    }
}
```

# GET /galleries/photos/
```python
response = {
    'status': 200,
    'content': [
            {
            'id': ...,
            'name': ...,
            'description': ...,
            'file': ...,
            'rate': ..., 
            'author': {
                'id': ...,
                'name': ...,
                'surname': ...,
                'patronymic': ...,
            },
        }
    ]
}
```

# PUT /galleries/photos/
```python
params = {
    'photo_id': ...,
}

body = {
    'name': ...,
    'description': ...,
    'file': ...,
    'author_id': ...,
}

response = {
    'status': 200,
    'content': [
            {
            'id': ...,
            'name': ...,
            'description': ...,
            'file': ...,
            'rate': ..., 
            'author': {
                'id': ...,
                'name': ...,
                'surname': ...,
                'patronymic': ...,
            },
        }
    ]
}
```

# DELETE /galleries/photos/
```python
params = {
    'photo_id': ...,
}

response = {
    'status': 204,
}
```

# POST /galleries/photos/rate/
```python
body = {
    'photo_id': ...,
    'rate': ...,
}
```