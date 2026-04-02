import pygame
import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image


class GPUPixelEditor:

    def __init__(self,width=256,height=256,scale=4):

        pygame.init()

        self.width = width
        self.height = height
        self.scale = scale

        self.window = pygame.display.set_mode((width*scale,height*scale))
        pygame.display.set_caption("PixelCore GPU Editor")

        self.pixels = np.zeros((height,width,3),dtype=np.uint8)
        self.pixels[:] = [255,255,255]

        self.selected_color = [0,0,0]

    # -------------------------

    def open_image(self):

        root = tk.Tk()
        root.withdraw()

        path = filedialog.askopenfilename()

        if not path:
            return

        img = Image.open(path).convert("RGB")

        img = img.resize((self.width,self.height))

        self.pixels = np.array(img)

    # -------------------------

    def new_canvas(self):

        root = tk.Tk()
        root.withdraw()

        size = simpledialog.askinteger(
            "Canvas Size",
            "Enter canvas size (example 256)"
        )

        if not size:
            return

        self.width = size
        self.height = size

        self.window = pygame.display.set_mode(
            (self.width*self.scale,self.height*self.scale)
        )

        self.pixels = np.zeros((size,size,3),dtype=np.uint8)
        self.pixels[:] = [255,255,255]

    # -------------------------

    def change_color(self):

        root = tk.Tk()
        root.withdraw()

        rgb = simpledialog.askstring(
            "RGB Color",
            "Enter color (example 255,0,0)"
        )

        if not rgb:
            return

        try:
            r,g,b = map(int,rgb.split(","))
            self.selected_color = [r,g,b]
        except:
            pass

    # -------------------------

    def run(self):

        running = True

        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_o:
                        self.open_image()

                    if event.key == pygame.K_n:
                        self.new_canvas()

                    if event.key == pygame.K_c:
                        self.change_color()

                if pygame.mouse.get_pressed()[0]:

                    mx,my = pygame.mouse.get_pos()

                    x = mx // self.scale
                    y = my // self.scale

                    if x < self.width and y < self.height:

                        self.pixels[y,x] = self.selected_color

            surf = pygame.surfarray.make_surface(
                np.transpose(self.pixels,(1,0,2))
            )

            surf = pygame.transform.scale(
                surf,
                (self.width*self.scale,self.height*self.scale)
            )

            self.window.blit(surf,(0,0))

            pygame.display.flip()

        pygame.quit()


# -------------------------

if __name__ == "__main__":

    print("GPU Pixel Editor Controls")
    print("--------------------------")
    print("Mouse Click = Draw Pixel")
    print("O = Open Image")
    print("N = New Canvas")
    print("C = Change Color")
    print("ESC or Close Window = Exit")

    editor = GPUPixelEditor(256,256,4)
    editor.run()