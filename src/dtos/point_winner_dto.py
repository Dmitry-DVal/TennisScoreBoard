from pydantic import BaseModel, Field


class PointWinnerDTO(BaseModel):
    player: int = Field(ge=0, le=1)
