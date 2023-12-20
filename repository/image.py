from sqlalchemy.orm import Session
from schemas.image_schema import DocumentReader
import datetime, uuid
from core.config import settings
import requests
import base64
import json
import objectpath
from enum import Enum


class Scenario(str, Enum):
    FullProcess = "FullProcess"
    MrzOrOcr = "MrzOrOcr"
    MrzAndLocate = "MrzAndLocate"
    LocateVisual_And_MrzOrOcr = "LocateVisual_And_MrzOrOcr"
    MrzOrBarcode = "MrzOrBarcode"



def reader_document(image):
    URL = settings.API_URL
    payload = {
    "processParam": {
    "scenario": f"{Scenario.FullProcess}",
    "doublePageSpread": True,
    "measureSystem": 0,
    "dateFormat": "M/d/yyyy"
  },
        "List": [
    {
      "ImageData": {
        "image": f"{image}"
        },
      "light":6,
      "page_idx":0}]}
    data = {}
    
    try:
        response = requests.post(URL, json = payload)
        ContainerList = response.json()['ContainerList']
        List = ContainerList['List']
        for i in List:
          try:
            Text = i['Text']
            fieldList = Text["fieldList"]
            for j in fieldList:
              fieldName = j['fieldName']
              value = j["value"]
              data[f"{fieldName}"] = value
          except:
            pass
          try:
            Images = i['Images']
            fieldList = Images["fieldList"]
            for z in fieldList:
              fieldName = z['fieldName']
              valueList = z['valueList']
              for x in valueList:
                value = x["value"]
                data[f"{fieldName}"] = value
          except:
            pass
        status_code = response.status_code
        message     = "SUCCESS"
    except requests.exceptions.RequestException:
        status_code = 500
        message     = "SERVER CONNECTION ERROR"
    return {
        "data"       : data,
        "status_code": status_code,
        "message"    : message
        }