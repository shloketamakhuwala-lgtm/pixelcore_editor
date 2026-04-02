import numpy as np


class PixelGrid:

    def __init__(self, width, height, color=(255,255,255)):

        self.width = width
        self.height = height

        self.matrix = np.zeros((height,width,3),dtype=np.uint8)
        self.matrix[:] = color

    def set_pixel(self,x,y,color):

        r,g,b = color
        self.matrix[y,x] = [r,g,b]

    def get_pixel(self,x,y):

        return tuple(self.matrix[y,x])

    def data(self):

        return self.matrix
