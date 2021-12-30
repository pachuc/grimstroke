from random import randint, choices

class ColorPalette:

  def __init__(self):
    self.strategy = None
    self.function = None
    self.color = None
    self.background = None
    self.weights = None
    self.color_choices = []
    self.color_strategies = ["random_color", 
                             "single_color", 
                             "fixed_options", 
                             "america",
                             "charcoal",
                             "sunset",
                             "pastel",
                             "modern",
                             "dark_reds",
                             "unsat_dark_reds",
                             "reds",
                             "purples",
                             "easter"]
    
  def use_config(self, config):
    for k in config.keys():
      setattr(self, k, config[k])
    self.strategy_to_function()

  def strategy_to_function(self):
    if self.strategy == "single_color" or self.strategy == "random_color":
      self.function = self.strategy
    else:
      self.function = "fixed_options"

  def seed(self):
    self.strategy = choices(self.color_strategies, weights=[2, 15, 15, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])[0]
    self.strategy_to_function()
    self.color_choices = []
    self.background = self.random_color()
    self.weights = [3, 2, 1]

    if self.strategy == "single_color":
      self.color = self.random_color()

    if self.strategy == "fixed_options":
      self.weights = None
      num_options = randint(1, 10)
      for i in range(0, num_options):
        self.color_choices.append(self.random_color())
    
    if self.strategy == "america":
      self.background = (22, 24, 83)
      self.color_choices.append((41, 44, 109))
      self.color_choices.append((250, 237, 240))
      self.color_choices.append((236, 37, 90))
    
    if self.strategy == "charcoal":
      self.background = (34, 40, 49)
      self.color_choices.append((57, 62, 70))
      self.color_choices.append((0, 173, 181))
      self.color_choices.append((238, 238, 238))
    
    if self.strategy == "sunset":
      self.background = (249, 237, 105)
      self.color_choices.append((240, 138, 93))
      self.color_choices.append((184, 59, 94))
      self.color_choices.append((106, 44, 112))
    
    if self.strategy == "pastel":
      self.background = (243, 129, 129)
      self.color_choices.append((252, 227, 138))
      self.color_choices.append((234, 255, 208))
      self.color_choices.append((149, 225, 211))
    
    if self.strategy == "modern":
      self.background = (8, 217, 214)
      self.color_choices.append((37, 42, 52))
      self.color_choices.append((255, 46, 99))
      self.color_choices.append((234, 234, 234))
    
    if self.strategy == "dark_reds":
      self.background = (43, 46, 74)
      self.color_choices.append((232, 69, 69))
      self.color_choices.append((144, 55, 73))
      self.color_choices.append((83, 53, 74))
    
    if self.strategy == "unsat_dark_reds":
      self.background = (246, 114, 128)
      self.color_choices.append((192, 108, 132))
      self.color_choices.append((108, 91, 123))
      self.color_choices.append((53, 92, 125))

    if self.strategy == "reds":
      self.background = (226, 62, 87)
      self.color_choices.append((136, 48, 78))
      self.color_choices.append((82, 37, 70))
      self.color_choices.append((49, 29, 63))
    
    if self.strategy == "purples":
      self.background = (244, 238, 255)
      self.color_choices.append((220, 214, 247))
      self.color_choices.append((166, 177, 225))
      self.color_choices.append((66, 72, 116))
    
    if self.strategy == "easter":
      self.background = (255, 207, 223)
      self.color_choices.append((254, 253, 202))
      self.color_choices.append((224, 249, 181))
      self.color_choices.append((165, 222, 229))

  def get_config(self):
    config = {}
    attributes = ["strategy", "color", "background", "color_choices", "weights"]
    for a in attributes:
      config[a] = getattr(self, a)
    return config

  def get_background(self):
    return self.background

  def get_color(self):
    function_to_call = getattr(self, self.function)
    return function_to_call()
  
  def random_color(self):
    return (randint(0, 255), randint(0, 255), randint(0, 255))

  def single_color(self):
    return self.color
  
  def fixed_options(self):
    return choices(self.color_choices, weights=self.weights)[0]