#!/usr/bin/python

import os
import time
import sys
 
start = 0
end = 8640
 
print "Starting timelapse script..."
while start < end:    
    if start % 180 == 0:
    	print "Another 30 mins elapsed... %d of %d." % (start, end) 
    os.system("fswebcam -i 0 -d /dev/video0 -r 640x480 -p YUYV -q --title @Rasp_Sap  /home/pi/projects/timelapse/%d%m%y_%H%M%S.jpg")
    start = start+1
    time.sleep(10)
 
print "Process of Timelapsed finnished!!"
sys.exit()
