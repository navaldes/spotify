from pydantic import BaseModel

class links(BaseModel):
    user_link: str
    song_link: str
    class Config:
        schema_extra = {
            'example': {
                'user_link': 'Your profile link',
                'song_link': 'The song to search for in your playlists'
                }
        }