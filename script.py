import cv2
import numpy

# a helper function required as OpenCV's createTrackbar() needs a callback function
def hello(x):
    print("")

#setting up the webcam, this opens default webcam, 0 refers to default camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Camera not opened.")
    exit()

#creating Trackbars
cv2.namedWindow("bars")
cv2.createTrackbar("lower_hue", "bars", 0, 180, hello)
cv2.createTrackbar("lower_saturation", "bars", 0, 255, hello)
cv2.createTrackbar("lower_value", "bars", 0, 255, hello)
cv2.createTrackbar("upper_hue", "bars", 180, 180, hello)
cv2.createTrackbar("upper_saturation", "bars", 255, 255, hello)
cv2.createTrackbar("upper_value", "bars", 50, 255, hello)

#capturing the initial frame
while(True):
    cv2.waitKey(1000)
    ret, init_frame = cap.read()
#flag is a flag which indicates if frame was captured successfully
    if(ret):
        break

#processing each frame
while(True):
    ret, frame =  cap.read()
    #converts frame to hsv
    inspect = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #get hsv values from trackbars
    upper_hue = cv2.getTrackbarPos("upper_hue", "bars")
    upper_saturation = cv2.getTrackbarPos("upper_saturation", "bars")
    upper_value = cv2.getTrackbarPos("upper_value", "bars")
    lower_hue = cv2.getTrackbarPos("lower_hue", "bars")
    lower_saturation = cv2.getTrackbarPos("lower_saturation", "bars")
    lower_value = cv2.getTrackbarPos("lower_value", "bars")

    #create a mask
    upper_hsv = numpy.array([upper_hue, upper_saturation, upper_value])
    lower_hsv = numpy.array([lower_hue, lower_saturation, lower_value])
    mask = cv2.inRange(inspect, lower_hsv, upper_hsv)
    kernel = numpy.ones((3,3), numpy.uint8)

    mask = cv2.medianBlur(mask, 3)
    mask = cv2.dilate(mask, kernel, 8)
    mask_inv = 255-mask

    #get the non cloak area
    b, g, r = frame[:,:,0], frame[:,:,1], frame[:,:,2]
    b = cv2.bitwise_and(mask_inv, b)
    g = cv2.bitwise_and(mask_inv, g)
    r = cv2.bitwise_and(mask_inv, r)
    frame_inv = cv2.merge((b, g, r))

    #get the cloak area
    b, g, r = init_frame[:,:,0], init_frame[:,:,1], init_frame[:,:,2]
    b = cv2.bitwise_and(mask, b)
    g = cv2.bitwise_and(mask, g)
    r = cv2.bitwise_and(mask, r)
    init_frame_inv = cv2.merge((b,g,r))

    #merge cloak and non cloak area and display
    total = cv2.bitwise_or(frame_inv, init_frame_inv)
    cv2.imshow("Harry's Cloak", total)
    #end program when user clicks on q
    if(cv2.waitKey(3)==ord('q')):
        break

cv2.destroyAllWindows()
cap.release()

    