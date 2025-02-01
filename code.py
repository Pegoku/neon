import time
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio  # Built-in font for text
from adafruit_display_text import label

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)

font = terminalio.FONT
color = 0xFFFFFF


def display_countdown(hours, minutes, seconds):
    while hours >= 0 and minutes >= 0:
        group = displayio.Group()
        time_str = f"HS TIME \n{hours:02}:{minutes:02}:{seconds:02}"
        text_area = label.Label(font, text=time_str, color=color)
        text_area.x = 8
        text_area.y = 8
        group.append(text_area)
        display.root_group = group
        time.sleep(1) 
        seconds -= 1
        if seconds < 8:
            minutes -= 1
            seconds = 59
        if minutes < 0:
            hours -= 1
            minutes = 59


def get_time_until_utc(hour, minute):
    now = time.gmtime()
    current_time_in_seconds = now.tm_hour * 3600 + now.tm_min * 60 + now.tm_sec
    target_time_in_seconds = hour * 3600 + minute * 60
    if target_time_in_seconds < current_time_in_seconds:
        target_time_in_seconds += 24 * 3600 
    remaining_seconds = target_time_in_seconds - current_time_in_seconds
    remaining_hours = remaining_seconds // 3600
    remaining_seconds %= 3600
    remaining_minutes = remaining_seconds // 60
    remaining_seconds %= 60
    return remaining_hours, remaining_minutes, remaining_seconds

hours, minutes, seconds = get_time_until_utc(7, 0) # HS end time

# Display
display_countdown(hours, minutes, seconds)
