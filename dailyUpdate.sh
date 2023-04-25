#!/bin/bash
cd /your/path 
python3 dailyUpdate.py
cd playlist
git add .
git commit -m "Daily Update - $(date +'%Y-%m-%d')" 
git push