from typing import List, Dict
from src.database import Database
from src.lastfm_client import LastFMClient

class RecommendationEngine:
    """Uses Last.fm similarity data for recommendations"""
    
    def __init__(self):
        self.db = Database()
        self.lastfm = LastFMClient()
    
    def generate(self, count: int = 10) -> List[Dict]:
        """Generate recommendations from your high-rated tracks"""
        liked_tracks = self.db.get_high_rated_tracks(min_rating=7)
        
        if not liked_tracks:
            return []
        
        recommendations = {}
        
        # For each liked track, find similar tracks
        for track in liked_tracks:
            similar = self.lastfm.get_similar_tracks(
                track['track_name'],
                track['artist_name']
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
                    recommendations[key]['score'] += rec['match'] * weight
        
        sorted_recs = sorted(
            recommendations.values(),
            key=lambda x: x['score'],
            reverse=True
        )
        
        return sorted_recs[:count]
