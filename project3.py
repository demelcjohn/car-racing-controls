import math
import cv2
import pkinput as keyinput 
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
font = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(0)

with mp_hands.Hands(model_complexity=0,min_detection_confidence=0.5,min_tracking_confidence=0.5) as hands:
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
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for point in mp_hands.HandLandmark:
                    if str(point) == "HandLandmark.WRIST":
                        normalizedLandmark = hand_landmarks.landmark[point]
                        pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,normalizedLandmark.y,imageWidth, imageHeight)
                        try:
                            co.append(list(pixelCoordinatesLandmark))
                        except:
                            continue
        
        if len(co) == 2:
            if co[0][0] > co[1][0] and co[0][1]>co[1][1] and co[0][1] - co[1][1] > 50:
                print("Accelerate")
                keyinput.release_key('l')
                keyinput.press_key('r')
                cv2.putText(image, "Accelerate", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                


            elif co[1][0] > co[0][0] and co[1][1]> co[0][1]+100 and co[1][1] - co[0][1] > 50:
                print("Accelerate")
                keyinput.release_key('l')
                keyinput.press_key('r')
                cv2.putText(image, "Accelerate", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                


            elif co[0][0] > co[1][0] and co[1][1]> co[0][1] and co[1][1] - co[0][1] > 50:
                print("Break")
                keyinput.release_key('r')
                keyinput.press_key('l')
                cv2.putText(image, "Break", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                

            elif co[1][0] > co[0][0] and co[0][1]> co[1][1] and co[0][1] - co[1][1] > 50:
                print("Break")
                keyinput.release_key('r')
                keyinput.press_key('l')
                cv2.putText(image, "Break", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                
        



     

        cv2.imshow('Hands',cv2.flip(image, 1))

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
