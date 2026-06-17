from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import engine, get_db, Base

app = FastAPI(title="Playlist Service", version="1.0.0")


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "playlist-service"}


@app.post("/playlists", response_model=schemas.PlaylistOut)
def create_playlist(playlist: schemas.PlaylistCreate, db: Session = Depends(get_db)):
    db_playlist = models.Playlist(name=playlist.name, owner_id=playlist.owner_id)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist


@app.get("/playlists", response_model=List[schemas.PlaylistOut])
def list_playlists(owner_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Playlist)
    if owner_id is not None:
        query = query.filter(models.Playlist.owner_id == owner_id)
    return query.all()


@app.get("/playlists/{playlist_id}", response_model=schemas.PlaylistOut)
def get_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist = db.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist no encontrada")
    return playlist


@app.put("/playlists/{playlist_id}", response_model=schemas.PlaylistOut)
def update_playlist(playlist_id: int, data: schemas.PlaylistUpdate, db: Session = Depends(get_db)):
    playlist = db.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist no encontrada")
    playlist.name = data.name
    db.commit()
    db.refresh(playlist)
    return playlist


@app.delete("/playlists/{playlist_id}")
def delete_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist = db.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist no encontrada")
    db.delete(playlist)
    db.commit()
    return {"detail": "Playlist eliminada"}


@app.post("/playlists/{playlist_id}/songs", response_model=schemas.PlaylistOut)
def add_song(playlist_id: int, song: schemas.SongIn, db: Session = Depends(get_db)):
    playlist = db.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist no encontrada")
    db_song = models.PlaylistSong(playlist_id=playlist_id, song_id=song.song_id, position=song.position)
    db.add(db_song)
    db.commit()
    db.refresh(playlist)
    return playlist


@app.delete("/playlists/{playlist_id}/songs/{song_id}")
def remove_song(playlist_id: int, song_id: int, db: Session = Depends(get_db)):
    db_song = db.query(models.PlaylistSong).filter(
        models.PlaylistSong.playlist_id == playlist_id,
        models.PlaylistSong.song_id == song_id
    ).first()
    if not db_song:
        raise HTTPException(status_code=404, detail="Canción no encontrada en la playlist")
    db.delete(db_song)
    db.commit()
    return {"detail": "Canción eliminada de la playlist"}
