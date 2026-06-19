import os
import requests
from typing import Dict, List, Optional

class LastFMClient:
    """Last.fm API client - NO PREMIUM NEEDED, completely free"""
    
    def __init__(self):
        self.api_key = os.getenv("LASTFM_API_KEY")
        if not self.api_key:
            raise ValueError("LASTFM_API_KEY not configured in .env")
        self.base_url = "http://ws.audioscrobbler.com/2.0/"
    
    def search_track(self, track_name: str, artist_name: str) -> Optional[Dict]:
        """Search for a track"""
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
            print(f"Search error: {e}")
        return None
    
    def get_similar_tracks(self, track_name: str, artist_name: str) -> List[Dict]:
        """Get similar tracks (core of recommendation engine)"""
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
            print(f"Similar tracks error: {e}")
        return []
    
    def get_artist_info(self, artist_name: str) -> Optional[Dict]:
        """Get artist information"""
        try:
            params = {
                'method': 'artist.getinfo',
                'artist': artist_name,
                'api_key': self.api_key,
                'format': 'json'
            }
            response = requests.get(self.base_url, params=params, timeout=5)
            data = response.json()
            
            if 'artist' in data:
                artist = data['artist']
                return {
                    'name': artist.get('name', ''),
                    'listeners': artist.get('stats', {}).get('listeners', 0),
                    'bio': artist.get('bio', {}).get('summary', ''),
                    'tags': [t.get('name') for t in artist.get('tags', {}).get('tag', [])]
                }
        except Exception as e:
            print(f"Artist info error: {e}")
        return None
    
    def get_top_artists(self) -> List[Dict]:
        """Get chart top artists"""
        try:
            params = {
                'method': 'chart.getTopArtists',
                'api_key': self.api_key,
                'format': 'json',
                'limit': 50
            }
            response = requests.get(self.base_url, params=params, timeout=5)
            data = response.json()
            
            if 'artists' in data:
                return [
                    {'name': a.get('name', ''), 'listeners': a.get('listeners', 0)}
                    for a in data['artists'].get('artist', [])
                ]
        except Exception as e:
            print(f"Top artists error: {e}")
        return []
    
    def get_top_tracks(self) -> List[Dict]:
        """Get chart top tracks"""
        try:
            params = {
                'method': 'chart.getTopTracks',
                'api_key': self.api_key,
                'format': 'json',
                'limit': 50
            }
            response = requests.get(self.base_url, params=params, timeout=5)
            data = response.json()
            
            if 'tracks' in data:
                return [
                    {
                        'name': t.get('name', ''),
                        'artist': t.get('artist', {}).get('name', ''),
                        'listeners': t.get('listeners', 0)
                    }
                    for t in data['tracks'].get('track', [])
                ]
        except Exception as e:
            print(f"Top tracks error: {e}")
        return []
