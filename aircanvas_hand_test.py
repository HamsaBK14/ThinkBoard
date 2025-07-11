import cv2
import numpy as np
import mediapipe as mp
import time
import os
from datetime import datetime
import random

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

colors = [(255, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
color_names = ['Purple', 'Blue', 'Green', 'Red']
brush_thickness = 10
eraser_thickness = 50
draw_color = colors[0]
xp, yp = 0, 0

undo_stack = []
eraser_mode = False
brush_type = "Pencil"

suggestion_text = ""
suggestion_timer = 0
suggested_corner = None
pick_color_mode = False

highlight_color = (0, 255, 0)
highlight_thickness = 4


def fingers_up(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    for i in range(1, 5):
        if hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[tips[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers


def save_drawing(canvas):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"drawing_{now}.png"
    cv2.imwrite(filename, canvas)
    print(f"Saved: {filename}")


def draw_spray(canvas, x, y, color):
    for _ in range(30):
        offset_x = random.randint(-15, 15)
        offset_y = random.randint(-15, 15)
        radius = random.randint(1, 2)
        cv2.circle(canvas, (x + offset_x, y + offset_y), radius, color, -1)


def analyze_canvas(filename):
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return "Error loading canvas", None

    h, w = img.shape
    corners = {
        'Top Left': img[0:h // 2, 0:w // 2],
        'Top Right': img[0:h // 2, w // 2:],
        'Bottom Left': img[h // 2:, 0:w // 2],
        'Bottom Right': img[h // 2:, w // 2:]
    }

    empty_scores = {}
    for name, section in corners.items():
        white_pixels = cv2.countNonZero(section)
        empty_scores[name] = white_pixels

    suggestion = min(empty_scores, key=empty_scores.get)
    return f"Try adding more in {suggestion} 🖌️", suggestion


def draw_highlight(img, corner):
    h, w = img.shape[:2]
    half_h, half_w = h // 2, w // 2

    if corner == 'Top Left':
        cv2.rectangle(img, (0, 0), (half_w, half_h), highlight_color, highlight_thickness)
    elif corner == 'Top Right':
        cv2.rectangle(img, (half_w, 0), (w, half_h), highlight_color, highlight_thickness)
    elif corner == 'Bottom Left':
        cv2.rectangle(img, (0, half_h), (half_w, h), highlight_color, highlight_thickness)
    elif corner == 'Bottom Right':
        cv2.rectangle(img, (half_w, half_h), (w, h), highlight_color, highlight_thickness)


while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    for i, color in enumerate(colors):
        cv2.rectangle(img, (i * 80 + 30, 5), (i * 80 + 90, 55), color, -1)
        cv2.putText(img, color_names[i], (i * 80 + 35, 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    brush_buttons = ["Pencil", "Marker", "Glow", "Spray"]
    for i, name in enumerate(brush_buttons):
        x1 = 900 + i * 80
        cv2.rectangle(img, (x1, 5), (x1 + 70, 55), (200, 200, 200), -1)
        cv2.putText(img, name, (x1 + 5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 1)

    cv2.rectangle(img, (370, 5), (440, 55), (0, 0, 0), -1)
    cv2.putText(img, "E", (390, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.rectangle(img, (450, 5), (520, 55), (255, 255, 255), -1)
    cv2.putText(img, "U", (470, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    cv2.rectangle(img, (530, 5), (600, 55), (0, 255, 255), -1)
    cv2.putText(img, "C", (550, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    cv2.rectangle(img, (610, 5), (680, 55), (0, 255, 0), -1)
    cv2.putText(img, "S", (630, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    cv2.rectangle(img, (690, 5), (760, 55), (200, 255, 200), -1)
    cv2.putText(img, "Sug", (700, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 100, 0), 2)

    cv2.rectangle(img, (770, 5), (840, 55), (180, 180, 255), -1)
    cv2.putText(img, "Pick", (780, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 100), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = hand_landmarks.landmark
            h, w, _ = img.shape
            cx, cy = int(lm_list[8].x * w), int(lm_list[8].y * h)

            fingers = fingers_up(hand_landmarks)

            if fingers[1] and fingers[2]:
                xp, yp = 0, 0
                if 5 < cy < 55:
                    if 30 < cx < 90:
                        draw_color = colors[0]; eraser_mode = False; pick_color_mode = False
                    elif 110 < cx < 170:
                        draw_color = colors[1]; eraser_mode = False; pick_color_mode = False
                    elif 190 < cx < 250:
                        draw_color = colors[2]; eraser_mode = False; pick_color_mode = False
                    elif 270 < cx < 330:
                        draw_color = colors[3]; eraser_mode = False; pick_color_mode = False
                    elif 370 < cx < 440:
                        eraser_mode = True
                    elif 450 < cx < 520:
                        if undo_stack:
                            canvas = undo_stack.pop()
                    elif 530 < cx < 600:
                        canvas = np.zeros((720, 1280, 3), dtype=np.uint8); undo_stack.clear()
                    elif 610 < cx < 680:
                        save_drawing(canvas)
                    elif 690 < cx < 760:
                        now = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"suggestion_canvas_{now}.png"
                        cv2.imwrite(filename, canvas)
                        suggestion_text, suggested_corner = analyze_canvas(filename)
                        suggestion_timer = time.time()
                    elif 770 < cx < 840:
                        pick_color_mode = True

                    for i, name in enumerate(brush_buttons):
                        bx = 900 + i * 80
                        if bx < cx < bx + 70:
                            brush_type = name

            elif fingers[1] and not fingers[2]:
                if xp == 0 and yp == 0:
                    xp, yp = cx, cy

                if pick_color_mode:
                    draw_color = img[cy, cx].tolist()
                    pick_color_mode = False

                else:
                    color = (0, 0, 0) if eraser_mode else draw_color
                    thickness = eraser_thickness if eraser_mode else brush_thickness

                    if not eraser_mode:
                        undo_stack.append(canvas.copy())

                    if eraser_mode:
                        cv2.line(canvas, (xp, yp), (cx, cy), color, thickness)
                    elif brush_type == "Pencil":
                        cv2.line(canvas, (xp, yp), (cx, cy), color, 2)
                    elif brush_type == "Marker":
                        cv2.line(canvas, (xp, yp), (cx, cy), color, 10)
                    elif brush_type == "Glow":
                        overlay = canvas.copy()
                        cv2.line(overlay, (xp, yp), (cx, cy), color, 25)
                        canvas = cv2.addWeighted(overlay, 0.4, canvas, 0.6, 0)
                    elif brush_type == "Spray":
                        draw_spray(canvas, cx, cy, color)

                xp, yp = cx, cy

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, img_inv)
    img = cv2.bitwise_or(img, canvas)

    if suggested_corner and time.time() - suggestion_timer < 3:
        draw_highlight(img, suggested_corner)

    cv2.putText(img, f"Brush: {brush_type}", (10, 700),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    if suggestion_text and time.time() - suggestion_timer < 5:
        cv2.rectangle(img, (20, 620), (1260, 680), (50, 50, 50), -1)
        cv2.putText(img, suggestion_text, (40, 660),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

    cv2.imshow("ThinkBoard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
