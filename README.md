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


# POST /collections/
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
                'collection_id': ...,
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


# GET /collections/
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
                    'collection_id': ...,
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


# PUT /collections/
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
                'collection_id': ...,
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

# PATCH /collections/photos/append/
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
                'collection_id': ...,
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

# DELETE /collections/photos/pop/
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
                'collection_id': ...,
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

# DELETE /collections/
```python
params = {
    'collection_id': ...,
}

response = {
    'status': 204,
}
```

# POST /collections/photos/
```python
body = {
    'id': ...,
    'name': ...,
    'description': ...,
    'file': ...,
    'author_id': ...,
    'collection_id': ...,
}

response = {
    'status': 201,
    'content': {
        'id': ...,
        'name': ...,
        'description': ...,
        'file': ...,
        'rate': ..., 
        'collection_id': ...,
        'author': {
            'id': ...,
            'name': ...,
            'surname': ...,
            'patronymic': ...,
        },
    }
}
```

# GET /collections/photos/
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
            'collection_id': ...,
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

# PUT /collections/photos/
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
            'collection_id': ...,
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

# DELETE /collections/photos/
```python
params = {
    'photo_id': ...,
}

response = {
    'status': 204,
}
```

# POST /collections/photos/rate/
```python
body = {
    'photo_id': ...,
    'rate': ...,
}
```