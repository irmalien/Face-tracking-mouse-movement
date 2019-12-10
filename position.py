class Position:

    def __init__(self,
                 smooth_intensity,
                 input_screen_width,
                 input_screen_height,
                 output_screen_width,
                 output_screen_height):
        self.history = []
        self.smooth_intensity = smooth_intensity
        self.input_screen_width = input_screen_width
        self.input_screen_height = input_screen_height
        self.output_screen_width = output_screen_width
        self.output_screen_height = output_screen_height

    def smooth_resized_position(self, x, y):
        self.resized_position(x, y)
        self.__save_position()
        return self.__find_average_position()

    def resized_position(self, x, y):
        self.x = self.__resize_position_x(x)
        self.y = self.__resize_position_y(y)
        return [self.x, self.y]

    def __resize_position_x(self, position_in_input):
        input = self.input_screen_width
        output = self.output_screen_width
        position_in_output = (position_in_input * output) / input
        return position_in_output

    def __resize_position_y(self, position_in_input):
        input = self.input_screen_height
        output = self.output_screen_height
        position_in_output = (position_in_input * output) / input
        return position_in_output

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
