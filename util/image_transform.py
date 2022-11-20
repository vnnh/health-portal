import cv2
import numpy as np
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = os.path.expanduser(
    r"~\AppData\Local\Tesseract-OCR\tesseract.exe")


def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def get_binary(image):
    (thresh, blackAndWhiteImage) = cv2.threshold(
        image, 100, 255, cv2.THRESH_BINARY)
    return blackAndWhiteImage


def detect(cropped_frame, is_number=False, all_characters=False):
    if (is_number):
        text = pytesseract.image_to_string(cropped_frame,
                                           config='-c tessedit_char_whitelist=0123456789 --psm 10')
    else:
        text = pytesseract.image_to_string(
            cropped_frame, config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz --psm 10')

    return text


def draw_text(image, x, y, w, h, text):
    cFrame = np.copy(image)
    cv2.rectangle(cFrame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(cFrame, "text: " + text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                2, (0, 0, 0), 5, cv2.LINE_AA)

    return cFrame


def erode(img, kernel_size=5):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    img_erosion = cv2.dilate(img, kernel, iterations=2)
    return img_erosion
