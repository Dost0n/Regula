from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreateUserSchema(BaseModel):
    phone_number :Optional[str]
    username     :Optional[str]
    password     :Optional[str]
    status       :Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            'example' :{
                'phone_number' :'+123456789123',
                'username'     :'user',
                'password'     :'123',
                'status'       : True,
            }
        }


class ShowUserSchema(BaseModel):
    phone_number :Optional[str]
    username     :Optional[str]
    status       :Optional[bool]
    create_at    :Optional[str]
    
    class Config:
        orm_mode = True