import datetime
import time


class system_time:
    def __init__(self, root, time_label):
        self.time_label = time_label
        self.root = root
        self.opening_time = datetime.datetime(2021, 1, 9, 7, 0, 0)
        self.is_paused = False
        self.current_time = self.opening_time
        self.pause_time = self.opening_time

    def stop_clock(self, val):
        self.is_paused = val
        self.pause_time = time.perf_counter()

    def get_time_stamp(self):
        return time.mktime(self.current_time.timetuple())

    def get_formatted_time(self):
        return self.current_time

    def get_time_difference(self, t):
        return self.convert_time(self.get_time_stamp() - (t - 120))  # subraction of 120 is a hot fix for latency

    def convert_time(self, seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        minutes = seconds // 60 - (hour * 60)
        seconds %= 60
        return "%d:%02d" % (hour, minutes)

    def clock(self):
        if not self.is_paused:
            self.current_time += datetime.timedelta(seconds=60)
            self.time_label.config(text=str(self.current_time))
        self.root.after(1000, self.clock)

    def pause(self):
        return self.is_paused
