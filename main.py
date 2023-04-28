import uvicorn
from fastapi import FastAPI
import playlist_router, artists_router

app = FastAPI(title='Wheres my song?',
              description='Locate which of my playlists a song is in',
              version='1.0')

app.include_router(playlist_router.router)
app.include_router(artists_router.router)

if __name__ == '__main__':
    uvicorn.run(app)