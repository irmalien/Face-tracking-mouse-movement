import time


class Framerate:

    def __init__(self, fps):
        self.__fps = fps
        self.__frame = 0
        self.__start = None
        self.actual_fps = 0

    def counter(self):
        if self.__start is None:
            self.__start = time.perf_counter()
        if self.__frame % 30 == 0:
            self.__start = time.perf_counter()
            self.__frame = 0
        self.__frame += 1

        target = self.__frame / self.__fps
        passed = time.perf_counter() - self.__start
        differ = target - passed
        self.actual_fps = round(self.__frame / passed)
        if self.actual_fps > 1000:
            self.actual_fps = 0
        if differ < 0:
            # raise ValueError('cannot maintain desired FPS rate')
            return True
        time.sleep(differ)
        return False
