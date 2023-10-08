import cv2
import mediapipe as mp
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4,8,12,16,20]

def countFingers(image, hand_Landmarks, HandNo=0):
    if hand_landmarks:
        landmarks = hand_Landmarks[handNo].landmark
        #print (landmarks)
        # Contar dedos
        fingers = []

        for lm_index in tipIds:
                # Obtener puntas de los dedos y valor de posición "y" inferior
                finger_tip_y = landmarks[lm_index].y 
                finger_bottom_y = landmarks[lm_index - 2].y
                # Obtener punta del pulgar y valor de posición "y" 
                thumb_tip_x = landmarks[lm_index].x
                thumb_bottom_x = landmarks[lm_index - 2].x

                # Verificar si algún dedo está abierto o cerrado
                if lm_index !=4:
                    if finger_tip_y < finger_bottom_y:
                        fingers.append(1)
                        print("El dedo con id ",lm_index," está abierto.")

                    if finger_tip_y > finger_bottom_y:
                        fingers.append(0)
                        print("El dedo con id ",lm_index," está cerrado.")
                else:
                    if thumb_tip_x > thumb_bottom_x:
                        fingers.append(1)
                        print("El pulgar está abierto.")
                    if thumb_tip_x < thumb_bottom_x:
                        fingers.append(0)
                        print("El pulgar está cerrado.")

        # print(fingers)
        totalFingers = fingers.count(1)

        # Mostrar texto
        text = f'Fingers: {totalFingers}'

        cv2.putText(image, text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

def drawHandsLanmarks(image, hand_Landmarks):
    if hand_landmarks:
        for landmarks in hand_Landmarks:
            mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTTIONS)

while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)

    results = hands.process(image)

    hand_landmarks = results.multi_hand_landmarks

    drawHandsLanmarks(image, hand_landmarks)

    countFingers

    cv2.imshow("Controlador de medios", image)

    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()