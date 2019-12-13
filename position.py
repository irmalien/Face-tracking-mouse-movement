class Position:

    def __init__(self,
                 smooth_intensity,
                 input_screen_width,
                 input_screen_height,
                 output_screen_width,
                 output_screen_height,
                 capture_crop_factor):
        self.smooth_intensity = smooth_intensity
        self.input_screen = {
            "w": input_screen_width,
            "h": input_screen_height,
            "pos": {
                "x": None,
                "y": None
            }
        }
        self.crop_screen = {
            "scale": capture_crop_factor,
            "w": None,
            "h": None,
            "margin_x": None,
            "margin_y": None,
            "pos": {
                "x": None,
                "y": None
            }
        }
        self.output_screen = {
            "w": output_screen_width,
            "h": output_screen_height,
            "history": [],
            "pos": {
                "x": None,
                "y": None
            }
        }
        self.__populate_crop_screen_params()

    def smooth_resized_position(self, x, y):
        self.input_screen['pos'] = {"x": x, "y": y}
        self.output_screen['pos'] = self.__resize_input_pos(
            self.input_screen['pos'])
        self.__save_pos_in_history(self.output_screen['pos'])
        smooth_position = self.__find_average_in_history()
        return smooth_position

    def __resize_input_pos(self, pos):
        self.crop_screen['pos'] = self.__crop_input_pos(pos)
        adjusted_pos = self.__adjust_pos_in_crop_screen(self.crop_screen)
        output_screen_pos = self.__resize_pos(adjusted_pos)
        return output_screen_pos

    def __populate_crop_screen_params(self):
        width = self.input_screen['w'] * self.crop_screen['scale']
        height = self.input_screen['h'] * self.crop_screen['scale']
        margin_x = (self.input_screen['w'] - width) / 2
        margin_y = (self.input_screen['h'] - height) / 2
        self.crop_screen['w'] = int(width)
        self.crop_screen['h'] = int(height)
        self.crop_screen['margin_x'] = int(margin_x)
        self.crop_screen['margin_y'] = int(margin_y)

    def __adjust_pos_in_crop_screen(self, crop_screen):
        x = crop_screen['pos']['x']
        y = crop_screen['pos']['y']
        x -= crop_screen['margin_x']
        y -= crop_screen['margin_y']
        return {"x": x, "y": y}

    def __crop_input_pos(self, pos):
        x = pos['x']
        y = pos['y']
        crop = self.crop_screen
        crop_x_start = crop['margin_x']
        crop_x_end = crop['margin_x'] + crop['w']
        crop_y_start = crop['margin_y']
        crop_y_end = crop['margin_y'] + crop['h']
        if x < crop_x_start:
            x = crop_x_start
        if x > crop_x_end:
            x = crop_x_end
        if y < crop_y_start:
            y = crop_y_start
        if y > crop_y_end:
            y = crop_y_end
        return {"x": x, "y": y}

    def __resize_pos(self, pos):
        x = self.__resize_pos_x(pos['x'])
        y = self.__resize_pos_y(pos['y'])
        return {"x": x, "y": y}

    def __resize_pos_x(self, x):
        position_in_input = x
        input = self.crop_screen['w']
        output = self.output_screen['h']
        position_in_output = (position_in_input * output) / input
        return position_in_output

    def __resize_pos_y(self, y):
        position_in_input = y
        input = self.crop_screen['h']
        output = self.output_screen['h']
        position_in_output = (position_in_input * output) / input
        return position_in_output

    def __save_pos_in_history(self, pos):
        x = pos['x']
        y = pos['y']
        self.output_screen['history'].append([x, y])
        if len(self.output_screen['history']) > self.smooth_intensity:
            self.output_screen['history'].pop(0)
            return

    def __find_average_in_history(self):
        list = self.output_screen['history']
        ncols = len(list[0])
        nrows = len(list)
        # Sum all elements in each column:
        results = ncols * [0]  # sums per column, afterwards avgs
        for col in range(ncols):
            for row in range(nrows):
                results[col] += list[row][col]
        # Then calculate averages:
        # * nrows is also number of elements in every col:
        num_of_elements = float(nrows)

        results = [int(sum / num_of_elements) for sum in results]
        return results
