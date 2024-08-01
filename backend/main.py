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


from constant import PROCESS,RISK,EQUIP,RESOURCE,GUIDE,INDUSTRY

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



def updateDatetime():
    current_time = datetime.utcnow()
    print(current_time)
    collection.insert_one({"timestamp": current_time})
    return {"message": "Timestamp added", "time": current_time}

@app.get("/upload/{databaseName}")
async def upload_json_to_database(databaseName):
    # 현재 파일의 절대 경로
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 상대 경로를 사용하여 파일 경로 구성
    file_path = os.path.join(current_dir, '..', 'data', f'{databaseName}.json')
    print(file_path)
    with open(file_path, "r", encoding='utf-8') as f:
        data = json.load(f)
        db[databaseName].insert_many(data)
        print(data)
    return {"file_size": "good"}



@app.get("/guide")
async def createGuideId():
    print("createGid")
    guideId = str(uuid.uuid1())
    db = client["safetyhub"]
    print("DB")
    collection = db['resources']
    print("COlelction")
    collection.insert_one({
        "_id":guideId,
        "step":1
    })
    return guideId

@app.get("/guide/{guideId}")
async def getGuideData(guideId):
    collection = db['resources']
    data = collection.find_one({"_id": guideId},
                           {"_id": 0, "step": 1, "lastTime": 1})
    print("guideId",data)
    return data

def findIndustryName(industryCode):
    # 컬렉션 선택
    collection = db['industry']

    majCode=industryCode//1000
    # 특정 문서 가져오기 (예를 들어, code가 3인 문서)
    document = collection.find_one({"code": majCode})

    # subCategory의 name 찾기
    sub_category_name = None

    # subCategory 필드 추출
    if document:
        mid_categories = document.get("midCategory", [])
        for mid_category in mid_categories:
            sub_categories = mid_category.get("subCategory", [])
            for sub_category in sub_categories:
                if sub_category.get("code") == industryCode:
                    sub_category_name = sub_category.get("name")
                    break
            if sub_category_name:
                break
    if sub_category_name:
        return sub_category_name
    else:
        return None #ERROR


@app.get("/guide/{guideId}/{step}")
async def getStepDataFromGuideId(guideId, step:int):
    collection=db['resources']
    result={}
    if step == 1:
        data = collection.find({ "_id" : guideId},
                                  {"_id": 0, "companyName": 1, "industryCode": 1, "companyFileUrl": 1})
        result["companyName"]=data["companyName"]
        result["industryCode"]=findIndustryName(data["industryCode"])
        result["companyFileUrl"] = data["companyFileUrl"]
    elif step == 2:
        data = collection.find({"_id": guideId},
                                  {"_id": 0, "topicType": 1, "topicId": 1})
        result=data
    elif step == 3: #정해야함
        data = collection.find({"_id": guideId},
                                   {"_id": 0, "companyName": 1, "industryCode": 1, "companyFileUrl": 1})
        pass
    elif step == 4:
        collection=db["guide"]
        data = collection.find_one({"_id": guideId})
        if data:
            return data
        else:
            return {}
    else:
        return {"error": "step not valid"}
        # query_filter = {"author":"sunjae"}
        # update_operation = {"$set":
        #                         {"<field name>": "sunj2-value"}
        #                     }
        # result = collection.update_many(query_filter, update_operation)

    return result

@app.get("/industry")
async def getIndustry():
    results=db.industry.find({},{"_id": 0})
    industry=[]
    for x in results:
        industry.append(x)
    print(industry)
    return industry

class Data1(BaseModel):
    companyName: str
    industryCode: int
    companyFile : UploadFile | None = None

class Data2(BaseModel):
    topicType: str
    topic: int

class Data3E(BaseModel):
    warnings: str

@app.get("/step")
async def stepbystep():
    print("OK")
    return {"step":1}

