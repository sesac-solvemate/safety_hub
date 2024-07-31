import datetime
import io

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from pyhtml2pdf import converter
import pymongo
import uuid
from typing import Annotated
import numpy as np
import pandas as pd

app=FastAPI()
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    print(file.content_type)
    # if file.content_type not in ["application/vnd.ms-excel",
    #                              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
    #     return {"error": "Invalid file type. Please upload an Excel file."}

    try:
        # 파일 내용을 읽어 BytesIO 객체로 변환
        contents = await file.read()
        data = io.BytesIO(contents)

        # pandas를 사용하여 Excel 파일 읽기
        df_dict = pd.read_excel(data,sheet_name=None)
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
    return {"filename": file.filename,"keys":list(df_dict.keys())}
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



# load .env
load_dotenv()

MONGO_USER = os.environ.get('MONGO_DB_ROOT_USER_NAME')
MONGO_PASSWORD = os.environ.get('MONGO_DB_ROOT_USER_PASSWORD')


client=pymongo.MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@localhost:27017/safetyhub?authSource=admin")

class Item(BaseModel):
    name: str
    type: str | None = None

@app.get("/")
async def first():
    print("hi first")
    # make_html()

    db = client["safetyhub"]
    # collection_list = db.list_collection_names()
    # for c in collection_list:
    #     print(c)
    collection = db['mycol']
    print(client)
    print(client.get_database())
    print(db)
    print(collection)

    # query_filter = {"author":"sunjae"}
    # update_operation = {"$set":
    #                         {"<field name>": "sunj2-value"}
    #                     }
    # result = collection.update_many(query_filter, update_operation)

    results = collection.find({"<field name>":"sunj2-value"})
    print(results)
    print(list(results))
    for document in results:
        print(document)

    # print(db.mycol.insert_one({
    #     "_id":"sunjaehaha",
    #     "author":"jason"
    # }).inserted_id)




@app.post("/guide")
async def createGuideId():
    guideId = str(uuid.uuid1())
    # save UUID->collections
    return guideId

@app.get("/guide/{guideId}")
async def getGuide(guideId):

    return {
        "step": 2,
        "lastTime": datetime.datetime.now()
    }

@app.get("/guide/{guideId}/{step}")
async def getStepDataFromGuideId(guideId, step:int):
    return {

    }

@app.get("/industry")
async def getIndustry():
    return []

@app.post("/step/{guideId}/{step}")
async def saveStepData(guideId, step:int):
    pass

@app.get("/process/{guideId}")
async def getProcessList(guideId):
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
async def createRiskData():
    pass

@app.put("/risk/{guideId}")
async def updateSelectedRisk(guideId):
    pass

@app.delete("/risk/{guideId}")
async def deleteRisk(guideId):
    pass

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

@app.put("/summary/{guideId}/")
async def updateOnlySafetyGuideWithLanguage(guideId, language="ko"):
    if language not in SUPPORT_LANGUAGE:
        pass
    return {}

@app.get("/download/{guideId}")
async def download(guideId):
    return ""


def make_html():
    file = open('html_test.html', 'w', encoding='UTF-8')

    file.write("<html><head><title>테스트 타이틀</title></head><body>테스트 입니다. </body></html>")
    file.close()