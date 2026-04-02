import pygame
import numpy as np


class GPURenderer:

    def __init__(self,width,height,scale=4):

        pygame.init()

        self.scale = scale
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode(
            (width*scale,height*scale),
            pygame.DOUBLEBUF
        )

        pygame.display.set_caption("PixelCore GPU Engine")

    def draw(self,pixel_matrix):

        surf = pygame.surfarray.make_surface(
            np.transpose(pixel_matrix,(1,0,2))
        )

        surf = pygame.transform.scale(
            surf,
            (self.width*self.scale,self.height*self.scale)
        )

        self.window.blit(surf,(0,0))

        pygame.display.flip()

    def get_pixel_from_mouse(self):

        mx,my = pygame.mouse.get_pos()

        x = mx//self.scale
        y = my//self.scale

        return x,y
