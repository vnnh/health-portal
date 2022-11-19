import pytesseract
import cv2
import os

pytesseract.pytesseract.tesseract_cmd = os.path.expanduser(
    r"~\AppData\Local\Tesseract-OCR\tesseract.exe")


def preprocess_image(image_path):
    grey_scale = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)
    # resized_image = cv2.resize(
    #    grey_scale, None, fx=1.25, fy=1.25, interpolation=cv2.INTER_LINEAR)
    # return cv2.adaptiveThreshold(resized_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 63, 13)
    return grey_scale


def parse(image_path):
    processed_image = preprocess_image(image_path)
    return pytesseract.image_to_string(processed_image, lang="eng").strip()
