import pygame, math
from random import randint, random

from painting import Painting

class Flower(Painting):


  def __init__(self, fullscreen=True, width=None, height=None, config_path=None):
    super().__init__(fullscreen, width, height, config_path)

  
  def seed(self):
    self.color_palette.seed()

  def get_config(self):
    return None

  def draw(self):
    self.screen.fill((0, 0, 0))
    pygame.draw.circle(self.screen, self.color_palette.get_background(), (self.width//2, self.height//2), self.width//8, 0)
