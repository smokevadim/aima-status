from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints


class CityDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[str, StringConstraints(max_length=50)]
