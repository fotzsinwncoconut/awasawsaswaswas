#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
python3 -c "import librosa, spotipy, sklearn; print('OK')"
if [ ! -f ".env" ]; then
    cp .env.example .env
fi
echo "Setup completado!"