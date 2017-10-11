#!/usr/bin/env python
import shutil
import os.path#, subprocess
FILE_PATH_USB = r'/home/pi/usbdrv'
SYS_PATH = r'/home/pi/projects/move/capt0000.jpg'
shutil.copy(SYS_PATH, FILE_PATH_USB)
os.remove(SYS_PATH)

