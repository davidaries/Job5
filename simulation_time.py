import datetime
import time
from icecream import ic

time_label = None
root = None
opening_time = datetime.datetime(2021, 1, 9, 7, 0, 0)
is_paused = False
current_time = opening_time
pause_time = opening_time


def stop_clock(val):
    global is_paused, pause_time
    is_paused = val
    pause_time = time.perf_counter()


def get_time_stamp():
    return time.mktime(current_time.timetuple())


def get_formatted_time():
    return current_time


def get_time_difference(t):
    return convert_time(get_time_stamp() - (t - 120))  # subraction of 120 is a hot fix for latency


def convert_time(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    minutes = seconds // 60 - (hour * 60)
    seconds %= 60
    return "%d:%02d" % (hour, minutes)


def clock():
    global current_time, root, time_label
    if not is_paused:
        current_time += datetime.timedelta(seconds=60)
        time_label.config(text=str(current_time))
    root.after(1000, clock)


def pause():
    return is_paused


def set_ui_tools(rt, timelbl):
    global root, time_label
    root = rt
    time_label = timelbl
