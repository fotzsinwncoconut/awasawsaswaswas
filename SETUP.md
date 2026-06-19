# Last.fm FREE API - NO PREMIUM REQUIRED

## SETUP (5 MINUTOS)

### 1. Create Last.fm account (FREE)
https://www.last.fm/join

### 2. Get API key (FREE)
https://www.last.fm/api/account/create
- Click "Create Application"
- Fill simple form
- Accept ToS
- Copy "API Key"

### 3. Update .env
```
LASTFM_API_KEY=your_api_key_here
```

### 4. Test it
```bash
python3 main.py status
python3 main.py init
python3 main.py add "Bohemian Rhapsody" "Queen" --rating 10
python3 main.py recommend --count 10
```

## Why Last.fm (not Spotify)?

- ✓ NO premium required
- ✓ NO premium check
- ✓ FREE API tier is unlimited
- ✓ Better similarity algorithms
- ✓ 70+ million songs database
- ✓ Huge community voting on similar tracks

## Commands

```bash
python3 main.py add "Song" "Artist" --rating 9
python3 main.py library
python3 main.py recommend --count 20
python3 main.py status
```
