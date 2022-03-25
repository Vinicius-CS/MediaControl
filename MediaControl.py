from win32con import KEYEVENTF_EXTENDEDKEY, VK_MEDIA_PLAY_PAUSE, VK_MEDIA_NEXT_TRACK, VK_MEDIA_PREV_TRACK
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from cvzone.HandTrackingModule import HandDetector
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from math import hypot
import win32api
import ctypes
import numpy
import cv2

# Variables
width, height = 1280, 720
delay = 50
delayCounter = 0

# Camera settings
cam = cv2.VideoCapture(0)
cam.set(0, width)
cam.set(0, height)

# Hand detector
hand = HandDetector(detectionCon=0.9, maxHands=1)

# Audio
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volMin, volMax = volume.GetVolumeRange()[:2]

while True:

    # Get the image from the camera
    success, img = cam.read()
    img = cv2.flip(img, 1)

    # Show text for close the application
    cv2.putText(img, 'Press any key to close', (0, 15), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 60, 245), 1)

    # If the camera device is not found
    if not success:
        # Checks if there is another camera device
        cam = cv2.VideoCapture(1)
        success, frame = cam.read()
        img = cv2.flip(img, 1)

        # If another camera device is not found
        if not success:
            # Show message and close the application
            ctypes.windll.user32.MessageBoxW(0, "Could not find your camera, check your device.", "Camera not found", 0)
            break

    # Find the hand and its landmarks
    hands, img = hand.findHands(img)

    # If the hand is detected
    if hands:
        # List the 21 landmarks
        lmList = hands[0]["lmList"]

        # List which fingers are raised
        fingers = hand.fingersUp(hands[0])

        # If the index, middle and ring fingers are raised
        if fingers == [0, 1, 1, 1, 0]:
            # Get the position of the fingers
            y = int(numpy.interp(lmList[8][1], [20, width], [10, width]))

            # Adjusts volume according to finger position
            vol = numpy.interp(hypot(y), [15, 220], [volMax, volMin])
            volume.SetMasterVolumeLevel(vol, None)

        # If the index and middle fingers are raised
        if fingers == [0, 1, 1, 0, 0]:
            # Get the distance between the index and middle fingers
            length, info, img = hand.findDistance(lmList[8], lmList[12], img)

            # If the distance between the index and middle finger is greater than 70
            if length > 25:
                # Delay pause and play
                delayCounter += 1
                if delayCounter > delay:
                    delayCounter = 0
                    # Pause or play
                    win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY, 0)

        # If the thumb is up
        if fingers == [1, 0, 0, 0, 0]:
            # Delay for next media
            delayCounter += 1
            if delayCounter > delay:
                delayCounter = 0
                # Next media
                win32api.keybd_event(VK_MEDIA_NEXT_TRACK, 0, KEYEVENTF_EXTENDEDKEY, 0)

        # If the little finger is raised
        if fingers == [0, 0, 0, 0, 1]:
            # Delay go back to previous media
            delayCounter += 1
            if delayCounter > delay:
                delayCounter = 0
                # Previous media
                win32api.keybd_event(VK_MEDIA_PREV_TRACK, 0, KEYEVENTF_EXTENDEDKEY, 0)

    # Show camera
    cv2.imshow("Media Control", img)

    # Press anything button to close
    if cv2.waitKey(1) > -1:
        break
