from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def welcome_user( ):
    return {"message": "server is up and running"}
