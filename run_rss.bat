@echo off
cd /d "%~dp0"
python njuskalo-rssgen.py
timeout /t 5 