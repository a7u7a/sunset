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


panel_width = 128
panel_height = 128

class Sunset(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Sunset, self).__init__(*args, **kwargs)
        self.sun_color = (177, 136, 58)
        self.stock_data = None

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
        if new_x >= panel_width * 2:
            new_x = panel_width * 2 - 1

        return new_x, new_y
    

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

    def run(self):
        self.offset_canvas = self.matrix.CreateFrameCanvas()
        self.tickers = TickerData().tickers
        
        while True: 
            self.offset_canvas.Clear()
            tx = random.randint(0,127)
            ty = random.randint(0,127)

            x,y = self.to_rectangular(tx, ty)
            print("tx",tx, "ty",ty)
            print("x",x, "y",y)
            print("")
            self.draw_filled_circle(x,y,10,self.sun_color)
            self.offset_canvas = self.matrix.SwapOnVSync(self.offset_canvas)
            sleep(.5)


if __name__ == "__main__":
    sunset = Sunset()
    if (not sunset.process()):
        sunset.print_help()