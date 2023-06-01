import sys
import random
import os
from time import sleep
from rgbmatrix import graphics
import json
from typing import Tuple
from ticker_data import TickerData
from datetime import datetime, timedelta
import math
# Import samplebase from parent directory 'samples'
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from samplebase import SampleBase


panel_width = 96
panel_height = 96

class Sunset(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Sunset, self).__init__(*args, **kwargs)
        self.sun_color = (253, 28, 8)
        self.stock_data = None
        self.load_stocks()

    def load_stocks(self):
        try:
            with open('stock_data.json') as json_file:
                self.stock_data = json.load(json_file)
                print("Updated stock data OK")
        except Exception as e: 
            print("ERROR load_stocks:",e)
            print("Error updating stock data")
            self.stock_data = None

    def to_rectangular(self, x, y):
        """ Maps pixel position from square panel arrangement (ie 64x64, one on top of the other) 
        to rectangular (ie 32x128, side by side) and constrains them to the screen space."""
        
        panel_num = y // panel_height
        new_x = x + panel_num * panel_width
        new_y = y % panel_height

        # Constrain x to the screen width
        if new_x >= panel_width*2:
            new_x = panel_width*2 - 1

        return new_x, new_y
    
    def draw_line_and_fill(self, point1: Tuple[int, int], point2: Tuple[int, int], color: Tuple[int, int, int]):
        x1, y1 = point1
        x2, y2 = point2
        r, g, b = color

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        if dx == 0 and dy == 0:
            _x, _y = self.to_rectangular(x1,y1)
            self.offset_canvas.SetPixel(_x, _y, r, g, b)
            return

        steep = dy > dx
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            dx, dy = dy, dx

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        error = int(dx / 2)
        y = y1
        y_step = 1 if y1 < y2 else -1

        for x in range(x1, x2 + 1):
            if steep:
                self.fill_column(y, x, r, g, b)
            else:
                self.fill_column(x, y, r, g, b)

            error -= dy
            if error < 0:
                y += y_step
                error += dx

    def fill_column(self, x: int, y: int, r: int, g: int, b: int):
        for y_fill in range(y, panel_height*2):
            _x, _y = self.to_rectangular(x,y_fill)
            self.offset_canvas.SetPixel(_x, _y, r, g, b)

    def draw_filled_circle(self, center_x, center_y, radius, color):
        """Draws a filled circle at a specified location with a specified radius and color."""
        r, g, b = color
        def set_circle_points(x, y):
            """Sets pixels to create a filled circle."""
            for i in range(center_x - x, center_x + x + 1):
                new_x, new_y = self.to_rectangular(i, center_y + y)
                self.offset_canvas.SetPixel(new_x, new_y, r, g, b)
                new_x, new_y = self.to_rectangular(i, center_y - y)
                self.offset_canvas.SetPixel(new_x, new_y, r, g, b)

            for i in range(center_x - y, center_x + y + 1):
                new_x, new_y = self.to_rectangular(i, center_y + x)
                self.offset_canvas.SetPixel(new_x, new_y, r, g, b)
                new_x, new_y = self.to_rectangular(i, center_y - x)
                self.offset_canvas.SetPixel(new_x, new_y, r, g, b)

        x = radius
        y = 0
        err = 0

        while x >= y:
            set_circle_points(x, y)
            y += 1
            if err <= 0:
                err += 2*y + 1
            if err > 0:
                x -= 1
                err -= 2*x + 1

    

    def plot_data(self, data, color=(255, 255, 255),lower_limit=10, upper_limit=0):
        # Step 1: Preprocess data
        dates = list(data.keys())
        values = list(data.values())
        
        # Convert date strings to datetime objects
        dates = [datetime.strptime(date, "%Y-%m-%d") for date in dates]

        # Replace "nodata" with None and convert others to float
        values = [None if value == "nodata" or value == "null" else float(value) for value in values]
        
        # Step 2: Normalize data to fit LED panel
        max_value = max(v for v in values if v is not None)
        min_value = min(v for v in values if v is not None)
        
        # Normalize to panel height
        normalized_values = [lower_limit - (value - min_value) / (max_value - min_value) * (lower_limit - upper_limit) if value is not None else None for value in values]
    
        # Step 3: Iterate over data and plot
        last_valid_y = None
        for i in range(1, len(dates)):
            x1 = (dates[i - 1] - dates[0]).days / (dates[-1] - dates[0]).days * (int(panel_width) - 1)
            x2 = (dates[i] - dates[0]).days / (dates[-1] - dates[0]).days * (int(panel_width) - 1)

            if normalized_values[i - 1] is not None:
                y1 = normalized_values[i - 1]
                last_valid_y = y1
            else:
                y1 = last_valid_y
            
            if normalized_values[i] is not None:
                y2 = normalized_values[i]
                last_valid_y = y2
            else:
                y2 = last_valid_y
            
            # debug points
            # x11,y11 = self.to_rectangular(int(x1), int(y1))
            # x22,y22 = self.to_rectangular(int(x2), int(y2))
            # self.draw_filled_circle(x11,y11,4,self.sun_color)
            # self.draw_filled_circle(x22,y22,4,self.sun_color)
            
            self.draw_line_and_fill((int(x1), int(y1)), (int(x2), int(y2)), color)



    def get_sun_position(self,current_time):
        # calculate minutes from midnight
        minutes_from_midnight = current_time.hour * 60 + current_time.minute
        # normalize it to a 0-1 scale (0 at midnight, 1 at next midnight)
        normalized_time = minutes_from_midnight / (24*60)
        # we use cos function to emulate the sun's movement, it returns 1 at midnight, 0 at 6AM, -1 at noon, 0 at 6PM and 1 at midnight again
        sun_elevation = math.cos(2*math.pi * normalized_time)
        # normalize sun elevation to a panel_height/2-panel_height scale (panel_height/2 at lowest, 0 at highest)
        screen_position = abs(panel_height-int((panel_height / 2) * (1-sun_elevation))) # abs to invert
        return screen_position

    def draw_sun(self, offset):
        """Draw sun according to time"""
        current_time = datetime.now()
        sun_radius = 20
        future_time = current_time + timedelta(hours=offset)
        sun_y_pos = self.get_sun_position(future_time)
        x,y = self.to_rectangular(int(panel_width/2), sun_y_pos)
        self.draw_filled_circle(x,y,sun_radius,self.sun_color)

    def get_color_from_tickers(self, name):
        for ticker in self.tickers["tickers"]:
            if name == ticker["symbol"]:
                return tuple(ticker["color"])

    def fill_color(self, color):
        r, g, b = color
        for y in range(panel_height):
            for x in range(panel_width):
                x_,y_ = self.to_rectangular(x, y)
                self.offset_canvas.SetPixel(x_, y_, r, g, b)

    def update_sky_color(self, offset):
        # Get the current time
        now = datetime.now()
        future_time = now + timedelta(hours=offset)
        future_time = future_time - timedelta(hours=6) # extra offset to fix bug

        # Normalize the time to a value between 0 (midnight) and 1 (next midnight)
        t = ((future_time.hour * 60 + future_time.minute) * 60 + future_time.second) / 86400  # 86400 seconds in a day

        # Define sky colors for different times of day
        colors = [
            (141, 164, 195),  # morning
            (47, 97, 135),  # midday
            (0, 25, 51),  # evening
            (0, 0, 0),  # midnight
        ]

        # Calculate the index and interpolation factor for the current time
        t *= len(colors)
        i = int(t)
        t -= i

        # Interpolate between the current and next colors
        color = [c1 * (1 - t) + c2 * t for c1, c2 in zip(colors[i % len(colors)], colors[(i + 1) % len(colors)])]
        # Fill the screen with the color
        self.fill_color(tuple(map(int, color)))

    def run(self):
        self.offset_canvas = self.matrix.CreateFrameCanvas()
        self.tickers = TickerData().tickers

        # to test sun position
        # for t in range(24):
        #     self.offset_canvas.Clear()
        #     self.update_sky_color(t) # testing background color
        #     self.draw_sun(t)
        #     self.offset_canvas = self.matrix.SwapOnVSync(self.offset_canvas)
        #     sleep(1)

        while True: 
            if self.stock_data is not None:
                futures = list(self.stock_data.keys())
                self.offset_canvas.Clear()
                upper = 40
                lower = 60
                self.update_sky_color(0)
                self.draw_sun(0)
                for future in futures:
                    future_data = self.stock_data[future]
                    # c1 = (random.randint(0,255), random.randint(0,255), random.randint(0,255)) 
                    color = self.get_color_from_tickers(future)
                    self.plot_data(future_data, color, lower, upper)
                    # modify limits after plotting
                    h = int(panel_height/4)
                    upper += random.randint(h-4,h+4)
                    lower += random.randint(h-4,h+4)
                self.offset_canvas = self.matrix.SwapOnVSync(self.offset_canvas)
                sleep(60)
                

if __name__ == "__main__":
    sunset = Sunset()
    if (not sunset.process()):
        sunset.print_help()
