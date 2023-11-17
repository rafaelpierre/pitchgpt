from pydantic import BaseModel

class Genre(BaseModel):

    display_name: str
    slug: str