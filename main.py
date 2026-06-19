#!/usr/bin/env python3
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
    """Add track to library"""
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
    """Generate recommendations"""
    from src.recommender import RecommendationEngine
    
    engine = RecommendationEngine()
    recommendations = engine.generate(count)
    
    if not recommendations:
        console.print("[yellow]No recommendations. Add tracks with rating >= 7[/yellow]")
        return
    
    console.print("\n[bold cyan]Recommendations:[/bold cyan]")
    for i, rec in enumerate(recommendations, 1):
        console.print(f"{i}. {rec['track']} - {rec['artist']} ({rec['score']:.0f}%)")

@app.command()
def library():
    """Show library"""
    from src.database import Database
    
    db = Database()
    tracks = db.get_all_tracks()
    
    if not tracks:
        console.print("[yellow]Empty. Add tracks first.[/yellow]")
        return
    
    console.print("\n[bold cyan]Your Library:[/bold cyan]")
    for track in tracks:
        console.print(f"• {track['track_name']} - {track['artist_name']} (★{track['rating']}/10)")
    console.print(f"\nTotal: {len(tracks)}")

@app.command()
def status():
    """Check status"""
    checks = []
    
    import sys
    checks.append((f"Python {sys.version.split()[0]}", True))
    
    try:
        import requests
        checks.append(("requests", True))
    except:
        checks.append(("requests", False))
    
    lastfm_key = os.getenv("LASTFM_API_KEY")
    checks.append(("LASTFM_API_KEY", bool(lastfm_key)))
    
    db_exists = Path(os.getenv("DB_PATH", "music_library.db")).exists()
    checks.append(("Database", db_exists))
    
    console.print("\n[bold cyan]Status:[/bold cyan]")
    for check, status in checks:
        symbol = "[green]✓[/green]" if status else "[red]✗[/red]"
        console.print(f"{symbol} {check}")
    print()

if __name__ == "__main__":
    app()