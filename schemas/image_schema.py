from pydantic import BaseModel
from typing import Optional



class DocumentReader(BaseModel):
    image      :Optional[str]