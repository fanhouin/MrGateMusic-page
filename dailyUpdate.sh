#!/bin/bash
cd /your/path 
python3 updateSheet.py
cd playlist
git add .
git commit -m "Daily Update - $(date +'%Y-%m-%d')" 
git push