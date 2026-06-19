import sqlite3
import os
from datetime import datetime
from typing import List, Dict

class Database:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.getenv("DB_PATH", "music_library.db")
        self.conn = None
        self.connect()
    
    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
    
    def init_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY,
                lastfm_id TEXT UNIQUE,
                track_name TEXT NOT NULL,
                artist_name TEXT NOT NULL,
                rating INTEGER DEFAULT 5,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY,
                source_track TEXT,
                recommended_track TEXT,
                recommended_artist TEXT,
                score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
    
    def add_track(self, track_data: Dict, rating: int = 5) -> bool:
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO tracks 
                (lastfm_id, track_name, artist_name, rating)
                VALUES (?, ?, ?, ?)
            """, (
                track_data['id'],
                track_data['name'],
                track_data['artist'],
                rating
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding track: {e}")
            return False
    
    def get_all_tracks(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tracks ORDER BY rating DESC, added_at DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_high_rated_tracks(self, min_rating: int = 7) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM tracks WHERE rating >= ? ORDER BY rating DESC",
            (min_rating,)
        )
        return [dict(row) for row in cursor.fetchall()]
    
    def cache_recommendation(self, source: str, track: str, artist: str, score: float):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO recommendations 
                (source_track, recommended_track, recommended_artist, score)
                VALUES (?, ?, ?, ?)
            """, (source, track, artist, score))
            self.conn.commit()
        except:
            pass
    
    def close(self):
        if self.conn:
            self.conn.close()