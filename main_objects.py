import pygame
class character:
  def __init__(self, type):
    self.type = type
    if type == "boss":
      self.X = 350
      self.Y = 50
      self.movementX = 0.3
      self.movementy = 0.3
    if type == "hero":
      self.X = 400
      self.Y = 500
      self.movementX = 0
      self.movementy = 0

