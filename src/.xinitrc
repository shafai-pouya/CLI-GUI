#!/bin/python
import os
import time

# begin applications like taskbar and titlebar
# os.system("python ~/CLI-GUI/taskbar.py &")

# time.sleep(1)
os.system('xrdb -merge ~/.Xresources')


os.system("uxterm")

time.sleep(1)

os.system("python ~/CLI-GUI/WM.py &")

time.sleep(1)

# os.system("python ~/CLI-GUI/taskbar.py &")

os.system("xsetroot -cursor_name X_cursor")   # begin cursor


os.system("exec uxterm")

# take a lopp
while True:
	pass

