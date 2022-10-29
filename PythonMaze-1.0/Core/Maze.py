from Core.Node import Node
from pygame.locals import *
from random import randint
import math

import pygame
import json

class Maze(object):

    def __init__(self, file_name):
        self.solved = False
        self.__str = ""
        self.__load_file("test1.txt")
      
    def __load_file(self, fname):
        with open(fname) as f:
            #content = f.readlines()
            self.length, self.width = [int(x) for x in next(f).split()]
            self.height = 1
            self.map = [None] * self.height
            self.tile_color = [None] * self.height
            self.map[0] = [None] * self.length
            self.tile_color[0] = [None] * self.length
            for i in range(0, self.length):
                self.map[0][i] = [None] * self.width
                self.tile_color[0][i] = [None] * self.width
                line = next(f)
                for j in range(0, self.width):
                    self.tile_color[0][i][j] = 0
                    c = line[j] 
                    if c in '0123456789':
                        self.map[0][i][j] = int(c)
                    else:
                        self.map[0][i][j] = c
                        if c == 'S':
                            self.start_node = Node(0, i, j, self, None)
                        elif c == 'E':
                            self.end_node = Node(0, i, j, self, None)


    def reset_colors(self):
        for i in range(0, self.height):
            for j in range(0, self.length):
                for k in range(0, self.width):
                    self.tile_color[i][j][k] = 0

    #Drawing the map into the GUI
    def draw(self,display_surf,wall_surf, stairs_surf, start_surf, end_surf, floor_surf):
        tile_size = 27
        number_font = pygame.font.SysFont("monospace", 18, True)
        text_font = pygame.font.SysFont("monospace", 18, True)
        #top floor seperator
        for k in range(0, self.width * self.height + self.height + 1):
            display_surf.blit(floor_surf,(k * tile_size, 0))

        for k in range(0, self.height): #repeated for number of floors
            for i in range(0, self.length): #repeated for floor length
                #displaying the floor seperator between each floor
                display_surf.blit(floor_surf,(k * tile_size * (self.width + 1) , (i + 1) * tile_size))
                for j in range(0,self.width): #repeated for floor width
                    if not(isinstance(self.map[k][i][j], int)): #if not an empty space which can be traversed
                        tile = None
                        if self.map[k][i][j] == '#': #wall
                            tile = wall_surf
                        elif self.map[k][i][j] == 'A': #stairs
                            tile = stairs_surf
                        elif self.map[k][i][j] == 'S': #start tile
                            tile = start_surf
                            self.start_node = Node(k,i,j,self,None)
                        elif self.map[k][i][j] == 'E': #end tile
                            tile = end_surf
                            self.end_node = Node(k,i,j,self,None)
                        display_surf.blit(tile,((j + k * self.width + k + 1) * tile_size, (i + 1) * tile_size))
                    else:
                        if self.tile_color[k][i][j] == 0:
                            font_colour = (255, 255, 255)
                        elif self.tile_color[k][i][j] == 1:
                            font_colour = (255, 255, 0)
                        elif self.tile_color[k][i][j] == 2:
                            font_colour = (100, 100, 255)
                        elif self.tile_color[k][i][j] == 3:
                            font_colour = (255, 0, 255)
                        elif self.tile_color[k][i][j] == 4:
                            font_colour = (0, 255, 255)

                        tile_label = number_font.render(str(self.map[k][i][j]), 1, font_colour)
                        display_surf.blit(tile_label, ((j + k * self.width + k + 1) * tile_size + 5, (i + 1) * tile_size + 5))
                        cost_label = text_font.render(self.__str, 1, (255, 255, 255)) #displaying final cost
                        display_surf.blit(cost_label, (10, (self.length + 8) * tile_size))
                            
                    j = j + 1
                if k == (self.height - 1): #if last floor, print the final floor sperator
                    display_surf.blit(floor_surf,((j + k * self.width + k + 1) * tile_size, (i + 1) * tile_size))
                i = i + 1
        
        #bottom floor seperator
        for k in range(0, self.width * self.height + self.height + 1):
            display_surf.blit(floor_surf,(k * tile_size, (self.length + 1) * tile_size))
        guide_label = text_font.render("Press 1 for DFS, 2 for BFS, 3 for UCS,", 1, (255, 255, 255))
        display_surf.blit(guide_label, (10, (self.length + 2) * tile_size))
        guide_label = text_font.render("4 for A* with h = Manhattan Distance, 5 for A* with h = Euclidean distance,", 1, (255, 255, 255))
        display_surf.blit(guide_label, (10, (self.length + 3) * tile_size))
        guide_label = text_font.render("6 for greedy with h = Manhattan Distance, 7 for greedy with h = Euclidean distance", 1, (255, 255, 255))
        display_surf.blit(guide_label, (10, (self.length + 4) * tile_size))

    def print(self, str):
        self.__str = str

