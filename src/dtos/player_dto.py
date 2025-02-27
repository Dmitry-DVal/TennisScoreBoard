from pydantic import BaseModel, Field, field_validator


class PlayerDTO(BaseModel):
    name: str = Field(min_length=2, max_length=25,
                      pattern="^[A-Za-zА-Яа-я]+(\s+[A-Za-zА-Яа-я]+)?$")
    player_number: int = Field(default=None)

    @field_validator('name', mode='before')
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        """Удаляем пробелы в начале и в конце строки. Меняем на формат Заглавной буквы в начале"""
        return value.strip().title()
