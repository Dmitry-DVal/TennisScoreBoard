from pydantic import BaseModel, Field, field_validator


class PlayerDTO(BaseModel):
    name: str = Field(min_length=1, max_length=30,
                      pattern="^[A-Za-zА-Яа-я]+(\s+[A-Za-zА-Яа-я]+)?$")

    @field_validator('name', mode='before')
    @classmethod
    def normalize_name(cls, value: str) -> str:
        """Удаляем лишние пробелы и форматируем имя"""
        value = " ".join(value.strip().split())  # Убираем лишние пробелы
        return value.title()  # Делаем Заглавную букву в начале каждого слова
