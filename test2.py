import sys
import random
import os
from time import sleep
from rgbmatrix import graphics
# Import samplebase from parent directory 'samples'
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from samplebase import SampleBase

print("henlo")

panel_width = 64
panel_height = 32

class SimpleSquare(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SimpleSquare, self).__init__(*args, **kwargs)

    def my_mapping(self,x,y):
        panel_num = y // panel_height

        new_x = x + panel_num * panel_width
        new_y = y % panel_height

        new_x %= panel_width * 2
        return new_x, new_y
    
    def draw_layer(self, centerline, distance, r,g,b):
        for i in range(panel_width):
            y = centerline + random.randint(-distance,distance)
            for p in range(y, panel_height*2):
               fx, fy = self.my_mapping(i,p)
               self.offset_canvas.SetPixel(fx, fy, r,g,b)

    def run(self):
        self.offset_canvas = self.matrix.CreateFrameCanvas()

        
        self.draw_layer(10, 3, 0, 255, 0)
        self.draw_layer(20, 4, 255, 255, 0)
        self.draw_layer(40, 5, 0, 255, 255)
        self.draw_layer(50, 1, 30, 15, 100)

        self.offset_canvas = self.matrix.SwapOnVSync(self.offset_canvas)

        sleep(20)
        # while True:
        #     square_x += random.randint(-d,d)
        #     square_y += random.randint(-d,d)
        #     square_x += 1
        #     square_y += 1
        #     # print("input",square_x,square_y)
        #     x,y = self.my_mapping(square_x,square_y)
        #     # print("output",x,y)
        #     offset_canvas.SetPixel(x, y, 255, 255, 255)
        #     offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
        #     sleep(.01)

if __name__ == "__main__":
    simple_square = SimpleSquare()
    if (not simple_square.process()):
        simple_square.print_help()