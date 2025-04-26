#!/bin/bash

xrdb -merge ~/.Xresources

python /opt/CLI-GUI/__main__.py

exec uxterm
