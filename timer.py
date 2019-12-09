import time

_tick2_frame = 0
_tick2_fps = 20000000   # real raw FPS
_tick2_t0 = time.time()


def tick(fps=60):
    global _tick2_frame, _tick2_fps, _tick2_t0
    n = _tick2_fps / fps
    _tick2_frame += n
    while n > 0:
        n -= 1
    if time.time() - _tick2_t0 > 1:
        _tick2_t0 = time.time()
        _tick2_fps = _tick2_frame
        _tick2_frame = 0

# while True:
#     tick(1)             # 1 frame per second
#     print(_tick2_fps)   # see adjustment in action
#     print(time.time())

################################################################################


def tick(fps, callback):
    frame = 0
    start = time.perf_counter()
    while True:
        callback()
        frame += 1
        target = frame / fps
        passed = time.perf_counter() - start
        differ = target - passed
        if differ < 0:
            raise ValueError('callback was too slow')
        time.sleep(differ)

# tick(60, lambda: print(time.time()))

################################################################################


class Timer:

    def __init__(self, fps):
        self.__fps = fps
        self.__frame = 0
        self.__start = None

    def tick(self):
        if self.__start is None:
            self.__start = time.perf_counter()
        self.__frame += 1
        target = self.__frame / self.__fps
        passed = time.perf_counter() - self.__start
        print(passed)
        differ = target - passed
        if differ < 0:
            # raise ValueError('cannot maintain desired FPS rate')
            return True
        time.sleep(differ)
        return False
