# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import imutils
import cv2
import time

 
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=200)
vs = VideoStream(src=0).start()

time.sleep(2.0)

# keep looping
while True:
    # grab the current frame
    frame=vs.read()
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    # resize the frame, blur it, and convert it to the HSV
    # color space
    if frame is None:
    	break

    frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
 
    # only proceed if at least one contour was found
    if len(cnts)>0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > 5:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                #cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                # update the points queue
    pts.appendleft(center)

    for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                    continue
 
            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(20 / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
            # show the frame to our screen
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
     		print("someething")
            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                    break
 
# cleanup the camera and close any open windows
vs.release()
cv2.destroyAllWindows()
