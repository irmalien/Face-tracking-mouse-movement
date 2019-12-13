import numpy as np
import cv2


class Draw:

    def selected_face_area(self, image, selected_face=None):
        if selected_face:
            start_point = (int(selected_face[1]), int(selected_face[2]))
            end_point = (int(selected_face[1] + selected_face[3]),
                         int(selected_face[2] + selected_face[4]))
            cv2.rectangle(image, start_point, end_point, (255, 0, 0), 1)

    def capture_crop_area(self, image, crop):
        start_point = (int(crop['margin_x']), int(crop['margin_y']))
        full_width = int(crop['margin_x']) + int(crop['w'])
        full_height = int(crop['margin_y']) + int(crop['h'])
        end_point = (full_width, full_height)
        cv2.rectangle(image, start_point, end_point, (255, 0, 0), 1)

    def cursor_location(self, image, pos):
        x = pos['x']
        y = pos['y']
        cv2.circle(image, (int(x), int(y)), 2, (0, 0, 255), 2)
