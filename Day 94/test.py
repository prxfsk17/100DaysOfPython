import os
import cv2
import datetime
import pyautogui
import numpy as np
from pynput.keyboard import Key, Controller

OBSTACLE_BOUNDING_ORIGIN = (745, 875)
OBSTACLE_BOUNDING_END = (820, 900)
HIGHEST_JUMP_BOUNDING_ORIGIN = (670, 777)
HIGHEST_JUMP_BOUNDING_END = (715, 800)

STATUS_IMAGE_Y = (490, 1078)
STATUS_IMAGE_X = (0, 1897)

OBSTACLE_BOUNDING_RELATIVE_ORIGIN = (
    OBSTACLE_BOUNDING_ORIGIN[0] - STATUS_IMAGE_X[0],
    OBSTACLE_BOUNDING_ORIGIN[1] - STATUS_IMAGE_Y[0]
)
OBSTACLE_BOUNDING_RELATIVE_END = (
    OBSTACLE_BOUNDING_END[0] - STATUS_IMAGE_X[0],
    OBSTACLE_BOUNDING_END[1] - STATUS_IMAGE_Y[0]
)

HIGHEST_JUMP_BOUNDING_RELATIVE_ORIGIN = (
    HIGHEST_JUMP_BOUNDING_ORIGIN[0] - STATUS_IMAGE_X[0],
    HIGHEST_JUMP_BOUNDING_ORIGIN[1] - STATUS_IMAGE_Y[0]
)
HIGHEST_JUMP_BOUNDING_RELATIVE_END = (
    HIGHEST_JUMP_BOUNDING_END[0] - STATUS_IMAGE_X[0],
    HIGHEST_JUMP_BOUNDING_END[1] - STATUS_IMAGE_Y[0]
)

KEYBOARD = Controller()
BOUND_AREA_COLORS = {
    1: (0, 0, 255),
    0: (0, 255, 0)
}
UP_DOWN_STATUS = {
    'up': 1,
    'down': 0
}

jumps = 0
prev_up_down_status = UP_DOWN_STATUS['down']
# Создаем папку для сохранения изображений
os.makedirs("debug_snapshots", exist_ok=True)


def check_contours_of_expected_area(image, area_thresh=0):
    # Проверяем, что изображение не пустое
    if image is None or image.size == 0:
        print("Предупреждение: передан пустой image для анализа контуров")
        return 0

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
    print("Запуск через 5 секунд...")

    jumps = 0

    KEYBOARD.press(Key.space)
    cv2.waitKey(1)
    KEYBOARD.release(Key.space)
    print("Начат процесс...")

    while True:
        try:
            full_screenshot = np.array(pyautogui.screenshot())
            full_screenshot = cv2.cvtColor(full_screenshot, cv2.COLOR_BGR2RGB)

            screen_image = full_screenshot[
                STATUS_IMAGE_Y[0]: STATUS_IMAGE_Y[1],
                STATUS_IMAGE_X[0]: STATUS_IMAGE_X[1]
            ]

            front_obs_block = full_screenshot[
                OBSTACLE_BOUNDING_ORIGIN[1]: OBSTACLE_BOUNDING_END[1],
                OBSTACLE_BOUNDING_ORIGIN[0]: OBSTACLE_BOUNDING_END[0]
            ]

            highest_jump_block = full_screenshot[
                HIGHEST_JUMP_BOUNDING_ORIGIN[1]: HIGHEST_JUMP_BOUNDING_END[1],
                HIGHEST_JUMP_BOUNDING_ORIGIN[0]: HIGHEST_JUMP_BOUNDING_END[0]
            ]

            print(f"Размеры: full_screenshot={full_screenshot.shape}, "
                  f"front_obs_block={front_obs_block.shape if front_obs_block.size > 0 else 'empty'}, "
                  f"highest_jump_block={highest_jump_block.shape if highest_jump_block.size > 0 else 'empty'}")



            avb = check_contours_of_expected_area(front_obs_block)
            obstacle_area_color, obstacle_status = BOUND_AREA_COLORS[0], 0

            if avb:
                obstacle_area_color, obstacle_status = BOUND_AREA_COLORS[1], 1
                print("Обнаружено препятствие! Прыжок!")
                KEYBOARD.press(Key.space)
                cv2.waitKey(1)
                KEYBOARD.release(Key.space)

            avb = check_contours_of_expected_area(highest_jump_block)
            highest_jump_bound_area_color, jump_status = BOUND_AREA_COLORS[0], 0

            if avb:
                highest_jump_bound_area_color, jump_status = BOUND_AREA_COLORS[1], 1
                print("Высокий прыжок обнаружен!")

            count_jumps(avb)

            cv2.rectangle(screen_image,
                          OBSTACLE_BOUNDING_RELATIVE_ORIGIN,
                          OBSTACLE_BOUNDING_RELATIVE_END,
                          obstacle_area_color, 2)

            cv2.rectangle(screen_image,
                          HIGHEST_JUMP_BOUNDING_RELATIVE_ORIGIN,
                          HIGHEST_JUMP_BOUNDING_RELATIVE_END,
                          highest_jump_bound_area_color, 2)

            screen_image = cv2.putText(screen_image, f'JUMPS: {jumps}', (570, 43),
                                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

            screen_image = cv2.putText(screen_image, f'OBSTACLE: {obstacle_status}',
                                       (OBSTACLE_BOUNDING_RELATIVE_ORIGIN[0],
                                        OBSTACLE_BOUNDING_RELATIVE_ORIGIN[1] - 10),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            screen_image = cv2.putText(screen_image, f'JUMP: {jump_status}',
                                       (HIGHEST_JUMP_BOUNDING_RELATIVE_ORIGIN[0],
                                        HIGHEST_JUMP_BOUNDING_RELATIVE_ORIGIN[1] - 10),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            cv2.imshow("LIVE | Automated Chrome Dinosaur", screen_image)
            cv2.waitKey(1)  # Обновляем окно

        except Exception as e:
            print(f"Ошибка в основном цикле: {e}")
            import traceback
            traceback.print_exc()
            break

        if cv2.waitKey(1) & 0xFF == 27:
            print(f"Программа завершена.")
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        App()
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
    finally:
        cv2.destroyAllWindows()