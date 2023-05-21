from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from os import getenv
from .world import database
from .routes import router

app = FastAPI()
load_dotenv()


@app.on_event("startup")
async def startup():
    await database.connect(getenv("Database.Path"))
    await database.setup()

@app.on_event("shutdown")
async def shutdown():
    await database.close()

@app.exception_handler(HTTPException)
async def defaultExcHandler(request, exc):
    return {
        'status': 'fail',
        'code': exc.status_code,
        'error': exc.detail or 'INTERNAL_SERVER_ERROR'
    }
    
                             
app.include_router(router)