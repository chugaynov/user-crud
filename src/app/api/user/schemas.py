from pydantic import EmailStr
from pydantic.fields import Field
from app.schemas.internal import DecimalFloat, InternalModel


class UserScheme(InternalModel):
    userName: str = Field(title="User login", examples=["chugaynov"])
    firstName: str = Field(title="Fist name", examples=["Aleksander"])
    lastName: str = Field(title="Last name", examples=["Chugaynov"])
    email: EmailStr
    phone: str = Field(title="Phone number", examples=["+79123456789"])


class UserIdScheme(InternalModel):
    id: int = Field(title="User unique ID", examples=[23])
