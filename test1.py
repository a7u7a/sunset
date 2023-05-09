import sys
import random
import os
from time import sleep
# Import samplebase from parent directory 'samples'
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from samplebase import SampleBase

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

    def run(self):
        offset_canvas = self.matrix.CreateFrameCanvas()

        square_x = 0
        square_y = 0
        d = 1
        print("width",self.matrix.width)
        print("height", self.matrix.height)
        while True:
            square_x += random.randint(-d,d)
            square_y += random.randint(-d,d)
            square_x += 1
            square_y += 1
            # print("input",square_x,square_y)
            x,y = self.my_mapping(square_x,square_y)
            # print("output",x,y)
            offset_canvas.SetPixel(x, y, 255, 255, 255)
            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
            sleep(.01)

if __name__ == "__main__":
    simple_square = SimpleSquare()
    if (not simple_square.process()):
        simple_square.print_help()