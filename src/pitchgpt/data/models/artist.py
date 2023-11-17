from pydantic import BaseModel
from pitchgpt.data.models.genre import Genre
from typing import List

class Artist(BaseModel):

    id: str
    display_name: str
    url: str
    genres: List[Genre]