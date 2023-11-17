from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_pascal

def to_pascal_hyphens(snake: str) -> str:
    
    items = [to_pascal(item) for item in snake.split("_")]
    pascal_hyphens = "-".join(items)
    return pascal_hyphens

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_pascal_hyphens,
        populate_by_name=True,
        from_attributes=True
    )

class ApiHeaders(BaseSchema):

    accept: str = "application/json"
    accept_encoding: str = "gzip, deflate, br"
    connection: str = "keep-alive"
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"