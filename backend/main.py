import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from pyhtml2pdf import converter
import pymongo


path = os.path.abspath('html_test.html')
print(path)
converter.convert(f'file:///{path}', 'sample2.pdf')
# converter.convert('https://pypi.org', 'sample.pdf')


# reader = PdfReader("example.pdf")
# number_of_pages = len(reader.pages)
# page = reader.pages[0]
# text = page.extract_text()
# # print(reader)
# # print(page)
# print(text)



# load .env
load_dotenv()

API_KEY = os.environ.get('MONGO_DB_ROOT_USER_NAME')
MONGO_USER = os.environ.get('MONGO_DB_ROOT_USER_PASSWORD')
MONGO_PASSWORD = os.environ.get('TEST')

app=FastAPI()

client=pymongo.MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@localhost:27017/mydb?authSource=admin&retryWrites=true&w=majority")

class Item(BaseModel):
    name: str
    type: str | None = None

@app.get("/")
async def first():
    print("hi first")
    # make_html()

    db = client["mydb"]
    collection = db['mycol']
    print(client)
    print(client.get_database())
    print(db)
    print(collection)
    data={
        "author":"sunjae"
    }
    result=collection.insert_one(data)
    print(result)
    # print(db.posts.insert_one(data).inserted_id)




@app.post("/guide")
async def createGuideId():
    # UUID
    # save UUID->collections
    return ""

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