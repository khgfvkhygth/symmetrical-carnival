@echo off
title [≡ƒÜÇ] Launching Godmode Predictor System...
echo --------------------------------------------
echo [*] Setting up environment...
cd /d %~dp0

REM Start OCR capture visual
start "" python ocr_box.py

REM Start live predictor script
start "" python live_predictor.py

REM Start Streamlit UI
start "" streamlit run app.py

exit