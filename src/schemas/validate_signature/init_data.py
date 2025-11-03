from pydantic import BaseModel, SecretStr


class ValidateInitDataRequest(BaseModel):
    init_data: SecretStr
