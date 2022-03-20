import pygame, pathlib, time
from abc import ABC, abstractmethod
from ast import literal_eval

from color_palette import ColorPalette
from random import randint
import datetime


class Painting(ABC):

  def __init__(self, width, height, screen, config_path=None):
    self.width = width
    self.height = height
    self.screen = screen

    self.color_palette = ColorPalette()
    self.clock = pygame.time.Clock()

    if config_path:
      f = open(config_path, "r")
      config_text = f.read()
      f.close()
      self.config = literal_eval(config_text)
      self.use_config()
    else:
      self.config = None

  @abstractmethod
  def get_config(self):
    pass

  def use_config(self):
    for k in self.config.keys():
      if k == "width" or k == "height":
        continue

      if k == "color_palette":
        self.color_palette.use_config(self.config[k])
      else:
        setattr(self, k, self.config[k])

  @abstractmethod
  def seed(self):
    pass

  @abstractmethod
  def draw(self):
    pass

  def coin_flip(self, num_choices=2):
    flip = randint(1, num_choices)
    if flip == 1:
      return True
    else:
      return False
  
  
  def biased_rand_int(self, mn, mx, rolls, f):
    r = []
    for i in range(0, rolls):
      r.append(randint(mn, mx))
    return f(r)

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
  
  def seed_draw_refresh(self):
    if self.config is None:
      self.seed()
    self.draw()
    self.write_text()
    self.refresh()

  def write_text(self):
    t = datetime.datetime.now()

    if t.month == 1 and t.day == 29:
      self.render_text(" Happy Anniversary! ")

    if t.month == 2 and t.day == 14:
      self.render_text(" pachu <3 divya ")
    
    if t.month == 3 and t.day == 25:
      self.render_text(" Happy Birthday Divya! ")

    
  def render_text(self, message):
    text_size = 100
    font = pygame.font.Font(pygame.font.match_font('sfcompacttext'), text_size)
    text_color = self.color_palette.get_background()
    text = font.render(message, True, text_color, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (self.width//2, self.height//2)
    self.screen.blit(text, textRect)
  