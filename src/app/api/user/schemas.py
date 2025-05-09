from pydantic import EmailStr
from pydantic.fields import Field
from app.schemas.internal import DecimalFloat, InternalModel


class UserScheme(InternalModel):
    userName: str = Field(title="User login", examples=["chugaynov"], max_length=256)
    firstName: str = Field(title="Fist name", examples=["Aleksander"], max_length=256)
    lastName: str = Field(title="Last name", examples=["Chugaynov"], max_length=256)
    email: EmailStr
    phone: str = Field(title="Phone number", examples=["+79123456789"], max_length=256)


class UserIdScheme(InternalModel):
    id: int = Field(title="User unique ID", examples=[23])
