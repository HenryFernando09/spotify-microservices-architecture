from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class SongIn(BaseModel):
    song_id: int
    position: Optional[int] = 0


class SongOut(SongIn):
    id: int

    class Config:
        from_attributes = True


class PlaylistCreate(BaseModel):
    name: str
    owner_id: int


class PlaylistUpdate(BaseModel):
    name: str


class PlaylistOut(BaseModel):
    id: int
    name: str
    owner_id: int
    created_at: datetime
    songs: List[SongOut] = []

    class Config:
        from_attributes = True
