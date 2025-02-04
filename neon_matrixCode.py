import time
import rgbmatrix 
import terminalio
import board
import framebufferio
import adafruit_display_text.label
import displayio
import requests
from datetime import datetime

# Vikunja API config
api_url = 'https://notes.pegoku.com/api/v1'
api_token = 'tk_84c5c5d9e96f22ba2fc93613946cab1d78209aa7' #Fake API key
tasksList = []

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)

font = terminalio.FONT
color = 0xFFFFFF

def display_text(text, date=''):
    group = displayio.Group()
    if date != '':
        text_area = adafruit_display_text.label.Label(font, text=text, color=color, x=32, y=16)
        group.append(text_area)

        # Create a black rectangle to clear half screen
        black_bitmap = displayio.Bitmap(32, 32, 1)
        black_palette = displayio.Palette(1)
        black_palette[0] = 0x000000  # Black color
        black_rect = displayio.TileGrid(black_bitmap, pixel_shader=black_palette, x=32, y=0)
        group.append(black_rect)
        
        date_area = adafruit_display_text.label.Label(font, text=date, color=color, x=39, y=16)
        group.append(date_area)
        display.root_group = group

        for x in range(32, -text_area.bounding_box[2], -1):
            text_area.x = x
            time.sleep(0.05)
    else:
        text_area = adafruit_display_text.label.Label(font, text=text, color=color, x=64, y=16)
        group.append(text_area)

        display.root_group = group
        
        for x in range(64, -text_area.bounding_box[2], -1):
            text_area.x = x
            time.sleep(0.05)
    
def list_all_tasks(api_url, api_token):
    headers = {
        'Authorization': f'Bearer {api_token}'
    }
    response = requests.get(f'{api_url}/tasks/all', headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()



def calculate_time(date):
    future_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    current_time = datetime.now()
    time_diff = future_date - current_time

    days = time_diff.days
    hours = time_diff.seconds // 3600

    if days > 0:
        return f'{days:02}D' if days < 100 else '99D'
    else:
        return f'{hours:02}h' if hours < 100 else '99h'

def getList():
    tasks = list_all_tasks(api_url, api_token)
    for task in tasks:
        title = task.get('title')
        due_date = task.get('due_date')
        if due_date == "0001-01-01T00:00:00Z":
            due_date = ""
        else:
            due_date = calculate_time(due_date)
        done = task.get('done')
        if not done:
            tasksList.append((title, due_date))
    return tasksList    

# Text to display
texts = getList() # [('PrintBoard', '09D'), ('Neon', '03D'), ('Alarm/Lights Home 2x', ''), ('HackPad', '39D')]

try:
    while True:
        for text, time_left in texts:
            display_text(text, time_left)
            time.sleep(1)
except KeyboardInterrupt:
    pass