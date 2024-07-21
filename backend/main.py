from fastapi import FastAPI

app=FastAPI()

@app.get("/")
async def first():
    print("hi first")