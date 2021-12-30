import pygame, pathlib, time
from screeninfo import get_monitors
from abc import ABC, abstractmethod

from color_palette import ColorPalette


class Painting(ABC):

  def __init__(self, fullscreen=True, width=None, height=None):
    pygame.init()

    if fullscreen:
      monitor = get_monitors()[0]
      self.width  = monitor.width
      self.height = monitor.height
      self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
      self.width  = width
      self.height = height
      self.screen = pygame.display.set_mode((width, height))
    
    self.color_palette = ColorPalette()
    self.clock = pygame.time.Clock()

  @abstractmethod
  def get_config(self):
    pass

  @abstractmethod
  def seed(self):
    pass

  @abstractmethod
  def draw(self):
    pass
  
  @abstractmethod
  def run(self):
    pass

  def refresh(self):
    pygame.display.flip()

  def save(self):
    current_time = time.time()
    current_path = pathlib.Path(__file__).parent.resolve()
    filename_png = f"{current_path}/saved_images/{current_time}.png"
    filename_txt = f"{current_path}/saved_images/{current_time}.txt"
    f = open(filename_png, "x")
    f.close()
    pygame.image.save(self.screen, filename_png)
    f = open(filename_txt, "x")
    f.write(str(self.get_config()))
    f.close()

  