#!/bin/bash

# remove lck if exist
rm -f /tmp/.X99-lock

# Run Xvfb in the background
Xvfb :99 -screen 0 1920x1080x24 &

# Set display for playwright
export DISPLAY=:99

# Run scrapper
python main.py
