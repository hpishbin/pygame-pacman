import pygame
import random
import time

class Ghost:
    NOT_WALLS = [' ', '.', 'O', 'G']
    DIRECTIONS = ['up', 'left', 'down', 'right']
    OPPSITES = {'right': 'left', 'left': 'right', 'down': 'up', 'up': 'down', 'none': 'none'}
    
    def __init__(self, pos, speed, map):
        self.home = pos
        self.pos = pos
        self.animation_pos = [float(pos[0]), float(pos[1])]
        self.speed = speed
        self.map = map
        self.state = 'chase'
        self.counter = 0
        self.import_images()
        self.frighten_mode_duration = 10

    def import_images(self):
        self.images = {}
        for direction in self.DIRECTIONS:
            self.images[direction + '_1'] = pygame.image.load('images/ghosts/' +  self.name + '/' + direction + '_1.png')
            self.images[direction + '_2'] = pygame.image.load('images/ghosts/' +  self.name + '/' + direction + '_2.png')
            self.images['dead_' + direction] = pygame.image.load('images/ghosts/dead/' + direction + '.png')
        self.images['frightened_1'] = pygame.image.load('images/ghosts/frightened/frightened_1.png')
        self.images['frightened_2'] = pygame.image.load('images/ghosts/frightened/frightened_2.png')
        self.images['frightened_3'] = pygame.image.load('images/ghosts/frightened/frightened_3.png')
        self.images['frightened_4'] = pygame.image.load('images/ghosts/frightened/frightened_4.png')
        

    def move(self, target):
        #portal exception
        if self.pos[0] < -1:
            self.pos[0] = len(self.map[0]) - 1
            self.animation_pos[0] = float(len(self.map[0]))
        elif self.pos[0] > len(self.map[0])-1:
            self.pos[0] = 0
            self.animation_pos[0] = float(-1)
        
        #home exception
        if self.map[self.pos[1]][self.pos[0]] == 'G': target = [len(self.map[0])//2, 0]

        if self.state == 'dead': target = self.home

        if self.pos[0] < len(self.map[0]) - 1 and self.map[self.pos[1]][self.pos[0]] == 'G':
            home = True
            if self.state == 'dead': self.state = 'chase'
        else: home = False

        if self.state == 'frightened':
            ways = []
            for way in self.ways(self.pos):
                if way[0] != self.OPPSITES[self.direction] or home:
                    ways.append(way)
            way = ways[random.randint(0, len(ways)-1)]
            self.direction = way[0]
            self.pos = way[1:]
        
        else:
            best_way = [float('inf'), [self.direction, self.pos[0], self.pos[1]]]
            for way in self.ways(self.pos):
                if way[0] != self.OPPSITES[self.direction] or home:
                    distance2 = ((way[1] - target[0]) ** 2 + (way[2] - target[1]) ** 2)
                    if distance2 < best_way[0]:
                        best_way = [distance2, way]
                    if distance2 == best_way[0] and self.DIRECTIONS.index(way[0]) < self.DIRECTIONS.index(best_way[1][0]):
                        best_way = [distance2, way]
            self.direction = best_way[1][0]
            self.pos = best_way[1][1:]

        #portal exception



    def ways(self, pos):
        NOT_WALLS = self.NOT_WALLS[:]
        ways = []
        #portal exception
        if self.pos[0] >= len(self.map[0])-1:
            ways.append(['right', pos[0] + 1, pos[1]])
            ways.append(['left', pos[0] - 1, pos[1]])
            return ways
        
        # #home exceptions
        if self.map[pos[1]][pos[0]] == 'G' or self.state == 'dead': NOT_WALLS.append('_')

        if self.map[pos[1]][pos[0] + 1] in NOT_WALLS:
            ways.append(['right', pos[0] + 1, pos[1]])
        if self.map[pos[1]][pos[0] - 1] in NOT_WALLS:
            ways.append(['left', pos[0] - 1, pos[1]])
        if self.map[pos[1] + 1][pos[0]] in NOT_WALLS:
            ways.append(['down', pos[0], pos[1] + 1])
        if self.map[pos[1] - 1][pos[0]] in NOT_WALLS:
            ways.append(['up', pos[0], pos[1] - 1])
        return ways
    
    def smooth_move(self, target):
        # self.counter += 1

        if not self.animation_pos[0].is_integer() or int(self.animation_pos[0]) != self.pos[0]:
            if self.animation_pos[0] > self.pos[0]:
                self.animation_pos[0] -= self.speed
            elif self.animation_pos[0] < self.pos[0]:
                self.animation_pos[0] += self.speed
            self.animation_pos[0] = round(self.animation_pos[0], 2)
        if not self.animation_pos[1].is_integer() or int(self.animation_pos[1]) != self.pos[1]:
            if self.animation_pos[1] > self.pos[1]:
                self.animation_pos[1] -= self.speed
            elif self.animation_pos[1] < self.pos[1]:
                self.animation_pos[1] += self.speed
            self.animation_pos[1] = round(self.animation_pos[1], 2)
        
        if (self.counter * self.speed).is_integer(): self.move(target)
    
    def get_ghost(self):
        self.counter += 1

        if self.state == 'frightened':
            if time.time() - self.frighten_time > self.frighten_mode_duration:
                self.state = 'chase'
                self.speed = self.speed * 2
                #for ghost lags when speed is doubled
                self.animation_pos = [round(self.animation_pos[0], 1), round(self.animation_pos[1], 1)]
            elif time.time() - self.frighten_time > 7/10 * self.frighten_mode_duration:
                return {'pos': self.animation_pos, 'image': self.images['frightened_' + str(int(self.counter * self.speed * 2) % 4 + 1)]}
            return {'pos': self.animation_pos, 'image': self.images['frightened_' + str(int(self.counter * self.speed) % 2 + 1)]}
        elif self.state == 'dead':
            return {'pos': self.animation_pos, 'image': self.images['dead_' + self.direction]}
        return {'pos': self.animation_pos, 'image': self.images[self.direction + '_' + str(int(self.counter * self.speed) % 2 + 1)]}
    
    def frighten(self):
        if self.state == 'dead': return
        elif self.state != 'frightened': self.speed = self.speed / 2
        self.state = 'frightened'
        self.direction = self.OPPSITES[self.direction]
        self.frighten_time = time.time()
    
    def die(self):
        self.state = 'dead'
        self.speed = self.speed * 2
        
        #for ghost lags when speed is doubled, second prameter depends on the speed of the ghost
        self.animation_pos = [round(self.animation_pos[0], 1), round(self.animation_pos[1], 1)]


class Blinky(Ghost):
    def __init__(self, pos, speed, map, home=None):
        self.name = 'Blinky'
        self.direction = 'left'
        super().__init__(pos, speed, map)
        if home: self.home = home


class Pinky(Ghost):
    def __init__(self, pos, speed, map):
        self.name = 'Pinky'
        self.direction = 'up'
        super().__init__(pos, speed, map)  

    def smooth_move(self, pacman_pos, pacman_direction):
        target = pacman_pos
        if pacman_direction == 'right':
            target = [pacman_pos[0] + 4, pacman_pos[1]]
        elif pacman_direction == 'left':
            target = [pacman_pos[0] - 4, pacman_pos[1]]
        elif pacman_direction == 'up':
            target = [pacman_pos[0] - 4, pacman_pos[1] - 4]
        elif pacman_direction == 'down':
            target = [pacman_pos[0], pacman_pos[1] + 4]
        return super().smooth_move(target)


class Inky(Ghost):
    def __init__(self, pos, speed, map):
        self.name = 'Inky'
        self.direction = 'up'
        super().__init__(pos, speed, map)

    def smooth_move(self, pacman_pos, blinky_pos):
        target = []
        target.append(pacman_pos[0] + (pacman_pos[0] - blinky_pos[0]))
        target.append(pacman_pos[1] + (pacman_pos[1] - blinky_pos[1]))
        
        # debug = super().smooth_move(target)
        # return{'pos': target, 'image': debug['image']}
        return super().smooth_move(target)


class Clyde(Ghost):
    def __init__(self, pos, speed, map):
        self.name = 'Clyde'
        self.direction = 'up'
        super().__init__(pos, speed, map)
    
    def smooth_move(self, pacman_pos):
        if abs(pacman_pos[0] - self.pos[0])**2 + abs(pacman_pos[1] - self.pos[1])**2 >= 64:
            return super().smooth_move(pacman_pos)
        else:
            return super().smooth_move(self.home)