from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_pascal
import pydantic

def to_pascal_hyphens(snake: str) -> str:
    
    items = [to_pascal(item) for item in snake.split("_")]
    pascal_hyphens = "-".join(items)
    return pascal_hyphens


class BaseApiSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_pascal_hyphens,
        populate_by_name=True,
        from_attributes=True
    )

class ApiHeaders(BaseApiSchema):

    accept: str = "application/json"
    accept_encoding: str = "gzip, deflate, br"
    connection: str = "keep-alive"
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

class PitchGptConfig(BaseModel):

    base_url: str = "https://pitchfork.com/api/v2/search/?types=reviews&hierarchy=sections%2Freviews%2Falbums%2Cchannels%2Freviews%2Falbums&sort=publishdate%20desc%2Cposition%20asc&size={size}&start={start}"
    api_headers: ApiHeaders = ApiHeaders()

    @pydantic.computed_field()
    @property
    def headers(self) -> dict:
        return self.api_headers.model_dump(by_alias = True)