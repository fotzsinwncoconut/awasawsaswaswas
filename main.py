#!/usr/bin/env python3
"""
Music Recommendation Engine - Sin necesidad de Spotify Premium
Usa Last.fm + MusicBrainz (APIs 100% gratuitas)
"""

import typer
from rich.console import Console
from pathlib import Path
import os
from dotenv import load_dotenv

app = typer.Typer()
console = Console()

load_dotenv()

@app.command()
def init():
    """Initialize database"""
    from src.database import Database
    db = Database()
    db.init_tables()
    console.print("[green]✓[/green] Database initialized")

@app.command()
def add(
    track_name: str,
    artist_name: str,
    rating: int = typer.Option(5, min=1, max=10)
):
    """Add track to your library"""
    from src.database import Database
    from src.lastfm_client import LastFMClient
    
    client = LastFMClient()
    track_data = client.search_track(track_name, artist_name)
    
    if track_data:
        db = Database()
        db.add_track(track_data, rating)
        console.print(f"[green]✓[/green] Added: {track_name} - {artist_name}")
    else:
        console.print(f"[red]✗[/red] Track not found")

@app.command()
def recommend(count: int = typer.Option(10)):
    """Generate recommendations based on your library"""
    from src.recommender import RecommendationEngine
    
    engine = RecommendationEngine()
    recommendations = engine.generate(count)
    
    if not recommendations:
        console.print("[yellow]No recommendations yet. Add more tracks first.[/yellow]")
        return
    
    console.print("\n[bold cyan]Recommended Tracks:[/bold cyan]")
    for i, rec in enumerate(recommendations, 1):
        console.print(f"{i}. {rec['track']} - {rec['artist']} (match: {rec['score']:.0f}%)")

@app.command()
def library():
    """Show your music library"""
    from src.database import Database
    
    db = Database()
    tracks = db.get_all_tracks()
    
    if not tracks:
        console.print("[yellow]Library is empty. Add tracks first.[/yellow]")
        return
    
    console.print("\n[bold cyan]Your Library:[/bold cyan]")
    for track in tracks:
        console.print(f"• {track['track']} - {track['artist']} (★ {track['rating']}/10)")
    console.print(f"\nTotal: {len(tracks)} tracks")

@app.command()
def status():
    """Check system status"""
    checks = []
    
    # Python
    import sys
    checks.append((f"Python {sys.version.split()[0]}", True))
    
    # Dependencies
    try:
        import requests
        checks.append(("requests", True))
    except:
        checks.append(("requests", False))
    
    try:
        import sklearn
        checks.append(("scikit-learn", True))
    except:
        checks.append(("scikit-learn", False))
    
    # API keys
    lastfm_key = os.getenv("LASTFM_API_KEY")
    checks.append(("Last.fm API configured", bool(lastfm_key)))
    
    # Database
    db_exists = Path(os.getenv("DB_PATH", "music_library.db")).exists()
    checks.append(("Database initialized", db_exists))
    
    console.print("\n[bold cyan]System Status:[/bold cyan]")
    for check, status in checks:
        symbol = "[green]✓[/green]" if status else "[red]✗[/red]"
        console.print(f"{symbol} {check}")
    
    print()

if __name__ == "__main__":
    app()