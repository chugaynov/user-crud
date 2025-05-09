from app.schemas.internal import DecimalFloat, InternalModel
from pydantic.fields import Field


class UserResponse(InternalModel):
    userName: str = Field(title="Логин пользователя", description="Логин пользователя")
    firstName: str = Field(title="Имя", description="Имя")
    lastName: str = Field(title="Фамилия", description="Фамилия")
    email: str = Field(title="Электронная почта", description="Электронная почта")
    phone: str = Field(title="Телефон", description="Телефон")


class UserIdResponse(InternalModel):
    id: int = Field(title="Идентификатор пользователя", description="Идентификатор пользователя")
