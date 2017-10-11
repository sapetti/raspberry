#!/usr/bin/env python

import os
import sys
import time

print "Start execution"
os.system("fswebcam -i 0 -d /dev/video0 -r 640x480 -q --title @Raspberry_Sap /home/pi/projects/take_picture/photos/%d%m%y_%H%M%S.jpg")
print "Photo taked"
sys.exit()
