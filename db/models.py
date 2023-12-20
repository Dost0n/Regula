from sqlalchemy import Column, ForeignKey, String,  Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'

    id           = Column(String, primary_key=True, index=True)
    username     = Column(String(25))
    phone_number = Column(String(25), unique=True)
    password     = Column(String(255))
    status       = Column(Boolean, default = False)
    create_at    = Column(String(50))
    update_at    = Column(String(50))

    def __repr__(self):
        return f"<User {self.username}>"