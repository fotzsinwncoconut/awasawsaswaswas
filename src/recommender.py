import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
from src.database import Database
from src.spotify_client import SpotifyClient
import os

class RecommendationEngine:
    def __init__(self):
        self.db = Database()
        self.spotify = SpotifyClient()
        self.min_similarity = float(os.getenv("MIN_SIMILARITY_SCORE", 0.6))
    
    def generate(self, count: int = 10) -> List[Dict]:
        """Generar recomendaciones"""
        liked_tracks = self.db.get_high_rated_tracks(min_rating=7)
        
        if not liked_tracks:
            return []
        
        liked_features = self._extract_features(liked_tracks)
        if liked_features is None or len(liked_features) == 0:
            return []
        
        avg_features = np.mean(liked_features, axis=0)
        similar_tracks = self._find_similar_from_artists(liked_tracks)
        
        if not similar_tracks:
            return []
        
        candidate_features = self._extract_features(similar_tracks)
        if candidate_features is None or len(candidate_features) == 0:
            return []
        
        similarities = cosine_similarity([avg_features], candidate_features)[0]
        
        recommendations = []
        for track, score in zip(similar_tracks, similarities):
            if score >= self.min_similarity:
                recommendations.append({
                    'track': track['name'],
                    'artist': track['artist'],
                    'score': float(score),
                    'spotify_id': track['spotify_id']
                })
        
        recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)
        return recommendations[:count]
    
    def _extract_features(self, tracks: List[Dict]) -> np.ndarray:
        """Extraer features de audio"""
        features_list = []
        
        for track in tracks:
            try:
                features = self.db.conn.cursor().execute(
                    "SELECT * FROM audio_features WHERE spotify_id = ?",
                    (track['spotify_id'],)
                ).fetchone()
                
                if features:
                    feature_vector = [
                        features[2], features[3], features[4], features[5],
                        features[7], features[9], features[10], features[12]
                    ]
                    features_list.append(feature_vector)
                else:
                    spotify_features = self.spotify.get_audio_features(track['spotify_id'])
                    if spotify_features:
                        self.db.add_audio_features(track['spotify_id'], spotify_features)
                        feature_vector = [
                            spotify_features.get('acousticness', 0),
                            spotify_features.get('danceability', 0),
                            spotify_features.get('energy', 0),
                            spotify_features.get('instrumentalness', 0),
                            spotify_features.get('loudness', 0),
                            spotify_features.get('speechiness', 0),
                            spotify_features.get('tempo', 0),
                            spotify_features.get('valence', 0)
                        ]
                        features_list.append(feature_vector)
            except Exception as e:
                print(f"Error: {e}")
                continue
        
        return np.array(features_list) if features_list else None
    
    def _find_similar_from_artists(self, liked_tracks: List[Dict]) -> List[Dict]:
        """Encontrar artistas similares"""
        similar_tracks = []
        seen_ids = {t['spotify_id'] for t in liked_tracks}
        
        for track in liked_tracks[:5]:
            try:
                artist_id = self.spotify.get_artist_id(track['artist_name'])
                if not artist_id:
                    continue
                
                similar_artists = self.spotify.get_similar_artists(artist_id)
                
                for artist in similar_artists[:3]:
                    top_tracks = self.spotify.get_artist_top_tracks(artist['id'])
                    for t in top_tracks:
                        if t['id'] not in seen_ids:
                            similar_tracks.append({
                                'spotify_id': t['id'],
                                'name': t['name'],
                                'artist': artist['name']
                            })
                            seen_ids.add(t['id'])
            except Exception as e:
                print(f"Error: {e}")
                continue
        
        return similar_tracks