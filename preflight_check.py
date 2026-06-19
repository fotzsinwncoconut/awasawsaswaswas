#!/usr/bin/env python3
import sys
import subprocess

print("Verificando sistema...")

try:
    import librosa
    import spotipy
    import sklearn
    print("✓ Todas las dependencias OK")
except:
    print("✗ Falta instalar dependencias")
    print("Ejecuta: pip install -r requirements.txt")
    sys.exit(1)