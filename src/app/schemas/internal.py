from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, PlainSerializer
from pydantic.alias_generators import to_camel


class InternalModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        from_attributes=True,
        populate_by_name=True,
        frozen=True,
    )


DecimalFloat = Annotated[
    Decimal,
    PlainSerializer(
        lambda x: float(x),
        return_type=float,
        when_used="json",
    ),
]
