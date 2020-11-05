class Animation:
    def __init__(self, start_pos: (int, int), end_pos: (int, int), duration: int):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.curr_pos = start_pos
        self.duration = duration
        self._time_elapsed = 0

    def start(self):
        self._time_elapsed = 0
        self.curr_pos = self.start_pos

    def update(self, time_elapsed: int) -> bool:
        self._time_elapsed += time_elapsed
        start_x, start_y = self.start_pos
        end_x, end_y = self.end_pos
        move_factor = self._time_elapsed / self.duration
        self.curr_pos = ((end_x - start_x) * move_factor, (end_y - start_y) * move_factor)
        print("Current position: [%s, %s]" % self.curr_pos)
        return self._time_elapsed >= self.duration
