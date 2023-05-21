from fastapi import FastAPI, HTTPException, Response, status
from aiosqlite import IntegrityError
from dotenv import load_dotenv
from os import getenv
from .world import database, insertPoem,  listPoems
from .schemas import Poem

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
    
                             
@app.get("/api/v1/list")
async def list():
    """
    Lists all stored poems
    """

    poems = await listPoems()
    return {'status': 'ok', 'code': 200, 'poems': poems}

@app.post("/api/v1/push", status_code=201)
async def push(poem: Poem, response: Response):
    """
    Inserts a poem into server
    """

    try:
        await insertPoem(poem)
        return {'status': 'ok', 'code': 201}
    except IntegrityError:
        response.status_code = status.HTTP_409_CONFLICT
        return {'status': "fail", 'code': 409, 'error': 'ALREADY_EXISTS'}
    
    
    