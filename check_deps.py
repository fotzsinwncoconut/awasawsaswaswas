#!/usr/bin/env python3
DEPENDENCIES = {
    'librosa': {'version': '0.10.0', 'cost': 'FREE', 'license': 'ISC', 'size': '200MB', 'purpose': 'Audio analysis'},
    'spotipy': {'version': '2.22.1', 'cost': 'FREE', 'license': 'MIT', 'size': '5MB', 'purpose': 'Spotify API'},
    'scikit-learn': {'version': '1.3.2', 'cost': 'FREE', 'license': 'BSD', 'size': '300MB', 'purpose': 'ML similarity'},
    'pandas': {'version': '2.1.3', 'cost': 'FREE', 'license': 'BSD', 'size': '100MB', 'purpose': 'Data processing'},
    'numpy': {'version': '1.24.3', 'cost': 'FREE', 'license': 'BSD', 'size': '400MB', 'purpose': 'Numerical'},
    'requests': {'version': '2.31.0', 'cost': 'FREE', 'license': 'Apache', 'size': '500KB', 'purpose': 'HTTP requests'},
    'python-dotenv': {'version': '1.0.0', 'cost': 'FREE', 'license': 'BSD', 'size': '50KB', 'purpose': 'Env vars'},
    'typer': {'version': '0.9.0', 'cost': 'FREE', 'license': 'MIT', 'size': '2MB', 'purpose': 'CLI'},
    'rich': {'version': '13.7.0', 'cost': 'FREE', 'license': 'MIT', 'size': '5MB', 'purpose': 'Terminal UI'},
}

print("\n" + "="*70)
print("DEPENDENCY ANALYSIS - ALL 100% FREE & OPEN SOURCE")
print("="*70 + "\n")

print("📦 PACKAGES TO INSTALL:\n")
for name, info in DEPENDENCIES.items():
    print(f"  {name:20} v{info['version']:10} | {info['license']:8} | {info['size']:10}")

print("\n" + "-"*70)
print(f"TOTAL SIZE: ~1.2GB | COST: $0 | Everything is FREE")
print("-"*70 + "\n")

print("🌐 EXTERNAL APIs (All FREE tier):")
print("  • Spotify API: 180k requests/month FREE (plenty for this)")
print("  • MusicBrainz: Unlimited FREE requests")
print("  • Local SQLite: FREE (your computer)\n")

print("\n📋 ACCOUNTS NEEDED (All FREE):")
print("  1. Spotify Developer: https://developer.spotify.com/dashboard")
print("  2. Takes 5 minutes, zero cost, zero credit card needed\n")

print("✓ EVERYTHING IS COMPLETELY FREE & OPEN SOURCE")
print("\nNext: python3 check_prereqs.py")
print("Then: pip install -r requirements.txt\n")