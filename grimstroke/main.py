import sys, pygame, math, random
from random import randint
from screeninfo import get_monitors
from perlin_noise import PerlinNoise


class Painting:

  def __init__(self):
    pygame.init()
    monitor = get_monitors()[0]

    self.width         = monitor.width
    self.height        = monitor.height
    self.screen        = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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


  def random_color(self):
    return (randint(0, 255), randint(0, 255), randint(0, 255))
  
  def random_thickness(self):
    return self.biased_rand_int(1, self.max_thickness, 10, min)

  def random_steps(self):
    return randint(10, 100)

  def random_gap(self):
    return self.biased_rand_int(0, self.max_gap, 5, min)

  def random_radius(self):
    return (random.random() * self.resolution)
  
  def random_circle_thickness(self):
    return randint(0, 10)
  

  def seed(self):
    self.background = self.random_color()
    self.color = self.random_color()
    self.max_thickness = randint(20, 100)
    self.max_gap       = randint(20, 100)
    self.thickness = self.random_thickness()
    self.num_steps = self.random_steps()
    self.gap = self.random_gap()
    self.rounding_factor = randint(2, 10)
    self.radius = self.random_radius()
    self.circle_thickness = self.random_circle_thickness()

    self.static_color = self.coin_flip()
    self.static_thickness = self.coin_flip()
    self.static_steps = self.coin_flip()
    self.static_gap = self.coin_flip()
    self.should_round = self.coin_flip()
    self.include_circles = self.coin_flip(4)
    self.only_circles = self.coin_flip()
    self.static_radius = self.coin_flip()
    self.filled_circles = self.coin_flip(4)
    self.static_circle_thickness = self.coin_flip()


    self.num_points = randint(20, 500)


  def round_angle(self, angle):
    to = math.pi/self.rounding_factor
    return round(angle / to) * to


  def refresh_grid(self):
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

      if not self.static_color:
        self.color = self.random_color()
      
      if not self.static_thickness:
        self.thickness = self.random_thickness()
      
      if not self.static_radius:
        self.radius = self.random_radius()

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
      
      #self.elements.append(elm)
      x = end_x
      y = end_y


  def draw_flow_field(self):
    for row in range(0, len(grid)):
      for col in range(0, len(grid[0])):
        ang = grid[row][col]
        x_diff = math.cos(ang) * (resolution/3)
        y_diff = math.sin(ang) * (resolution/3)
        x = left_x + (col * resolution)
        y = top_y + (row * resolution)
        start_x = x - x_diff
        start_y = y - y_diff
        end_x = x + x_diff
        end_y = y + y_diff
        pygame.draw.line(screen, 'red', (start_x, start_y), (end_x, end_y), 1)


  def draw(self):
    self.seed()
    self.refresh_grid()
    self.screen.fill(self.background)

    i = 0
    while i < self.width:
     if self.coin_flip():
       j = randint(0, self.height)
       self.draw_curve(i, j)
     
     if not self.static_gap:
       self.gap = self.random_gap()
    
     i += self.gap

    # for i in range(0, self.num_points):
    #   x = randint(0, self.width)
    #   y = randint(0, self.height)
    #   self.draw_curve(x, y)

  
  def refresh(self):
    pygame.display.flip()


  def run(self):
    self.draw()
    self.refresh()

    while 1:
      for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RETURN:
            self.draw()
            self.refresh()
          
          if event.key == pygame.K_ESCAPE:
            sys.exit()
      
      pygame.event.clear()


p = Painting()
p.run()