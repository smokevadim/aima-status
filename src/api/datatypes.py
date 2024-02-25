from datetime import date
from typing import Any

import pydantic
from pydantic import ConfigDict, model_validator


class DataClass:
    prefix = ''

    def __init__(self, value: str):
        self._value = value[len(self.prefix):] if value.startswith(self.prefix) else value

    @property
    def value(self):
        return self.prefix + self._value

    def __repr__(self):
        return self._value

    def __str__(self):
        return self._value


class City(DataClass):
    prefix = 'city_'


class AIMA(DataClass):
    prefix = 'aima_'


class Article(DataClass):
    prefix = 'article_'


class PreviewData(pydantic.BaseModel):
    date: date
    city: City
    aima: AIMA
    article: Article
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode='before')
    @classmethod
    def string_to_city(cls, data: Any):
        if isinstance(data, dict):
            if 'city' in data:
                data['city'] = City(data['city'])
            if 'aima' in data:
                data['aima'] = AIMA(data['aima'])
            if 'article' in data:
                data['article'] = Article(data['article'])
        return data

    def preview_text(self):
        return f"Date: {self.date}\nCity: {self.city}\nAIMA/SEF: {self.aima}\nArticle: {self.article}"
