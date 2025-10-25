from pydantic import BaseModel


class CommandOption(BaseModel):
    name: str
    description: str
    required: bool = True