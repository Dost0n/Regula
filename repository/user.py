from schemas.user_schema import CreateUserSchema
from sqlalchemy.orm.session import Session
import datetime, uuid
from db.hashing import Hasher
from db.models import User 



def user_create(db:Session, request:CreateUserSchema):
    user_date      = str(datetime.datetime.now())
    user_id        = str(uuid.uuid1())
    user_object = User(
        id           = user_id,
        username     = request.username,
        phone_number = request.phone_number,
        password     = Hasher.get_password_hash(request.password),
        create_at    = user_date,
        update_at    = user_date,
        status       = request.status,
    )
    db.add(user_object)
    db.commit()
    db.refresh(user_object)
    return user_object