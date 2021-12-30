import pygame, math
from random import randint, random
from perlin_noise import PerlinNoise

from painting import Painting


class FlowField(Painting):

  def __init__(self, fullscreen=True, width=None, height=None):
    super().__init__(fullscreen, width, height)

    self.left_x        = int(self.width * -0.5)
    self.right_x       = int(self.width * 1.5)
    self.top_y         = int(self.height * -0.5)
    self.bottom_y      = int(self.height * 1.5)
    self.resolution    = int(self.width * 0.01)
    self.num_columns   = int((self.right_x - self.left_x) / self.resolution)
    self.num_rows      = int((self.bottom_y - self.top_y) / self.resolution)
    self.grid          = [[0 for col in range(self.num_columns)] for row in range(self.num_rows)]

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
  
  def random_thickness(self):
    return self.biased_rand_int(1, self.max_thickness, 10, min)

  def random_steps(self):
    return randint(10, 100)

  def random_gap(self):
    return self.biased_rand_int(1, self.max_gap, 5, min)

  def random_radius(self):
    return (random() * self.resolution)
  
  def random_circle_thickness(self):
    return randint(1, 10)
  
  def round_angle(self, angle):
    to = math.pi/self.rounding_factor
    return round(angle / to) * to
  
  def get_config(self):
    config = {}
    attributes = ["width",
                  "height",
                  "max_thickness", 
                  "max_gap", 
                  "thickness", 
                  "num_steps", 
                  "gap", 
                  "rounding_factor", 
                  "radius", 
                  "circle_thickness",
                  "static_thickness",
                  "static_steps",
                  "static_gap",
                  "should_round",
                  "include_circles",
                  "only_circles",
                  "static_radius",
                  "filled_circles",
                  "static_circle_thickness",
                  "non_overlapping_circles",
                  "use_random_angles",
                  "use_random_height",
                  "use_random_points",
                  "use_same_points",
                  "num_points"]
    for a in attributes:
      config[a] = getattr(self, a)
    config["color_palette"] = self.color_palette.get_config()
    return config
  
  def seed(self):
    self.color_palette.seed()
    self.background = self.color_palette.get_background()
    self.max_thickness = randint(20, 100)
    self.max_gap       = randint(20, 100)
    self.thickness = self.random_thickness()
    self.num_steps = self.random_steps()
    self.gap = self.random_gap()
    self.rounding_factor = randint(2, 10)
    self.radius = self.random_radius()
    self.circle_thickness = self.random_circle_thickness()

    self.static_thickness = self.coin_flip()
    self.static_steps = self.coin_flip()
    self.static_gap = self.coin_flip()
    self.should_round = self.coin_flip()
    self.include_circles = self.coin_flip(4)
    self.only_circles = self.coin_flip()
    self.static_radius = self.coin_flip()
    self.filled_circles = self.coin_flip(4)
    self.static_circle_thickness = self.coin_flip()
    self.non_overlapping_circles = self.coin_flip()
    self.use_random_angles = self.coin_flip(10)
    self.use_random_height = self.coin_flip()
    self.use_random_points = self.coin_flip(10)
    self.use_same_points = self.coin_flip(10)
    self.num_points = randint(20, 500)

  def refresh_grid(self):
    if self.use_random_angles:
      scalar = randint(1, 2)
      for row in range(0, self.num_rows):
        for col in range(0, self.num_columns):
          angle = random() * scalar * math.pi
          if self.should_round:
            angle = self.round_angle(angle)
          self.grid[row][col] = angle
    else:
      noise = PerlinNoise()
      for row in range(0, self.num_rows):
        for col in range(0, self.num_columns):
          scaled_x = col * 0.005
          scaled_y = row * 0.005
          noise_val = noise([scaled_x, scaled_y])
          angle = noise_val * 2 * math.pi
          if self.should_round:
            angle = self.round_angle(angle)
          self.grid[row][col] = angle
  
  def draw_curve(self, x, y):
    if not self.static_steps:
      self.num_steps = self.random_steps()

    for n in range(0, self.num_steps):
      x_offset = x - self.left_x
      y_offset = y - self.top_y

      col = int(x_offset/self.resolution)
      row = int(y_offset/self.resolution)

      if row >= 0 and row < len(self.grid) and col >= 0 and col < len(self.grid[0]):
        ang = self.grid[row][col]
      else:
        break
    
      x_diff = math.cos(ang) * self.resolution
      y_diff = math.sin(ang) * self.resolution

      end_x = x + x_diff
      end_y = y + y_diff

      self.color = self.color_palette.get_color()
      
      if not self.static_thickness:
        self.thickness = self.random_thickness()
      
      if not self.static_radius:
        self.radius = self.random_radius()
      elif self.non_overlapping_circles:
        self.radius = self.resolution/2

      if self.filled_circles:
        self.circle_thickness = 0
      elif not self.static_circle_thickness:
        self.circle_thickness = self.random_circle_thickness()

      if self.include_circles:
        if self.only_circles:
          pygame.draw.circle(self.screen, self.color, (x, y), self.radius, self.circle_thickness)
        else:
          if self.coin_flip():
            pygame.draw.circle(self.screen, self.color, (x, y), self.radius, self.circle_thickness)
          else:
            pygame.draw.line(self.screen, self.color, (x, y), (end_x, end_y), self.thickness)
      else:
        pygame.draw.line(self.screen, self.color, (x, y), (end_x, end_y), self.thickness)

      x = end_x
      y = end_y

  def draw_flow_field(self):
    for row in range(0, len(self.grid)):
      for col in range(0, len(self.grid[0])):
        ang = self.grid[row][col]
        x_diff = math.cos(ang) * (self.resolution/3)
        y_diff = math.sin(ang) * (self.resolution/3)
        x = self.left_x + (col * self.resolution)
        y = self.top_y + (row * self.resolution)
        start_x = x - x_diff
        start_y = y - y_diff
        end_x = x + x_diff
        end_y = y + y_diff
        pygame.draw.line(self.screen, 'red', (start_x, start_y), (end_x, end_y), 1)

  def draw(self):
    self.seed()
    self.refresh_grid()
    self.screen.fill(self.background)

    if self.use_random_points:
      # all random
      for i in range(0, self.num_points):
        x = randint(0, self.width)
        y = randint(0, self.height)
        self.draw_curve(x, y)

    elif self.use_same_points:
      # linear matching points
      i = randint(0, min(self.width, self.height))
      while i < self.width and i < self.height:
        if self.coin_flip():
          self.draw_curve(i, i)
     
        if not self.static_gap:
          self.gap = self.random_gap()
        i += self.gap

    elif self.use_random_height:
      #itterate through width
      # pick random height
      i = 0
      while i < self.width:
        if self.coin_flip():
          j = randint(0, self.height)
          self.draw_curve(i, j)
     
        if not self.static_gap:
          self.gap = self.random_gap()
        i += self.gap

    else:
      # itterate through height
      # pick random width
      i = 0
      while i < self.height:
        if self.coin_flip():
          j = randint(0, self.width)
          self.draw_curve(j, i)
     
        if not self.static_gap:
          self.gap = self.random_gap()
        i += self.gap
  