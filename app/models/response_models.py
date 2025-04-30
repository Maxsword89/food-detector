from pydantic import BaseModel

class RecognizeResponse(BaseModel):
    name_eng: str
    name_loc: str
    grams: float
    calories: int
    proteins: float
    fats: float
    carbs: float
