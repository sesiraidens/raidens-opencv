import cv2
import numpy as np

def detect_color(frame, lower_bound, upper_bound, color_space='HSV'):
    if color_space == 'HSV':
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array(lower_bound), np.array(upper_bound))
    elif color_space == 'LAB':
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        mask = cv2.inRange(lab, np.array(lower_bound), np.array(upper_bound))
    
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def get_color_area(contour):
    area = cv2.contourArea(contour)
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    else:
        cx, cy = 0, 0
    return area, (cx, cy)

def filter_by_area(contours, min_area=500, max_area=100000):
    filtered = []
    for c in contours:
        area = cv2.contourArea(c)
        if min_area <= area <= max_area:
            filtered.append(c)
    return filtered