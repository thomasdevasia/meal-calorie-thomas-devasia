"""Schemas for get_calories endpoint."""

from pydantic import BaseModel


class similar_result_item(BaseModel):
    dish_name: str
    servings: int
    calories_per_serving: float
    total_calories: float
    protein_per_serving: float
    fat_per_serving: float
    carbohydrates_per_serving: float
    source: str
    brand: str | None
    ingredients: str | None


class dish(BaseModel):
    dish_name: str
    servings: int


class get_calories_response(BaseModel):
    dish_name: str
    servings: int
    calories_per_serving: float
    total_calories: float
    protein_per_serving: float
    fat_per_serving: float
    carbohydrates_per_serving: float
    source: str
    similar_items: list[similar_result_item] | None = []


class get_calories_response_error(BaseModel):
    detail: str
    status: str