from fastapi import HTTPException, status


class UserException:
    NotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    LoginAlreadyUsed = HTTPException(status_code=status.HTTP_409_CONFLICT, detail='This login already in used.')

