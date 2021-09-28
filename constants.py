import pygame
from queue import PriorityQueue

width, height = 500, 500
rows, cols = 50, 50
square_size = width//cols
red = (255, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
blue = (0, 160, 250)
gray = (128, 128, 128)
orange = (255, 165, 0)
maze = [[0 for i in range(50)] for j in range(50)]
