from random import randint, choices

class ColorPallete:

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
                             "modern"]

  def seed(self):
    self.strategy = choices(self.color_strategies, weights=[2, 10, 10, 2, 2, 2, 2, 2])[0]
    self.function = "fixed_options"
    self.color_choices = []
    self.background = self.random_color()
    self.weights = [3, 2, 1]

    if self.strategy == "single_color":
      self.function = self.strategy
      self.color = self.random_color()
    
    if self.strategy == "random_color":
      self.function = self.strategy

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