from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from db.session import get_db
from typing import List
from routers.login_router import get_current_user_from_token
import datetime, uuid
from db.models import User
from db.hashing import Hasher
import secrets
import random, string, shutil
import base64
from schemas.image_schema import DocumentReader
from repository.image import reader_document
from enum import Enum


class Scenario(str, Enum):
    FullProcess = "FullProcess"
    MrzOrOcr = "MrzOrOcr"
    MrzAndLocate = "MrzAndLocate"
    LocateVisual_And_MrzOrOcr = "LocateVisual_And_MrzOrOcr"
    MrzOrBarcode = "MrzOrBarcode"


router = APIRouter()


@router.post("/image", status_code = status.HTTP_201_CREATED)
async def create_upload_file(uploaded_file: UploadFile = File(...), Scenario: Scenario = Scenario.FullProcess):
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(10))
    new = f'{rand_str}'
    file_type = uploaded_file.filename.rsplit('.',1)[1]
    file_location = f"images/{new}.{file_type}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(uploaded_file.file, file_object)
    
    with open(file_location, "rb") as image_file:
       encoded_image_string = base64.b64encode(image_file.read())
    data = reader_document(encoded_image_string.decode('utf-8'), Scenario)
    return {
        "data"  : data['data'],
        "status": {
            "status_code":data["status_code"],
            "message"   :data["message"],
        }
    }


@router.post("/documentreader")
def document_reader(document:DocumentReader, db: Session = Depends(get_db)):
    data = reader_document(document.image)
    return {
        "data"  : data['data'],
        "status": {
            "status_code":data["status_code"],
            "message"   :data["message"],
        }
    }

