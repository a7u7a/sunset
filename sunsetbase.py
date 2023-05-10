import sys
import random
import os
from time import sleep
from rgbmatrix import graphics
import json
from typing import Tuple
from ticker_data import TickerData
# Import samplebase from parent directory 'samples'
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from samplebase import SampleBase


panel_width = 64
panel_height = 32

class Sunset(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Sunset, self).__init__(*args, **kwargs)

    def load_stocks(self):
        try:
            with open('stock_data.json') as json_file:
                self.stock_data = json.load(json_file)
                print("Updated stock data OK")
        except Exception as e: 
            print("ERROR load_stocks:",e)
            print("Error updating stock data")
            self.stock_data = None

    def to_rectangular(self,x,y):
        """ Maps pixel position from square panel arrangment (ie 64x64, one on top of the other) to rectangular (ie 32x128, side by side)"""
        panel_num = y // panel_height
        new_x = x + panel_num * panel_width
        new_y = y % panel_height
        new_x %= panel_width * 2
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

    def draw_layer(self,centerline, color):
        point1 = (0, centerline)
        numPoints = 7
        for i in range(numPoints):
            if i == 5:
                x = panel_width-1
            else:
                x = abs(int(((panel_width/numPoints)*i) + random.randint(-2,2)))
                if x > panel_width:
                    x -= 3
            y = centerline + random.randint(-12,12)
            point2 = (x, y)
            self.draw_line_and_fill(point1, point2, color)
            point1 = point2


    def run(self):
        self.offset_canvas = self.matrix.CreateFrameCanvas()
        self.tickers = TickerData().tickers
        print("self.tickers",self.tickers)

        while True:
            centerline = 14
        # while True: 
        #     self.offset_canvas.Clear()
        #     centerline = 14
        #     c1 = (random.randint(0,255), random.randint(0,255), random.randint(0,255)) 
        #     c2 = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        #     c3 = (random.randint(0,255),random.randint(0,255) ,random.randint(0,255) )
        #     colors = [c1, c2, c3]
        #     for i in range(3):
        #         self.draw_layer(centerline, colors[i])
        #         centerline += 12

        #     self.offset_canvas = self.matrix.SwapOnVSync(self.offset_canvas)
            # sleep(.1)

if __name__ == "__main__":
    sunset = Sunset()
    if (not sunset.process()):
        sunset.print_help()