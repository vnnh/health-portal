import cv2
import util.image_transform as image_transform
import numpy as np


def is_vertical(line):
    return line[0] == line[2]


def is_horizontal(line):
    return line[1] == line[3]


def overlapping_filter(lines, sorting_index):
    filtered_lines = []
    lines = sorted(lines, key=lambda lines: lines[sorting_index])

    for i in range(len(lines)):
        l_curr = lines[i]
        if (i > 0):
            l_prev = lines[i-1]
            if ((l_curr[sorting_index] - l_prev[sorting_index]) > 5):
                filtered_lines.append(l_curr)
        else:
            filtered_lines.append(l_curr)

    return filtered_lines


def get_crop(image, horizontal, vertical, left_line_index, right_line_index, top_line_index, bottom_line_index, offset=4, crop=0):
    x1 = vertical[left_line_index][2] - offset
    y1 = horizontal[top_line_index][3] + offset
    x2 = vertical[right_line_index][2] - offset
    y2 = horizontal[bottom_line_index][3] - offset

    if crop < 0:
        x2 = x2 + crop
    else:
        x1 = x1 + crop

    cropped_image = image[y1:y2, x1:x2]

    return cropped_image, (x1, y1, x2-x1, y2-y1)


def detect_lines(image, rho=1, theta=np.pi/180, threshold=50, minLinLength=290, maxLineGap=6, display=False, write=False):
    # Check if image is loaded fine
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if gray is None:
        print('Error opening image!')
        return -1

    dst = cv2.Canny(gray, 50, 150, None, 3)

    cImage = np.copy(image)

    linesP = cv2.HoughLinesP(dst, rho, theta, threshold,
                             None, minLinLength, maxLineGap)

    horizontal_lines = []
    vertical_lines = []

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]

            if (is_vertical(l)):
                vertical_lines.append(l)

            elif (is_horizontal(l)):
                horizontal_lines.append(l)

        horizontal_lines = overlapping_filter(horizontal_lines, 1)
        vertical_lines = overlapping_filter(vertical_lines, 0)

    if (display):
        for i, line in enumerate(horizontal_lines):
            cv2.line(cImage, (line[0], line[1]), (line[2],
                                                  line[3]), (0, 255, 0), 3, cv2.LINE_AA)

            cv2.putText(cImage, str(i) + "h", (line[0] + 5, line[1]), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 0), 1, cv2.LINE_AA)

        for i, line in enumerate(vertical_lines):
            cv2.line(cImage, (line[0], line[1]), (line[2],
                                                  line[3]), (0, 0, 255), 3, cv2.LINE_AA)
            cv2.putText(cImage, str(i) + "v", (line[0], line[1] + 5), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 0), 1, cv2.LINE_AA)

        cv2.imshow("Source", cImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return (horizontal_lines, vertical_lines)


def interpret_covid_table(image_path, display=False, print_text=False, write=False):
    src = cv2.imread(image_path)

    horizontal, vertical = detect_lines(src, display=True)

    gray = image_transform.get_grayscale(src)
    bw = image_transform.get_binary(gray)

    info = {}

    def extract_crop(label, is_number, all_characters, left_line_index, right_line_index, top_line_index, bottom_line_index, crop=0):
        cropped_image, (x, y, w, h) = get_crop(bw, horizontal, vertical,
                                               left_line_index, right_line_index, top_line_index, bottom_line_index, 4, crop)

        text = image_transform.detect(
            cropped_image, is_number, all_characters)

        if (display):
            image_with_text = image_transform.draw_text(
                src, x, y, w, h, text)
            cv2.imshow("detect", image_with_text)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        info[label] = text

    extract_crop("last_name", False, False, 0, 2, 2, 3)
    extract_crop("first_name", False, False, 2, 4, 2, 3, -100)
    extract_crop("middle_initial", False, False, 2, 4, 2, 3, 380)
    extract_crop("dob", True, False, 0, 2, 3, 4)

    extract_crop("product_name", False, False, 1, 2, 8, 9)

    return info


def interpret_patient_table(image_path, display=False):
    src = cv2.imread(image_path)

    horizontal, vertical = detect_lines(src, display=True)

    gray = image_transform.get_grayscale(src)
    bw = image_transform.get_binary(gray)

    def extract_crop(label, is_number, all_characters, left_line_index, right_line_index, top_line_index, bottom_line_index):
        cropped_image, (x, y, w, h) = get_crop(bw, horizontal, vertical,
                                               left_line_index, right_line_index, top_line_index, bottom_line_index)

        text = image_transform.detect(
            cropped_image, is_number, all_characters)

        if (display):
            image_with_text = image_transform.draw_text(
                src, x, y, w, h, text)
            cv2.imshow("detect", image_with_text)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    extract_crop("first_name", False, False, 0, 1, 0, 1)
    extract_crop("last_name", False, False, 1, 2, 0, 1)
    extract_crop("middle", False, False, 2, 3, 0, 1)
    extract_crop("date of birth", True, False, 0, 1, 1, 2)
    extract_crop("gender", False, False, 1, 2, 1, 2)
    extract_crop("cell", True, False, 2, 3, 1, 2)
    extract_crop("blood", False, False, 0, 1, 2, 3)
    extract_crop("weight", True, False, 1, 2, 2, 3)
    extract_crop("height", True, False, 2, 3, 2, 3)
    extract_crop("email", False, True, 0, 3, 3, 4)
    extract_crop("home", False, True, 0, 3, 4, 5)
    extract_crop("health insurance", False, False, 0, 2, 5, 6)
    extract_crop("work_phone", True, False, 2, 3, 5, 6)

    # conditions
    extract_crop("cond1", False, False, 0, 3, 7, 8)
    extract_crop("cond2", False, False, 0, 3, 8, 9)
    extract_crop("cond3", False, False, 0, 3, 9, 10)
    extract_crop("cond4", False, False, 0, 3, 10, 11)

    extract_crop("emergency_home", False, True, 0, 3, 12, 13)
    extract_crop("emergency_phone", True, False, 0, 3, 13, 14)


if __name__ == "__main__":
    interpret_covid_table("./temp/covid_card_fill.png", display=True)
    # interpret_patient_table(
    #    "./temp/fill patient.png", display=True)
