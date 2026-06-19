from typing import List, Dict
from src.database import Database
from src.lastfm_client import LastFMClient

class RecommendationEngine:
    """Recommendation engine using Last.fm similarity data"""
    
    def __init__(self):
        self.db = Database()
        self.lastfm = LastFMClient()
    
    def generate(self, count: int = 10) -> List[Dict]:
        """Generate recommendations from library"""
        # Get high-rated tracks
        liked_tracks = self.db.get_high_rated_tracks(min_rating=7)
        
        if not liked_tracks:
            return []
        
        recommendations = {}
        
        # For each liked track, find similar tracks
        for track in liked_tracks:
            similar = self.lastfm.get_similar_tracks(
                track['track'],
                track['artist']
            )
            
            # Weight by user rating
            weight = track['rating'] / 10.0
            
            for rec in similar:
                key = f"{rec['name']}|{rec['artist']}"
                if key not in recommendations:
                    recommendations[key] = {
                        'track': rec['name'],
                        'artist': rec['artist'],
                        'score': rec['match'] * weight
                    }
                else:
                    # Accumulate score if appears multiple times
                    recommendations[key]['score'] += rec['match'] * weight
        
        # Sort and return top N
        sorted_recs = sorted(
            recommendations.values(),
            key=lambda x: x['score'],
            reverse=True
        )
        
        return sorted_recs[:count]
    
    def discover_new(self, count: int = 10) -> List[Dict]:
        """Discover new music from trending + similar artists"""
        recommendations = {}
        
        # Get liked tracks and their artists
        liked_tracks = self.db.get_high_rated_tracks(min_rating=7)
        
        if not liked_tracks:
            # If no library, return trending
            trending = self.lastfm.get_top_tracks()
            return [
                {'track': t['name'], 'artist': t['artist'], 'score': 80}
                for t in trending[:count]
            ]
        
        # For each liked artist, find similar tracks
        for track in liked_tracks[:5]:  # Top 5 liked tracks
            similar = self.lastfm.get_similar_tracks(
                track['track'],
                track['artist']
            )
            
            for rec in similar:
                key = f"{rec['name']}|{rec['artist']}"
                if key not in recommendations:
                    recommendations[key] = {
                        'track': rec['name'],
                        'artist': rec['artist'],
                        'score': rec['match']
                    }
        
        sorted_recs = sorted(
            recommendations.values(),
            key=lambda x: x['score'],
            reverse=True
        )
        
        return sorted_recs[:count]
