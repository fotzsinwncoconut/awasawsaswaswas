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
    """Inicializar database"""
    from src.database import Database
    db = Database()
    db.init_tables()
    console.print("[green]✓[/green] Database inicializada")

@app.command()
def add(
    track_name: str = typer.Argument(...),
    artist_name: str = typer.Argument(...),
    rating: int = typer.Option(5, min=1, max=10)
):
    """Agregar canción a biblioteca"""
    from src.database import Database
    from src.spotify_client import SpotifyClient
    
    console.print("[cyan]Buscando en Spotify...[/cyan]")
    client = SpotifyClient()
    track_data = client.search_track(track_name, artist_name)
    
    if track_data:
        db = Database()
        db.add_track(track_data, rating)
        console.print(f"[green]✓[/green] Agregada: {track_data['name']} - {track_data['artist']}")
    else:
        console.print(f"[red]✗[/red] Canción no encontrada")

@app.command()
def recommend(count: int = typer.Option(10)):
    """Generar recomendaciones"""
    from src.recommender import RecommendationEngine
    
    console.print("[cyan]Generando recomendaciones...[/cyan]")
    engine = RecommendationEngine()
    recommendations = engine.generate(count)
    
    if not recommendations:
        console.print("[yellow]⚠[/yellow] No hay recomendaciones. Agrega más canciones.")
        return
    
    console.print("\n[bold cyan]Recomendaciones:[/bold cyan]")
    for i, rec in enumerate(recommendations, 1):
        console.print(f"{i}. {rec['track']} - {rec['artist']} (score: {rec['score']:.2f})")

@app.command()
def library():
    """Ver biblioteca"""
    from src.database import Database
    
    db = Database()
    tracks = db.get_all_tracks()
    
    if not tracks:
        console.print("[yellow]Tu biblioteca está vacía[/yellow]")
        return
    
    console.print("\n[bold cyan]Tu Biblioteca:[/bold cyan]")
    for track in tracks:
        rating = "★" * track['rating'] + "☆" * (10 - track['rating'])
        console.print(f"• {track['track_name']} - {track['artist_name']} [{rating}]")

@app.command()
def status():
    """Ver estado del sistema"""
    console.print("[bold cyan]Status:[/bold cyan]")
    
    try:
        import librosa
        console.print("[green]✓[/green] librosa OK")
    except:
        console.print("[red]✗[/red] librosa falta")
    
    try:
        import spotipy
        console.print("[green]✓[/green] spotipy OK")
    except:
        console.print("[red]✗[/red] spotipy falta")
    
    if os.getenv("SPOTIFY_CLIENT_ID"):
        console.print("[green]✓[/green] Spotify API configurada")
    else:
        console.print("[red]✗[/red] Spotify API no configurada (.env)")
    
    if Path(os.getenv("DB_PATH", "music_library.db")).exists():
        console.print("[green]✓[/green] Database lista")
    else:
        console.print("[red]✗[/red] Database no inicializada (corre: python main.py init)")

if __name__ == "__main__":
    app()