from pydantic import BaseModel

class AlbumReview(BaseModel):

    modified_at: str
    seo_description: str
    display_name: str
    slug: str
    release_year: int
    dek: str

