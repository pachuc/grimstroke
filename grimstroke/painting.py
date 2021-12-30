import pygame, pathlib, time
from screeninfo import get_monitors
from abc import ABC, abstractmethod
from ast import literal_eval

from color_palette import ColorPalette


class Painting(ABC):

  def __init__(self, fullscreen=True, width=None, height=None, config_path=None):
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
    self.refresh()

  def run(self):
    self.seed_draw_refresh()
    pygame.time.set_timer(42069, 10*1000)

    running = True
    while running:
      self.clock.tick(60)
      
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False

        if event.type == 42069:
          self.seed_draw_refresh()

        if event.type == pygame.KEYDOWN:
          
          if event.key == pygame.K_ESCAPE:
            running = False
          
          if event.key == pygame.K_s:
            self.save()

      pygame.event.clear()

    pygame.quit()

  