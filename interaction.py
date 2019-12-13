import pyautogui


class Interaction:

    def __init__(self,
                 keypress_precision,
                 output_screen_width,
                 output_screen_height):
        self.keypress_precision = keypress_precision
        self.output_screen_width = output_screen_width
        self.output_screen_height = output_screen_height

    def move_keyboard(self, x, y):
        width = self.output_screen_width
        height = self.output_screen_height
        number_of_keypress = self.keypress_precision
        x = x - (width / 2)
        y = y - (height / 2)
        area_x = 'left' if x < 0 else 'right'
        area_y = 'up' if y < 0 else 'down'

        if area_x == 'left':
            steps_x = self.__map(x, -(width / 2), 0, number_of_keypress, 0)
        else:
            steps_x = self.__map(x, 0, width / 2, 0, number_of_keypress)

        steps_x = int(round(steps_x))
        for times in range(steps_x):
            pyautogui.press(area_x)

        if area_y == 'up':
            steps_y = self.__map(y, -(height / 2), 0, number_of_keypress, 0)
        else:
            steps_y = self.__map(y, 0, height / 2, 0, number_of_keypress)

        steps_y = int(round(steps_y * 2))
        for times in range(steps_y):
            pyautogui.press(area_y)

    def move_mouse(self, x, y):
        pyautogui.moveTo(x, y)

    def __map(self, value, start1, stop1, start2, stop2):
        newValue = ((value - start1) / (stop1 - start1)) * \
            (stop2 - start2) + start2
        return newValue
