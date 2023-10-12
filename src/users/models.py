from pydantic import BaseModel, SecretStr, Field, field_validator


class BaseUser(BaseModel):
    email: str = Field(min_length=8, max_length=100)

    @field_validator('email')
    @classmethod
    def validate_email(cls, value: str) -> str:
        if '@' not in value:
            raise ValueError('Поле email должно содержать "@"')
        return value


class UserRead(BaseUser):
    id: int


class UserInput(BaseUser):
    password: SecretStr = Field(min_length=8, max_length=16)
