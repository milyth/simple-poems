from pydantic import BaseModel


class Poem(BaseModel):
  #  id: int
    
    title: str
    author: str | None
    content: str 