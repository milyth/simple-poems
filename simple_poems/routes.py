from fastapi import Response, status, APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from aiosqlite import IntegrityError
from typing import Annotated

from .world import insertPoem, listPoems
from .schemas import Poem
router = APIRouter()
templates = Jinja2Templates(directory="templates")


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
    

@router.get("/_upload")
async def upload(title: str, author: str, content: str):
    try:
        await insertPoem(Poem(title=title, author=author, content=content))
    except IntegrityError:
       pass
    return RedirectResponse(url="/")
    
    

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", context={'request': request, 'poems]': await listPoems()})

@router.get("/upload")
async def upload(request: Request):
    return templates.TemplateResponse("upload.html", context={'request': request})