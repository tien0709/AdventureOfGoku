import pygame
from tile import AnimatedTile
from random import randint
from HealthBar import *
from settings import *

class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, '../graphics/enemy/run')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = -1*randint(3,5)
        self.healthBar =  HealthBar(  widthHealthBar_enemy, heightHealthBar, hpEnemy)###########################
        self.be_hited = True###########################
        self.can_reverse = True ######################################
    def move(self):
        self.rect.x += self.speed
        
    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)
            
    def reverse(self):
        self.speed *= -1
            
    def update(self, shift_x, shift_y):##################################
        self.rect.x += shift_x
        self.rect.y += shift_y
        if(self.healthBar.health) <= 0 : self.kill()########################################
        self.animate()
        self.move()
        self.reverse_image()
       # self.healthBar.update()###########################