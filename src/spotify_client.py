import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from typing import Dict, List, Optional

class SpotifyClient:
    def __init__(self):
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            raise ValueError("Falta configurar Spotify API en .env")
        
        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        self.client = spotipy.Spotify(auth_manager=auth_manager)
    
    def search_track(self, track_name: str, artist_name: str) -> Optional[Dict]:
        """Buscar canción en Spotify"""
        try:
            query = f"track:{track_name} artist:{artist_name}"
            results = self.client.search(q=query, type="track", limit=1)
            
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                return {
                    'id': track['id'],
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'duration_ms': track['duration_ms'],
                    'popularity': track['popularity']
                }
        except Exception as e:
            print(f"Error en búsqueda: {e}")
        return None
    
    def get_audio_features(self, spotify_id: str) -> Optional[Dict]:
        """Obtener features de audio"""
        try:
            features = self.client.audio_features(spotify_id)[0]
            return features
        except Exception as e:
            print(f"Error: {e}")
        return None
    
    def get_similar_artists(self, artist_id: str) -> List[Dict]:
        """Obtener artistas similares"""
        try:
            results = self.client.artist_related_artists(artist_id)
            return [
                {'id': a['id'], 'name': a['name']}
                for a in results['artists'][:10]
            ]
        except Exception as e:
            print(f"Error: {e}")
        return []
    
    def get_artist_top_tracks(self, artist_id: str, market: str = "US") -> List[Dict]:
        """Obtener top canciones del artista"""
        try:
            results = self.client.artist_top_tracks(artist_id, market=market)
            return [
                {
                    'id': t['id'],
                    'name': t['name'],
                    'popularity': t['popularity']
                }
                for t in results['tracks'][:5]
            ]
        except Exception as e:
            print(f"Error: {e}")
        return []
    
    def get_artist_id(self, artist_name: str) -> Optional[str]:
        """Obtener ID del artista"""
        try:
            results = self.client.search(q=f"artist:{artist_name}", type="artist", limit=1)
            if results['artists']['items']:
                return results['artists']['items'][0]['id']
        except Exception as e:
            print(f"Error: {e}")
        return None