from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

# for API's have the json output be camel case instead of snakecase

class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
