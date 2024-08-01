import sys
from pathlib import Path

# 현재 파일의 부모 디렉토리를 sys.path에 추가
sys.path.append(str(Path(__file__).resolve().parent))

import io
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from pyhtml2pdf import converter
import pymongo
import uuid
from typing import Annotated,Optional
import numpy as np
import pandas as pd
from datetime import datetime
import json


from enumVar import PROCESS,RISK,EQUIP,RESOURCE,GUIDE,INDUSTRY,COLLECTIONS

# load .env
load_dotenv()
app = FastAPI()

# MongoDB 설정
MONGO_USER = os.environ.get('MONGO_DB_ROOT_USER_NAME')
MONGO_PASSWORD = os.environ.get('MONGO_DB_ROOT_USER_PASSWORD')
MONGO_HOST = os.environ.get('MONGO_DB_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_DB_PORT', '27017')
print(MONGO_USER,MONGO_PASSWORD,MONGO_HOST,MONGO_PORT)
client = pymongo.MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/safetyhub?authSource=admin&retryWrites=true&w=majority")
db = client["safetyhub"]
collection = db["timestamps"]
print(db)
print(collection)


@app.post("/step/{guideId}/1")
async def saveStepData(guideId, companyName: str=Form(...),
    industryCode: int=Form(...),
    companyFile : Optional[UploadFile] = File(None)):
    print("helo step1")
    print(guideId,companyName,industryCode)
    if companyFile:
        print(companyFile.content_type)
    # if file.content_type not in ["application/vnd.ms-excel",
    #                              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
    #     return {"error": "Invalid file type. Please upload an Excel file."}

    print(COLLECTIONS.RESOURCE)
    result = db[COLLECTIONS.RESOURCE].update_one({"_id": guideId}, {"$set":
                            {RESOURCE.COMPANY_NAME: companyName,
                             RESOURCE.INDUSTRY_CODE: industryCode,
                             RESOURCE.COMPANY_FILE: "",
                             RESOURCE.STEP:2,
                             RESOURCE.LAST_TIME: datetime.utcnow()}
                        })

    print(result.modified_count)

    # try:
    #     # 파일 내용을 읽어 BytesIO 객체로 변환
    #     contents = await companyFile.read()
    #     data = io.BytesIO(contents)
    #
    #     # pandas를 사용하여 Excel 파일 읽기
    #     df_dict = pd.read_excel(data, sheet_name=None)
    #     print(df_dict["1-1 사업장 공정정보"])
    #     # 데이터 확인 (예시: 데이터프레임의 첫 5행 출력)
    #     data_preview = {sheet: df.head().to_dict() for sheet, df in df_dict.items()}
    #     # print(data_preview)
    #     for x in data_preview:
    #         print(f"==={x}===")
    #         print(data_preview[x])
    #         print("--")
    #     # data_preview = {
    #     #     sheet: df.head().replace({pd.NA: None, float('inf'): None, float('-inf'): None}).to_dict()
    #     #     for sheet, df in df_dict.items()
    #     # }
    #     # return {"filename": file.filename, "sheets": list(df_dict.keys()), "data_preview": data_preview}
    #
    # except Exception as e:
    #     return {"error": str(e)}
    return {"filename": companyFile.filename}#, "keys": list(df_dict.keys())}

@app.get("/risk/")
async def getRiskListByKeyword(keyword):
    return []
@app.post("/risk")
async def createRiskData(riskName):

    pass

# @app.delete("/risk/{guideId}")
# async def deleteRisk(guideId):
#     pass

# @app.delete("/summary/{guideId}")
# async def deleteSafetyGuide(guideId):
#     pass

# @app.put("/summary/{guideId}/")
# async def updateOnlySafetyGuideWithLanguage(guideId, language="ko"):
#     if language not in SUPPORT_LANGUAGE:
#         pass
#     return {}