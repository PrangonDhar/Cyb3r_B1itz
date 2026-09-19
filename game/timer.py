import time


class GameTimer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.perf_counter()
        self.end_time = None

    def stop(self):
        if self.start_time is not None:
            self.end_time = time.perf_counter()

    def elapsed_seconds(self):
        if self.start_time is None:
            return 0.0

        end = self.end_time or time.perf_counter()

        return end - self.start_time


class QuestionTimer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = None

    def start(self):
        self.start_time = time.perf_counter()

    def elapsed(self):
        if self.start_time is None:
            return 0.0

        return time.perf_counter() - self.start_time

    def remaining(self):
        return max(0.0, self.duration - self.elapsed())

    def expired(self):
        return self.elapsed() >= self.duration
    