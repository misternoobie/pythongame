import pygame
class character:
  def __init__(self, type):
    self.type = type
    if type == "boss":
      image = pygame.image.load('tEm.gif')
      self.image = pygame.transform.scale(image, (75, 75))
      self.X = 350
      self.Y = 50
      self.movementX = 0.3
      self.movementy = 0.3
      print("Enemy Created: ", self.X, " | ", self.Y)
    if type == "hero":
      image = pygame.image.load('ZQjb.gif')
      self.image = pygame.transform.scale(image, (100, 100))
      self.X = 400
      self.Y = 500
      self.movementX = 0
      self.movementY = 0

  def getImage(self):
    return self.image

class weapon:
  def __init__(self, type):
    self.type = type
    if type == "bamboo":
      image = pygame.image.load('bamboo.png')
      self.image = pygame.transform.scale(image, (25, 25))
      self.X = 0
      self.Y = 0
      self.movementX = 0.5
      self.movementY = 2
      self.state = "ready"
      print("Bamboo Created: ", self.X, " | ", self.Y)

  def getImage(self):
    return self.image