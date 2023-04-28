from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse


router = APIRouter()

@router.get('/artist', tags=['Artists'])
def get_artist():
    artist = 'Dua Lipa'
    msg = f'The artist is {artist}'

    return JSONResponse(content={"message": msg}, status_code=200)