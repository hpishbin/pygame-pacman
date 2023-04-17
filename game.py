import pygame
import random
import ghost

class Game:
    def __init__(self, map, pacman_pos):
        self.map = map
        self.start_pos = pacman_pos
        self.pacman_pos = pacman_pos
        self.direction = 'none'
        self.SPEED = 0.1
        self.score = 0
        self.lives_amount = 3
        self.lives = self.lives_amount
        self.ghosts = []
        self.add_ghosts()
        self.import_images()
        self.counter = 0
        self.lock = False

    def add_ghosts(self):
        self.ghosts.append(ghost.Blinky([9, 8], self.SPEED, self.map, [9, 10]))
        self.ghosts.append(ghost.Clyde([8, 10], self.SPEED, self.map))
        self.ghosts.append(ghost.Pinky([9, 10], self.SPEED, self.map))
        self.ghosts.append(ghost.Inky([10, 10], self.SPEED, self.map))
    
    def import_images(self):
        self.images = {}
        for direction in ['left', 'right', 'up', 'down']:
            self.images[direction + '_open'] = pygame.image.load('images/pacman/' + direction + '_open.png')
            self.images[direction + '_closed'] = pygame.image.load('images/pacman/' + direction + '_closed.png')
        self.images['moon'] = pygame.image.load('images/pacman/moon.png')
        for i in range(1, 12):
            self.images['dead_' + str(i)] = pygame.image.load('images/pacman/dead/dead_' + str(i) + '.png')
        self.images['now'] = self.images['moon']
        self.images['pacman'] = self.images['right_closed']
    def move(self, keys):
        NOT_WALLS = [' ', '.', 'O']
        if self.lock: return
        location = self.pacman_pos
        new_direction = 'none'
        tmploc = self.advanced_round(self.pacman_pos)


        if keys[pygame.K_RIGHT] or keys[pygame.K_d] or self.direction == 'right':
            #portal exception:
            if tmploc[0] >= len(self.map[0]) - 1:
                if self.direction != 'right': new_direction = 'right'
            elif float(tmploc[1]).is_integer() and self.map[tmploc[1]][int(tmploc[0] + self.SPEED)+1] in NOT_WALLS:
                if self.direction != 'right': new_direction = 'right'
            else: location[0] = round(location[0])
        if keys[pygame.K_LEFT] or keys[pygame.K_a] or self.direction == 'left':
            if float(tmploc[1]).is_integer() and self.map[tmploc[1]][int(tmploc[0] - self.SPEED)] in NOT_WALLS:
                if self.direction != 'left': new_direction = 'left'
            else: location[0] = round(location[0])
        if keys[pygame.K_DOWN] or keys[pygame.K_s] or self.direction == 'down':
            #portal exception:
            if tmploc[0] >= len(self.map[0]) - 1: pass
            elif float(tmploc[0]).is_integer() and self.map[int(tmploc[1] + self.SPEED)+1][tmploc[0]] in NOT_WALLS:
                if self.direction != 'down': new_direction = 'down'
            else: location[1] = round(location[1])
        if keys[pygame.K_UP] or keys[pygame.K_w] or self.direction == 'up':
            #portal exception:
            if tmploc[0] >= len(self.map[0]) - 1: pass
            elif float(tmploc[0]).is_integer() and self.map[int(tmploc[1] - self.SPEED)][tmploc[0]] in NOT_WALLS:
                if self.direction != 'up': self.direction = 'up'
            else: location[1] = round(location[1])
        location = [round(location[0], 2), round(location[1], 2)]
        
        if new_direction == 'none': new_direction = self.direction
        if new_direction == 'right':
            location[0] += self.SPEED
            self.direction = 'right'
        if new_direction == 'left':
            location[0] -= self.SPEED
            self.direction = 'left'
        if new_direction == 'down':
            location[1] += self.SPEED
            self.direction = 'down'
        if new_direction == 'up':
            location[1] -= self.SPEED
            self.direction = 'up'
        
        #portal:
        if location[0] <= -1: location[0] = len(self.map[0])
        elif location[0] >= len(self.map[0]): location[0] = -1

        self.pacman_pos = location
    
    def get_packman(self):
        self.counter += 1
        if self.counter < 55 and self.lock:
            self.images['now'] = self.images['dead_' + str(int(self.counter / 5) + 1)]
        elif self.counter == 55 and self.lock:
            if self.lives != 0: self.lock = False
            self.pacman_pos = self.start_pos
        elif self.counter % 5 == 0:
            if self.direction == 'none':
                self.images['now'] = self.images['moon']
            elif self.images['now'] == self.images[self.direction + '_open']:
                self.images['now'] = self.images[self.direction + '_closed']
            elif self.images['now'] == self.images[self.direction + '_closed']:
                self.images['now'] = self.images['moon']
            else:
                self.images['now'] = self.images[self.direction + '_open']
        
        return {'pos': self.pacman_pos, 'image': self.images['now']}    
    
    def advanced_round(self, input):
        output = list(tuple(input))
        if round(abs(input[0] - round(input[0])), 2) < 0.3: output[0] = round(input[0])
        if round(abs(input[1] - round(input[1])), 2) < 0.3: output[1] = round(input[1])
        return output
    
    def collision_check(self):
        for ghost in self.ghosts:
            if [round(self.pacman_pos[0]), round(self.pacman_pos[1])] == [round(ghost.animation_pos[0]), round(ghost.animation_pos[1])]:
                if ghost.state == 'dead': pass
                elif ghost.state == 'frightened':
                    ghost.die()
                    self.killed_ghosts += 1
                    self.score += 2**self.killed_ghosts * 100
                else:
                    self.replay()


        if round(self.pacman_pos[0]) >= len(self.map[0]): pass      #portal exception
        elif self.map[round(self.pacman_pos[1])][round(self.pacman_pos[0])] == 'O':
            self.map[round(self.pacman_pos[1])][round(self.pacman_pos[0])] = ' '
            for ghost in self.ghosts: ghost.frighten()
            self.killed_ghosts = 0
        elif self.map[round(self.pacman_pos[1])][round(self.pacman_pos[0])] == '.':
            self.map[round(self.pacman_pos[1])][round(self.pacman_pos[0])] = ' '
            self.score += 10

    def get_ghosts(self):
        response = []
        for ghost in self.ghosts:
            if ghost.name == 'Blinky':
                if self.direction != 'none': ghost.smooth_move(self.pacman_pos)
                response.append(ghost.get_ghost())
                blinky = ghost
            elif ghost.name == 'Pinky':
                if self.direction != 'none': ghost.smooth_move(self.pacman_pos, self.direction)
                response.append(ghost.get_ghost())
            elif ghost.name == 'Inky':
                if self.direction != 'none': ghost.smooth_move(self.pacman_pos, blinky.pos)
                response.append(ghost.get_ghost())
            elif ghost.name == 'Clyde':
                if self.direction != 'none': ghost.smooth_move(self.pacman_pos)
                response.append(ghost.get_ghost())
        return response
    
    def replay(self):
        # self.pacman_pos = self.start_pos
        self.lives -= 1
        self.counter = 0
        self.lock = True
        self.ghosts = []
        self.add_ghosts()
        self.direction = 'none'

    def get_lives(self):
        response = []
        for i in range(1, self.lives_amount + 1):
            if i <= self.lives:
                response.append(self.images['pacman'])
            else:
                response.append(self.images['dead_11'])
        return response