# step 데이터 저장
@app.post("/step/{guideId}/1")
async def saveStepData(guideId, companyName: str=Form(...),
    industryCode: int=Form(...),
    companyFile : Optional[UploadFile] = File(None)):
    print("helo step1")
    print(companyName,industryCode)
    if companyFile:
        print(companyFile.content_type)
    # if file.content_type not in ["application/vnd.ms-excel",
    #                              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
    #     return {"error": "Invalid file type. Please upload an Excel file."}

    try:
        # 파일 내용을 읽어 BytesIO 객체로 변환
        contents = await companyFile.read()
        data = io.BytesIO(contents)

        # pandas를 사용하여 Excel 파일 읽기
        df_dict = pd.read_excel(data, sheet_name=None)
        print(df_dict["3-3 위험성평가(1)"])
        # 데이터 확인 (예시: 데이터프레임의 첫 5행 출력)
        # data_preview = {sheet: df.head().to_dict() for sheet, df in df_dict.items()}
        # data_preview = {
        #     sheet: df.head().replace({pd.NA: None, float('inf'): None, float('-inf'): None}).to_dict()
        #     for sheet, df in df_dict.items()
        # }
        # return {"filename": file.filename, "sheets": list(df_dict.keys()), "data_preview": data_preview}

    except Exception as e:
        return {"error": str(e)}
    return {"filename": companyFile.filename, "keys": list(df_dict.keys())}

@app.post("/step/{guideId}/{step}")
async def saveStepData(guideId, step:int,data: Data2 | Data3E):
    print("helo step")
    if step == 2:
        pass
    elif step == 3:
        pass
    elif step == 4:
        pass
    else:
        return {"error":"step not valid"}


@app.get("/process/{guideId}")
async def getProcessList(guideId):
    guideData=db.resources.find_one({"_id": guideId},{"industryCode":1})
    if guideData and "industryCode" in guideData:
        defaultData=db.process.find({"industryCode":guideData["industryCode"]})
        ownData = db.process.find({}, {"_id": 0})
        # process = []
        # for x in results:
        #     process.append(x)
        # print(process)
    return []

@app.get("/equipment/{guideId}")
async def getEquipmentList(guideId):
    return []

@app.get("/risk")
async def getRiskList(guideId):
    return []

@app.get("/risk/{guideId}")
async def getSelectedRiskList(guideId):
    return []

@app.post("/risk")
async def createRiskData(riskName):

    pass

@app.put("/risk/{guideId}")
async def updateSelectedRisk(guideId):
    pass

# @app.delete("/risk/{guideId}")
# async def deleteRisk(guideId):
#     pass

@app.get("/risk/")
async def getRiskListByKeyword(keyword):
    return []

@app.post("/summary/{guideId}")
async def createSafetyGuide(guideId):
    return {}

@app.put("/summary/{guideId}")
async def updateSafetyGuide(guideId):
    return {}

@app.delete("/summary/{guideId}")
async def deleteSafetyGuide(guideId):
    pass

SUPPORT_LANGUAGE={"ko", "en", "zh", "vi"}
@app.get("/summary/{guideId}/")
async def getSafetyGuideWithLanguage(guideId, language="ko"):
    if language not in SUPPORT_LANGUAGE:
        pass
    return {}

# @app.put("/summary/{guideId}/")
# async def updateOnlySafetyGuideWithLanguage(guideId, language="ko"):
#     if language not in SUPPORT_LANGUAGE:
#         pass
#     return {}

@app.get("/download/{guideId}")
async def download(guideId):

    return ""


def make_html():
    file = open('html_test.html', 'w', encoding='UTF-8')

    file.write("<html><head><title>테스트 타이틀</title></head><body>테스트 입니다. </body></html>")
    file.close()

def htmlToPdf(htmlFile):
    path = os.path.abspath('html_test.html')
    print(path)
    converter.convert(f'file:///{path}', 'sample2.pdf')
    # converter.convert('https://pypi.org', 'sample.pdf')

def pdfToText(pdfFile):
    reader = PdfReader("example.pdf")
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    # print(reader)
    # print(page)
    print(text)