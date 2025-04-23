from pydantic import BaseModel, Field, field_validator


class PlayerDTO(BaseModel):
    name: str = Field(
        min_length=1, max_length=30, pattern="^[A-Za-zА-Яа-я]+(\s+[A-Za-zА-Яа-я]+)?$"
    )

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        """Remove extra spaces and format the name"""
        value = " ".join(value.strip().split())
        return value.title()
