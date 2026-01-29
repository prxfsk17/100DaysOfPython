import os
import cv2
import datetime
import pyautogui
import numpy as np
from pynput.keyboard import Key, Controller

OBSTACLE_BOUNDING_ORIGIN = (745, 875)
OBSTACLE_BOUNDING_END = (790, 900)
HIGHEST_JUMP_BOUNDING_ORIGIN = (670, 777)
HIGHEST_JUMP_BOUNDING_END = (715, 800)
KEYBOARD = Controller()
BOUND_AREA_COLORS = {
    1: (0, 0, 255),
    0: (0, 255, 0)
}
UP_DOWN_STATUS = {
    'up': 1,
    'down': 0
}
STATUS_IMAGE_Y = (490, 1078)
STATUS_IMAGE_X = (0, 1897)
STATUS_IMAGE_RES = (1897, 588 )

jumps = 0
prev_up_down_status = UP_DOWN_STATUS['down']


def check_contours_of_expected_area(image, area_thresh=0):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 100, 250)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for c in contours:
        area = cv2.contourArea(c)
        if area > area_thresh:
            return 1
    return 0


def count_jumps(cont_avb):
    global prev_up_down_status, jumps

    if cont_avb is UP_DOWN_STATUS['up']:
        if cont_avb is not prev_up_down_status:
            jumps += 1
            prev_up_down_status = cont_avb
    else:
        prev_up_down_status = 0


def App():
    global jumps

    cv2.waitKey(5000)

    jumps = 0

    KEYBOARD.press(Key.space)
    cv2.waitKey(1)
    KEYBOARD.release(Key.space)

    while True:
        screen_image = np.array(pyautogui.screenshot())
        screen_image = cv2.cvtColor(screen_image, cv2.COLOR_BGR2RGB)
        screen_image = screen_image[STATUS_IMAGE_Y[0]: STATUS_IMAGE_Y[1], STATUS_IMAGE_X[0]: STATUS_IMAGE_X[1]]

        front_obs_block = screen_image[
            OBSTACLE_BOUNDING_ORIGIN[1]: OBSTACLE_BOUNDING_END[1] + 1,
            OBSTACLE_BOUNDING_ORIGIN[0]: OBSTACLE_BOUNDING_END[0] + 1
        ]
        highest_jump_block = screen_image[
            HIGHEST_JUMP_BOUNDING_ORIGIN[1]: HIGHEST_JUMP_BOUNDING_END[1] + 1,
            HIGHEST_JUMP_BOUNDING_ORIGIN[0]: HIGHEST_JUMP_BOUNDING_END[0] + 1
        ]

        avb = check_contours_of_expected_area(front_obs_block)
        obstacle_area_color, obstacle_status = BOUND_AREA_COLORS[0], 0

        if avb:
            obstacle_area_color, obstacle_status = BOUND_AREA_COLORS[1], 1

            KEYBOARD.press(Key.space)
            cv2.waitKey(1)
            KEYBOARD.release(Key.space)

        avb = check_contours_of_expected_area(highest_jump_block)
        highest_jump_bound_area_color, jump_status = BOUND_AREA_COLORS[0], 0

        if avb:
            highest_jump_bound_area_color, jump_status = BOUND_AREA_COLORS[1], 1
        count_jumps(avb)

        cv2.rectangle(screen_image, OBSTACLE_BOUNDING_ORIGIN, OBSTACLE_BOUNDING_END, obstacle_area_color, 2)
        cv2.rectangle(screen_image, HIGHEST_JUMP_BOUNDING_ORIGIN, HIGHEST_JUMP_BOUNDING_END,
                      highest_jump_bound_area_color, 2)
        cv2.rectangle(screen_image, (OBSTACLE_BOUNDING_ORIGIN[0], OBSTACLE_BOUNDING_ORIGIN[1] - 22),
                      (OBSTACLE_BOUNDING_ORIGIN[0] + 22, OBSTACLE_BOUNDING_ORIGIN[1]), obstacle_area_color, -1)
        cv2.rectangle(screen_image, (HIGHEST_JUMP_BOUNDING_END[0], HIGHEST_JUMP_BOUNDING_ORIGIN[1]),
                      (HIGHEST_JUMP_BOUNDING_END[0] + 22, HIGHEST_JUMP_BOUNDING_ORIGIN[1] + 22),
                      highest_jump_bound_area_color, -1)

        screen_image = cv2.putText(screen_image, 'JUMPS: {}'.format(jumps), (570, 43), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                                   (0, 0, 255), 2)
        screen_image = cv2.putText(screen_image, '{}'.format(obstacle_status), (384, 167), cv2.FONT_HERSHEY_SIMPLEX,
                                   0.7, (255, 255, 255), 2)
        screen_image = cv2.putText(screen_image, '{}'.format(jump_status), (345, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                   (255, 255, 255), 2)

        cv2.imshow("LIVE | Automated Chrome Dinosaur", screen_image)

        k = cv2.waitKey(1)
        if k == 27:
            return

App()
cv2.destroyAllWindows()