import numpy as np
from tkinter import filedialog
from PIL import Image


class PixelGrid:

    def __init__(self, width, height, background=(255,255,255)):

        self.width = width
        self.height = height

        self.matrix = np.zeros((height,width,3),dtype=np.uint8)
        self.matrix[:] = background 

    def get_pixel(self,x,y):

        return tuple(self.matrix[y,x])

    def set_pixel(self,x,y,color):

        r,g,b = color
        self.matrix[y,x] = [r,g,b]

    def fill(self,color):

        r,g,b = color
        self.matrix[:] = [r,g,b]

    def load_image(self,image):

        self.matrix = np.array(image)

        self.height,self.width,_ = self.matrix.shape

    def data(self):

        return self.matrix
    def save_image(self):

     path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg"),
            ("All Files", "*.*")
        ]
    )

     if not path:
        return

     matrix = self.matrix

     img = Image.fromarray(matrix)

     img.save(path)