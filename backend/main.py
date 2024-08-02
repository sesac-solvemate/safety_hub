import sys
from pathlib import Path

# 현재 파일의 부모 디렉토리를 sys.path에 추가
sys.path.append(str(Path(__file__).resolve().parent))

import io
from fastapi import FastAPI, File, UploadFile, Form,HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from pyhtml2pdf import converter
import pymongo
import uuid
from typing import Annotated, Optional, List
import numpy as np
import pandas as pd
from datetime import datetime
import json

from enumVar import PROCESS, RISK, EQUIP, RESOURCE, GUIDE, INDUSTRY, COLLECTIONS
import boto3
from botocore.exceptions import NoCredentialsError,ClientError
from fastapi.middleware.cors import CORSMiddleware
# load .env
load_dotenv()
app = FastAPI()
# CORS 설정
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://example.com",  # 필요에 따라 허용할 도메인을 추가
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 도메인 목록
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메서드 (예: GET, POST 등)
    allow_headers=["*"],  # 허용할 HTTP 헤더
)
# MongoDB 설정
MONGO_USER = os.environ.get('MONGO_DB_ROOT_USER_NAME')
MONGO_PASSWORD = os.environ.get('MONGO_DB_ROOT_USER_PASSWORD')
MONGO_HOST = os.environ.get('MONGO_DB_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_DB_PORT', '27017')
print(MONGO_USER, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT)
client = pymongo.MongoClient(
    f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/safetyhub?authSource=admin&retryWrites=true&w=majority")
db = client["safetyhub"]
print(db)

# 현재 파일의 절대 경로
current_dir = os.path.dirname(os.path.abspath(__file__))

s3=boto3.client("s3",
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
)
BUCKET=os.environ.get("AWS_BUCKET_NAME")
S3_URL=os.environ.get("AWS_BUCKET_LOCATION")
def check_object_exists(object_name):
    s3 = boto3.client('s3')
    try:
        s3.head_object(Bucket=BUCKET, Key=object_name)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise
    except NoCredentialsError:
        print("Credentials not available")
        return False
# 파일 업로드 함수
def upload_to_s3(file_name, object_name=None):
    if object_name is None:
        object_name = file_name

    try:
        s3.upload_file(file_name, BUCKET, object_name)
        print(f"File {file_name} uploaded to {BUCKET}/{object_name}")
    except FileNotFoundError:
        print(f"The file {file_name} was not found")
    except NoCredentialsError:
        print("Credentials not available")

# 파일 다운로드 함수
def download_from_s3(object_name, file_name=None):
    if file_name is None:
        file_name = object_name

    try:
        s3.download_file(BUCKET, object_name, file_name)
        print(f"File {file_name} downloaded from {BUCKET}/{object_name}")
    except FileNotFoundError:
        print(f"The file {file_name} was not found")
    except NoCredentialsError:
        print("Credentials not available")


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
    collection = db[COLLECTIONS.RESOURCE]
    collection.insert_one({
        "_id": guideId,
        RESOURCE.STEP: 1,
        RESOURCE.LAST_TIME: datetime.utcnow()
    })
    return guideId


@app.get("/guide/{guideId}")
async def getGuideData(guideId):
    collection = db[COLLECTIONS.RESOURCE]
    data = collection.find_one({"_id": guideId},
                               {"_id": 0, RESOURCE.STEP: 1, RESOURCE.LAST_TIME: 1})
    print("guideId", data)
    return dict(data)


def findIndustryName(industryCode):
    # 컬렉션 선택
    collection = db['industry']

    majCode = industryCode // 1000
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
        return None  # ERROR


@app.get("/guide/{guideId}/{step}")
async def getStepDataFromGuideId(guideId: str, step: int) -> dict:
    collection = db[COLLECTIONS.RESOURCE]
    # if collection is None: //다른 방식으로 있나 없나 체크해야함
    #     return {"error":"no id"}
    query = {"_id": guideId}
    result = {}
    if step == 1:
        data = collection.find_one(query,
                                   {"_id": 0, RESOURCE.COMPANY_NAME: 1, RESOURCE.INDUSTRY_CODE: 1,
                                    RESOURCE.COMPANY_FILE: 1})
        result[RESOURCE.COMPANY_NAME] = data[RESOURCE.COMPANY_NAME]
        result["industryName"] = findIndustryName(data[RESOURCE.INDUSTRY_CODE])
        result[RESOURCE.COMPANY_FILE] = data[RESOURCE.COMPANY_FILE]
        # return result
    elif step == 2:
        data = collection.find_one(query,
                                   {"_id": 0, RESOURCE.TOPIC_TYPE: 1, RESOURCE.TOPIC_ID: 1})
        result = data
    elif step == 3:  # 정해야함
        data = collection.find_one(query,
                                   {"_id": 0, "companyName": 1, "industryCode": 1, "companyFileUrl": 1})
    elif step == 4:
        data = db[COLLECTIONS.GUIDE].find_one(query)
        if data:
            return data
    else:
        return {"error": "step not valid"}
    print(step, result)
    print(type(result))
    return result


@app.get("/industry")
async def getIndustry():
    results = db.industry.find({}, {"_id": 0})
    industry = []
    for x in results:
        industry.append(x)
    print(industry)
    return industry


class Data1(BaseModel):
    companyName: str
    industryCode: int
    companyFile: UploadFile | None = None

class Data2(BaseModel):
    topicType: str
    topicId: int

class Notice(BaseModel):
    type: str
    notice: str

class Contact(BaseModel):
    name: str
    contact: str

class Data3P(BaseModel):
    topicRisk: List[str]
    topicNotice: str
    emergencyNotice: List[Notice]
    emergencyContact: List[Contact]
    map: List[UploadFile]


# step 데이터 저장
@app.post("/step/{guideId}/3/{topicType}")
async def saveStep3Data(guideId, topicType,
                        topicRisk: List[str] = Form(None),
                        topicNotice: Optional[str] = Form(None),
                        emergencyNotice_types: Optional[List[str]] = Form(None),
                        emergencyNotice_messages: Optional[List[str]] = Form(None),
                        emergencyContact_names: Optional[List[str]] = Form(None),
                        emergencyContact_phones: Optional[List[str]] = Form(None),
                        map: Optional[List[UploadFile]] = File(None)
                        ):
    validCheck=db[COLLECTIONS.RESOURCE].find_one({"_id":guideId,RESOURCE.TOPIC_TYPE:topicType})
    if not validCheck:
        return {"err":"pp"}# ERROR
    # emergencyNotice와 emergencyContact를 Notice와 Contact 객체 리스트로 변환
    emergencyNotice = [Notice(type=type, notice=message) for type, message in zip(emergencyNotice_types,
                                                                                  emergencyNotice_messages)] if emergencyNotice_types and emergencyNotice_messages else []
    emergencyContact = [Contact(name=name, contact=phone) for name, phone in zip(emergencyContact_names,
                                                                                 emergencyContact_phones)] if emergencyContact_names and emergencyContact_phones else []
    result = db[COLLECTIONS.RESOURCE].update_one({"_id": guideId}, {"$set":
                                                                        {RESOURCE.TOPIC_RISK: topicRisk,
                                                                         RESOURCE.TOPIC_NOTICE: topicNotice,
                                                                         RESOURCE.EMERGENCY_NOTICE: emergencyNotice,
                                                                         RESOURCE.EMERGENCY_CONTACT: emergencyContact,
                                                                         RESOURCE.COMPANY_MAP: map,
                                                                         RESOURCE.STEP: 4,
                                                                         RESOURCE.LAST_TIME: datetime.utcnow()}
                                                                    })

    print(result.modified_count)
    createSafetyGuide(guideId)


@app.post("/step/{guideId}/1")
async def saveStep1Data(guideId, companyName: str = Form(...),
                        industryCode: int = Form(...),
                        companyFile: Optional[UploadFile] = File(None)):
    print("helo step1")
    print(guideId, companyName, industryCode)
    if companyFile:
        print(companyFile.content_type)
        if companyFile.content_type not in ["application/vnd.ms-excel",
                                     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
            return {"error": "Invalid file type. Please upload an Excel file."}

        # 현재 파일의 절대 경로
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 상대 경로를 사용하여 파일 경로 구성
        filepath={}
        filepath[COLLECTIONS.PROCESS] = os.path.join(current_dir, '..', 'data', f'user_{COLLECTIONS.PROCESS}.json')
        filepath[COLLECTIONS.EQUIP] = os.path.join(current_dir, '..', 'data', f'user_{COLLECTIONS.EQUIP}.json')
        for name in filepath:
            with open(filepath[name], "r", encoding='utf-8') as f:
                data = json.load(f)
                db[name].insert_one({
                    "guideId":guideId,
                    name: data
                })
        riskpath = os.path.join(current_dir, '..', 'data', f'user_{COLLECTIONS.RISK}.json')
        with open(riskpath, "r", encoding='utf-8') as f:
            data = json.load(f)
            for x in data:
                x["guideId"]= guideId
            db[COLLECTIONS.RISK].insert_many(data)

    result = db[COLLECTIONS.RESOURCE].update_one({"_id": guideId}, {"$set":
                                                                        {RESOURCE.COMPANY_NAME: companyName,
                                                                         RESOURCE.INDUSTRY_CODE: industryCode,
                                                                         RESOURCE.COMPANY_FILE: "",
                                                                         RESOURCE.STEP: 2,
                                                                         RESOURCE.LAST_TIME: datetime.utcnow()}
                                                                    })

    print(result.modified_count)
    try:
        s3.upload_fileobj(companyFile.file, BUCKET, f"{guideId}.xlsx")
    except NoCredentialsError:
        raise HTTPException(status_code=400, detail="Credentials not available")
    except ClientError as e:
        raise HTTPException(status_code=400, detail=f"Client error: {e}")
    return {"filename": companyFile.filename}  # , "keys": list(df_dict.keys())}


@app.post("/step/{guideId}/{step}")
async def saveStepData(guideId, step: int, data: Data2):
    print("helo step")
    if step == 2:
        result = db[COLLECTIONS.RESOURCE].update_one({"_id": guideId},
                                                     {"$set":
                                                          {RESOURCE.TOPIC_TYPE: data.topicType,
                                                           RESOURCE.TOPIC_ID: data.topicId,
                                                           RESOURCE.STEP: step + 1,
                                                           RESOURCE.LAST_TIME: datetime.utcnow()}
                                                      })
    elif step == 4:
        pass
    else:
        return {"error": "step not valid"}
    return "OK"


@app.get("/process/{guideId}")
async def getProcessList(guideId):
    data = db[COLLECTIONS.RESOURCE].find_one({"_id": guideId}, {"_id": 0, RESOURCE.INDUSTRY_CODE: 1})
    industryCode = data[RESOURCE.INDUSTRY_CODE]
    processData = db[COLLECTIONS.PROCESS].find_one({PROCESS.INDUSTRY_CODE: industryCode}, {"_id": 0, PROCESS.PROCESS: 1})
    companyProcessData = db[COLLECTIONS.PROCESS].find_one({"guideId": guideId},
                                                   {"_id": 0, PROCESS.PROCESS: 1})

    process={
        "process":processData[PROCESS.PROCESS],
        "companyProcess":companyProcessData[PROCESS.PROCESS]
    }
    return process



@app.get("/equipment/{guideId}")
async def getEquipmentList(guideId):
    data = db[COLLECTIONS.RESOURCE].find_one({"_id": guideId}, {"_id": 0, RESOURCE.INDUSTRY_CODE: 1})
    industryCode = data[RESOURCE.INDUSTRY_CODE]
    equipmentData = db[COLLECTIONS.EQUIP].find_one({EQUIP.INDUSTRY_CODE: industryCode},
                                                   {"_id": 0, EQUIP.EQUIP: 1})
    companyEquipmentData = db[COLLECTIONS.EQUIP].find_one({"guideId": guideId},
                                                          {"_id": 0, EQUIP.EQUIP: 1})
    print(equipmentData)
    print(companyEquipmentData)
    equipment = {
        "equipment": equipmentData[EQUIP.EQUIP],
        "companyEquipment": companyEquipmentData[EQUIP.EQUIP]
    }
    return equipment


@app.get("/risk/{guideId}")
async def getRiskList(guideId):
    data=db[COLLECTIONS.RESOURCE].find_one({"_id":guideId},{"_id":0,RESOURCE.TOPIC_ID:1})
    processId=data[RESOURCE.TOPIC_ID]
    riskData=db[COLLECTIONS.RISK].find_one({RISK.PROCESS_ID:processId},{"_id":0,RISK.RISK:1})
    ownRiskData=db[COLLECTIONS.RISK].find_one({"guideId":guideId},{"_id":0,RISK.RISK:1})
    print(len(riskData[RISK.RISK]),len(ownRiskData[RISK.RISK]))
    return {
        RISK.RISK:riskData[RISK.RISK],
        RISK.OWN_RISK:ownRiskData[RISK.RISK]
    }


@app.get("/risk/{guideId}/choice")
async def getSelectedRiskList(guideId):
    data = db[COLLECTIONS.RESOURCE].find_one({"_id": guideId}, {"_id": 0, RESOURCE.TOPIC_RISK: 1})
    if not data:
        return {"error": "no data"}
    return data[RESOURCE.TOPIC_RISK]

def createSafetyGuide(guideId):
    #model 돌리기

    # model 돌린 결과 출력
    # 상대 경로를 사용하여 파일 경로 구성
    file_path = os.path.join(current_dir, '..', 'data', 'safety_rules_ko.json')
    print(file_path)
    with open(file_path, "r", encoding='utf-8') as f:
        data = json.load(f)
        db[COLLECTIONS.GUIDE].insert_one({
            "_id": guideId,
            "language":{
                "ko":data
            },
            "images": ["url"],
        })
        print(data)
    return data


@app.put("/summary/{guideId}")
async def updateSafetyGuide(guideId):
    return {}


SUPPORT_LANGUAGE = {"ko", "en", "zh", "vi"}


@app.get("/summary/{guideId}/")
async def getSafetyGuideWithLanguage(guideId, language="ko"):
    if language not in SUPPORT_LANGUAGE:
        pass
    # if s3에 있으면 챙겨오기
    filename=f"{guideId}/{language}.html"
    # if check_object_exists(filename):
    #     url=f"{S3_URL}{filename}"
    #     return url
    data=db[COLLECTIONS.GUIDE].find_one({
        "_id": guideId
    })
    if language not in data[GUIDE.LANGUAGE] or not data:
        return {"err":"exist"}
    createHtml(guideId, language)
    return f"{S3_URL}{filename}"


@app.get("/download/{guideId}")
async def download(guideId, language="ko"):
    data = db[COLLECTIONS.GUIDE].find_one({"_id": guideId}, {"_id": 0, GUIDE.DOWNLOAD_URL: 1})
    if not data:
        data = createDownloadUrl(guideId, language)
    url = data[GUIDE.DOWNLOAD_URL]
    return url


def createDownloadUrl(guideId, language=GUIDE.LANGUAGE_KOR):
    html = createHtml(guideId, language)
    htmlToPdf(guideId, html)


def createHtml(guideId, language=GUIDE.LANGUAGE_KOR):
    try:
        resource = db[COLLECTIONS.RESOURCE].find_one({"_id": guideId})
        data = db[COLLECTIONS.GUIDE].find_one({"_id": guideId})
        contents = data[GUIDE.LANGUAGE][language]
        # print(contents)
        body =[" "]*4
        # print(body)
        titles=list(contents.keys())
        # print(titles, titles[0])
        # print(contents[titles[0]])

        tmp=[]
        for subTitle, text in contents[titles[0]].items():
            # print(subTitle,text)
            tmp.append(f'''
            <div class="mini-block">
        <h3>{subTitle}</h3>
        <p>
        {text}
        </p>
    </div>''')
        body[0]="".join(tmp)
        #2
        tmp = []
        for i,(subTitle, text) in enumerate(contents[titles[2]].items()):
            tmp.append(f'''
                    <div class="mini-block">
                <h3>{subTitle}</h3>
                <p>
                {text}
                </p>
            </div>
            {f"<img src={S3_URL}/map.jpg width=300px>" if i==0 else ""}
            ''')
        body[2]="".join(tmp)
        #3
        tmp=[]
        for subTitle, text in contents[titles[3]].items():
            tmp.append(f'''
            <div class="mini-block">
        <h3>{subTitle}</h3>
        <p>
        {text}
        </p>
    </div>''')
        body[3] = "".join(tmp)
        #1
        tmp = []
        for subTitle, subContent in contents[titles[1]].items():
            tmp.append(f'''
                    <div class="mini-block">
                <h3>{subTitle}</h3>
                ''')
            for miniTitle, text in subContent:
                tmp.append(f'''<p>
                <h4>{miniTitle}</h4>
                {text}
                </p>
                ''')
            tmp.append("</div>")
        body[1] = "".join(tmp)

        print("==",body)

        template = f'''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{resource[RESOURCE.COMPANY_NAME]} 안전 교육 자료</title>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

body{{
font-family: Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif;
}}

section{{
    display: block;
    margin: 10px;
    padding: 20px;
    border-radius: 5px;
}}
.title{{
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
}}

.mini-block{{
    display: block;
    margin: 4px;
    padding: 10px 0px;
    /* border: 1px solid #ccc; */
    border-radius: 5px;
}}

    </style>
</head>
<body>
    <section>
        <h2 class="title">
            <img src="https://via.placeholder.com/150" alt="logo" width="20px"/> {titles[0]}
        </h2>
        <hr>{
        "".join(body)
        }          
            </section>
</body>
</html>
    '''
        print(template)
        file = open(f'{guideId}_{language}.html', 'w', encoding='UTF-8')
        file.write(template)
        file.close()
        # s3에도 저장
        upload_to_s3(f'{guideId}_{language}.html', f'{guideId}/{language}.html')

        return  # 저장한 링크~
    except:
        # throw error
        return {"err": "someting is wrong"}


def htmlToPdf(guideId, htmlFileUrl, language=GUIDE.LANGUAGE_KOR):
    # path = os.path.abspath('html_test.html')
    # print(path)
    # converter.convert(f'file:///{path}', 'sample2.pdf')
    converter.convert(htmlFileUrl, f'{guideId}_{language}.pdf')
    # converter.convert('https://pypi.org', 'sample.pdf')
    # s3에 저장
    upload_to_s3(f'{guideId}_{language}.pdf',f'{guideId}/{language}.pdf')

#
# # 파일 저장 경로 설정
# UPLOAD_DIRECTORY = "../uploads"
#
# # 디렉토리가 존재하지 않으면 생성
# if not os.path.exists(UPLOAD_DIRECTORY):
#     os.makedirs(UPLOAD_DIRECTORY)
# def upload_file_to_local(file: UploadFile = File(...), objectName):
#     file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
#
#     with open(file_location, "wb") as f:
#         f.write(await file.read())
