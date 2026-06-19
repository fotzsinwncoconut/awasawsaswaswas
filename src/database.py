import sqlite3
import os
from typing import List, Dict

class Database:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.getenv("DB_PATH", "music_library.db")
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
    
    def init_tables(self):
        """Crear tablas"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY,
                spotify_id TEXT UNIQUE,
                track_name TEXT NOT NULL,
                artist_name TEXT NOT NULL,
                album_name TEXT,
                duration_ms INTEGER,
                popularity INTEGER,
                rating INTEGER DEFAULT 5,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audio_features (
                id INTEGER PRIMARY KEY,
                spotify_id TEXT UNIQUE,
                acousticness REAL,
                danceability REAL,
                energy REAL,
                instrumentalness REAL,
                key INTEGER,
                liveness REAL,
                loudness REAL,
                mode INTEGER,
                speechiness REAL,
                tempo REAL,
                time_signature INTEGER,
                valence REAL,
                FOREIGN KEY (spotify_id) REFERENCES tracks(spotify_id)
            )
        """)
        
        self.conn.commit()
    
    def add_track(self, track_data: Dict, rating: int = 5) -> bool:
        """Agregar canción"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO tracks 
                (spotify_id, track_name, artist_name, album_name, duration_ms, popularity, rating)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                track_data['id'],
                track_data['name'],
                track_data['artist'],
                track_data.get('album', ''),
                track_data.get('duration_ms', 0),
                track_data.get('popularity', 0),
                rating
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def add_audio_features(self, spotify_id: str, features: Dict) -> bool:
        """Guardar features de audio"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO audio_features
                (spotify_id, acousticness, danceability, energy, instrumentalness, key,
                 liveness, loudness, mode, speechiness, tempo, time_signature, valence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                spotify_id,
                features.get('acousticness', 0),
                features.get('danceability', 0),
                features.get('energy', 0),
                features.get('instrumentalness', 0),
                features.get('key', 0),
                features.get('liveness', 0),
                features.get('loudness', 0),
                features.get('mode', 0),
                features.get('speechiness', 0),
                features.get('tempo', 0),
                features.get('time_signature', 0),
                features.get('valence', 0)
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def get_all_tracks(self) -> List[Dict]:
        """Obtener todas las canciones"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tracks ORDER BY rating DESC, added_at DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_high_rated_tracks(self, min_rating: int = 7) -> List[Dict]:
        """Obtener canciones con alta calificación"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tracks WHERE rating >= ? ORDER BY rating DESC", (min_rating,))
        return [dict(row) for row in cursor.fetchall()]