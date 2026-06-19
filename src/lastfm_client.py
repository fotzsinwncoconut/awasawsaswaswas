import os
import requests
from typing import Dict, List, Optional

class LastFMClient:
    """Last.fm API - NO PREMIUM NEEDED"""
    
    def __init__(self):
        self.api_key = os.getenv("LASTFM_API_KEY")
        if not self.api_key:
            raise ValueError("LASTFM_API_KEY not in .env")
        self.base_url = "http://ws.audioscrobbler.com/2.0/"
    
    def search_track(self, track_name: str, artist_name: str) -> Optional[Dict]:
        """Search track"""
        try:
            params = {
                'method': 'track.search',
                'track': track_name,
                'artist': artist_name,
                'api_key': self.api_key,
                'format': 'json',
                'limit': 1
            }
            response = requests.get(self.base_url, params=params, timeout=5)
            data = response.json()
            
            if 'results' in data and 'trackmatches' in data['results']:
                matches = data['results']['trackmatches']['track']
                if matches:
                    track = matches[0] if isinstance(matches, list) else matches
                    return {
                        'id': track.get('mbid', ''),
                        'name': track.get('name', ''),
                        'artist': track.get('artist', ''),
                        'url': track.get('url', '')
                    }
        except Exception as e:
            print(f"Error: {e}")
        return None
    
    def get_similar_tracks(self, track_name: str, artist_name: str) -> List[Dict]:
        """Get similar tracks - THIS IS THE KEY"""
        try:
            params = {
                'method': 'track.getSimilar',
                'track': track_name,
                'artist': artist_name,
                'api_key': self.api_key,
                'format': 'json',
                'limit': 20
            }
            response = requests.get(self.base_url, params=params, timeout=5)
            data = response.json()
            
            if 'similartracks' in data:
                tracks = data['similartracks'].get('track', [])
                if tracks and not isinstance(tracks, list):
                    tracks = [tracks]
                
                return [
                    {
                        'name': t.get('name', ''),
                        'artist': t.get('artist', {}).get('name', ''),
                        'match': float(t.get('match', 0)) * 100,
                        'mbid': t.get('mbid', '')
                    }
                    for t in tracks
                ]
        except Exception as e:
            print(f"Error: {e}")
        return []
    
    def get_artist_top_tracks(self, artist_name: str) -> List[Dict]:
        """Get artist's top tracks"""
        try:
            params = {
                'method': 'artist.getTopTracks',
                'artist': artist_name,
                'api_key': self.api_key,
                'format': 'json',
                'limit': 10
            }
            response = requests.get(self.base_url, params=params, timeout=5)
            data = response.json()
            
            if 'toptracks' in data:
                tracks = data['toptracks'].get('track', [])
                if tracks and not isinstance(tracks, list):
                    tracks = [tracks]
                
                return [
                    {
                        'name': t.get('name', ''),
                        'artist': t.get('artist', {}).get('name', ''),
                        'listeners': int(t.get('listeners', 0))
                    }
                    for t in tracks
                ]
        except:
            pass
        return []
