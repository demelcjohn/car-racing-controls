import math
import pkinput2 as keyinput
import cv2
import mediapipe as mp
from time import sleep
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    imageHeight, imageWidth, _ = image.shape

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    co=[]
    mt=[]
    mp=[]
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        for point in mp_hands.HandLandmark:
           if str(point) == "HandLandmark.WRIST" :
              normalizedLandmark = hand_landmarks.landmark[point]
              pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,
                                                                                        normalizedLandmark.y,
                                                                                    imageWidth, imageHeight)

              try:
                co.append(list(pixelCoordinatesLandmark))
              except:
                  continue

           if str(point) == "HandLandmark.MIDDLE_FINGER_TIP" :
              normalizedLandmark = hand_landmarks.landmark[point]
              pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,
                                                                                        normalizedLandmark.y,
                                                                                    imageWidth, imageHeight)

              try:
                mt.append(list(pixelCoordinatesLandmark))
              except:
                  continue

           if str(point) == "HandLandmark.MIDDLE_FINGER_PIP" :
              normalizedLandmark = hand_landmarks.landmark[point]
              pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,
                                                                                        normalizedLandmark.y,
                                                                                    imageWidth, imageHeight)

              try:
                mp.append(list(pixelCoordinatesLandmark))
              except:
                  continue

    try:
        if len(co) == 2:

            if co[0][0] > co[1][0] and (mt[0][1]>mp[0][1]) and (mt[1][1]<mp[1][1]):
                print("Turn left.")
                keyinput.release_key('s')
                keyinput.release_key('d')
                keyinput.press_key('a')
                keyinput.press_key('w')
                sleep(.1)
                cv2.putText(image, "Turn left", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)


            elif co[1][0] > co[0][0] and (mt[1][1]>mp[1][1]) and (mt[0][1]<mp[0][1]):
                print("Turn left.")
                keyinput.release_key('s')
                keyinput.release_key('d')
                keyinput.press_key('a')
                keyinput.press_key('w')
                sleep(.1)
                cv2.putText(image, "Turn left", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)


            elif co[0][0] > co[1][0] and (mt[0][1]<mp[0][1]) and (mt[1][1]>mp[1][1]):
                print("Turn right.")
                keyinput.release_key('s')
                keyinput.release_key('a')
                keyinput.press_key('d')
                keyinput.press_key('w')
                sleep(.1)
                cv2.putText(image, "Turn right", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

            elif co[1][0] > co[0][0] and (mt[1][1]<mp[1][1]) and (mt[0][1]>mp[0][1]):
                print("Turn right.")
                keyinput.release_key('s')
                keyinput.release_key('a')
                keyinput.press_key('d')
                keyinput.press_key('w')
                sleep(.1)
                cv2.putText(image, "Turn right", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
            
            else:
                print("keeping straight")
                keyinput.release_key('s')
                keyinput.release_key('a')
                keyinput.release_key('d')
                keyinput.press_key('w')
                cv2.putText(image, "keep straight", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

                if(mt[0][1]>mp[0][1]):
                    keyinput.press_key('b')
                else:
                    keyinput.release_key('b')
        

        if len(co)==1:
            print("keeping back")
            keyinput.release_key('a')
            keyinput.release_key('d')
            keyinput.release_key('w')
            keyinput.press_key('s')
            cv2.putText(image, "keeping back", (50, 50), font, 1.0, (0, 255, 0), 2, cv2.LINE_AA)

        if(len(co)==0):
            keyinput.release_key('a')
            keyinput.release_key('d')
            keyinput.release_key('w')
            keyinput.release_key('s')


    except:
        continue




    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))


    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
cap.release()