import pygame, math
import numpy as np
from random import randint, random

from painting import Painting

class Polar(Painting):


  def __init__(self, width, height, screen, config_path=None):
    super().__init__(width, height, screen, config_path=config_path)
    self.coordinates = []
    self.thickness = 1
    self.petal_scalar = 1
    self.scalar = 1
    

  
  def get_random_spacing(self, dim):
    # self.biased_rand_int(1, 20, 5, min)
    return (dim // self.biased_rand_int(1, 20, 3, min))
  

  def seed(self):
    self.color_palette.seed()

    self.color = self.color_palette.get_color()
    self.populate_coordinates()
    self.scalar = self.biased_rand_int(25, 500, 3, max)
    self.petal_scalar = self.biased_rand_int(1, 100, 3, min)
    self.thickness = self.biased_rand_int(1, 50, 3, min)


    self.locked = self.coin_flip(2)
    self.changing_color = self.coin_flip(2)

    self.xdiv = self.get_random_spacing(self.width)
    if self.locked:
      self.ydiv = self.xdiv
    else:
      self.ydiv = self.get_random_spacing(self.height)
    


  def get_config(self):
    return None

  def cart2pol(self, x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

  def pol2cart(self, rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)


  def flower_curve(self, theta):
    rho =  self.scalar * math.cos(self.petal_scalar * theta)
    return rho


  def populate_coordinates(self):
    self.coordinates = []
    theta = 0
    while (theta <= 2 * math.pi):
      rho = self.flower_curve(theta)
      self.coordinates.append(self.pol2cart(rho, theta))
      theta += .01

  def render_polar_coords(self, xoffset, yoffset, color):
    i = 0
    j = 1

    while j < len(self.coordinates):
      x1, y1 = self.coordinates[i]
      x2, y2 = self.coordinates[j]
      x1 += xoffset
      x2 += xoffset
      y1 += yoffset
      y2 += yoffset
      if self.changing_color:
        color = self.color_palette.get_color()
      pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), self.thickness)
      i += 1
      j += 1


  def draw(self):
    
    self.screen.fill(self.color_palette.get_background())

    if self.locked:
      for cx in range(0, self.width + self.ydiv, self.ydiv):
        for cy in range(0, self.height + self.ydiv, self.ydiv):
          self.render_polar_coords(cx, cy, self.color_palette.get_color())
    else:
      for cx in range(0, self.width + self.xdiv, self.xdiv):
        for cy in range(0, self.height + self.ydiv, self.ydiv):
          self.render_polar_coords(cx, cy, self.color_palette.get_color())
    

