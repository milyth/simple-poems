from fastapi import Response, status, APIRouter
from fastapi.templating import Jinja2Templates
from aiosqlite import IntegrityError

from .world import insertPoem, listPoems
from .schemas import Poem
router = APIRouter()

@router.get("/api/v1/list")
async def list():
    """
    Lists all stored poems
    """

    poems = await listPoems()
    return {'status': 'ok', 'code': 200, 'poems': poems}

@router.post("/api/v1/push", status_code=201)
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
    
    
