import cv2
import mediapipe as mp
import pyautogui
#import time

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)


screen_w, screen_h = pyautogui.size()


speed_factor = 1.4


initial_x, initial_y = pyautogui.position()
first_detection = False  
#dragging = False

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)

pyautogui.FAILSAFE = False  

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            
            palm_x = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
            palm_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y

            
            palm_x = int(palm_x * screen_w)
            palm_y = int(palm_y * screen_h)

            
            if not first_detection:
                initial_x, initial_y = palm_x, palm_y
                first_detection = True
                continue  

            
            target_x = min(max((palm_x - initial_x) * speed_factor + initial_x, 0), screen_w - 1)
            target_y = min(max((palm_y - initial_y) * speed_factor + initial_y, 0), screen_h - 1)

            
            current_x, current_y = pyautogui.position()
            smooth_x = current_x + (target_x - current_x) * 0.2
            smooth_y = current_y + (target_y - current_y) * 0.2

            
            pyautogui.moveTo(smooth_x, smooth_y, duration=0.01)

            
            print(f"Mouse X: {target_x}, Mouse Y: {target_y}, Screen: {screen_w}x{screen_h}")

            
            fingers = []
            tip_ids = [4, 8, 12, 16, 20]

            for i in range(1, 5):  
                if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y:
                    fingers.append(1)  
                else:
                    fingers.append(0)

            #Left Click
            if fingers == [1, 0, 0, 0]:
                print("Left Click")
                pyautogui.click(interval=0.15)
            #Right Click  
            elif fingers == [1, 1, 0, 0]:
                print("Right Click")
                pyautogui.rightClick(interval=0.15)
            #Scroll Down
            elif fingers == [1, 1, 1, 0]:
                print("Scroll Down")
                pyautogui.scroll(-40)  
            #Scroll Up
            elif fingers == [1, 1, 1, 1]:
                print("Scroll Up")
                pyautogui.scroll(40)
            

    cv2.imshow("Hand Tracking", frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()