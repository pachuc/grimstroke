import pygame, pathlib, time, random
from screeninfo import get_monitors
from random import randint
from flow_field import FlowField
from polar import Polar



class PaintingRunner():

  def __init__(self, fullscreen=True, width=None, height=None, config_path=None):
    pygame.init()

    if fullscreen:
      monitor = get_monitors()[0]
      self.width  = monitor.width
      self.height = monitor.height
      screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
      self.width  = width
      self.height = height
      screen = pygame.display.set_mode((width, height))

    self.clock = pygame.time.Clock()

    self.painting_options = [
      FlowField(self.width, self.height, screen, config_path=config_path),
      Polar(self.width, self.height, screen, config_path=config_path),
    ]


  def get_random_painting(self):
    return random.choice(self.painting_options)


  def run(self):
    painting = self.get_random_painting()
    painting.seed_draw_refresh()
    pygame.time.set_timer(42069, 10*1000)

    running = True
    while running:
      self.clock.tick(60)
      
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False

        if event.type == 42069:
          painting = self.get_random_painting()
          painting.seed_draw_refresh()

        if event.type == pygame.KEYDOWN:
          
          if event.key == pygame.K_ESCAPE:
            running = False
          
          if event.key == pygame.K_s:
            painting.save()

      pygame.event.clear()

    pygame.quit()