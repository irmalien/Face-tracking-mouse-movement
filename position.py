class Position:

    def __init__(self,
                 smooth_intensity,
                 input_screen_width,
                 input_screen_height,
                 output_screen_width,
                 output_screen_height,
                 capture_crop_factor):
        self.history = []
        self.smooth_intensity = smooth_intensity
        self.input_screen_width = input_screen_width
        self.input_screen_height = input_screen_height
        self.output_screen_width = output_screen_width
        self.output_screen_height = output_screen_height
        self.capture_crop_factor = capture_crop_factor
        self.capture_crop_size = self.__apply_crop_factor()

    def smooth_resized_position(self, x, y):
        self.resized_position(x, y)
        self.__save_position()
        return self.__find_average_position()

    def resized_position(self, x, y):
        self.x = x
        self.y = y
        self.__limit_position_in_crop_size()
        self.__define_position_in_crop_size()
        self.__resize_position_x()
        self.__resize_position_y()
        return [self.x, self.y]

    def __apply_crop_factor(self):
        crop_width = self.input_screen_width * self.capture_crop_factor
        crop_height = self.input_screen_height * self.capture_crop_factor
        margin_x = (self.input_screen_width - crop_width) / 2
        margin_y = (self.input_screen_height - crop_height) / 2
        return [margin_x, margin_y, crop_width, crop_height]

    def __define_position_in_crop_size(self):
        self.x = self.x - self.capture_crop_size[0]
        self.y = self.y - self.capture_crop_size[1]

    def __limit_position_in_crop_size(self):
        crop_x_start = self.capture_crop_size[0]
        crop_x_end = self.capture_crop_size[0] + self.capture_crop_size[2]
        crop_y_start = self.capture_crop_size[1]
        crop_y_end = self.capture_crop_size[1] + self.capture_crop_size[3]
        if self.x < crop_x_start:
            self.x = crop_x_start
        if self.x > crop_x_end:
            self.x = crop_x_end
        if self.y < crop_y_start:
            self.y = crop_y_start
        if self.y > crop_y_end:
            self.y = crop_y_end

    def __resize_position_x(self):
        position_in_input = self.x
        input = self.capture_crop_size[2]
        output = self.output_screen_width
        position_in_output = (position_in_input * output) / input
        self.x = position_in_output

    def __resize_position_y(self):
        position_in_input = self.y
        input = self.capture_crop_size[3]
        output = self.output_screen_height
        position_in_output = (position_in_input * output) / input
        self.y = position_in_output

    def __save_position(self):
        self.history.append([self.x, self.y])
        if len(self.history) > self.smooth_intensity:
            self.history.pop(0)
            return

    def __find_average_position(self):
        list = self.history
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
