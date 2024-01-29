#!/bin/bash
export XAUTHORITY=/home/pi/.Xauthority
export DISPLAY=:0 
export XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR

python3 /home/pi/nfr/NCSYS003_SERVER_NODE/app/main.py