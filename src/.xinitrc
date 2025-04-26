#!/bin/bash

xrdb -merge /opt/CLI-GUI/cfg/.Xresources

python /opt/CLI-GUI/__main__.py

exec uxterm
