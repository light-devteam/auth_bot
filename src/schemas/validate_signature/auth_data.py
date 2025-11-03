from typing import Optional

from pydantic import BaseModel


class ValidateAuthDataRequest(BaseModel):
    id: str
    first_name: str
    last_name: Optional[str] = ''
    username: Optional[str] = ''
    photo_url: Optional[str] = ''
    auth_date: str
    hash: str
