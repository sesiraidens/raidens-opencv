import cv2
import numpy as np

def gaussian_blur(frame, kernel_size=5):
    return cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)

def median_blur(frame, kernel_size=5):
    return cv2.medianBlur(frame, kernel_size)

def bilateral_filter(frame, d=9, sigma_color=75, sigma_space=75):
    return cv2.bilateralFilter(frame, d, sigma_color, sigma_space)

def clahe(frame, clip_limit=2.0, grid_size=8):
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(grid_size, grid_size))
    l = clahe.apply(l)
    lab = cv2.merge([l, a, b])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)