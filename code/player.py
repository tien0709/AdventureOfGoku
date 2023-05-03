import pygame,time
from support import import_folder
from  HealthBar import * 
from settings import *
from  manaBar import * 
from end import*

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,surface,create_jump_particles):
		super().__init__()
		self.ssj = False
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.15
		self.image = self.animations['idle'][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)	
		self.mana = mana##########################################
		self.healthBar =  HealthBar(  widthHealthBar_player, heightHealthBar, hpPlayer)###########################
		self.manaBar =  manaBar(  widthHealthBar_player, heightHealthBar, self.mana)###########################
		self.killed_boss = False#########################################
		self.time_end = 0############################3
		self.collect_coin = True#####################
		#self.be_cleave = True###########################
		#self.time_to_be_cleave = 0#######################
		# dust particles 
		self.import_dust_run_particles()
		self.dust_frame_index = 0
		self.dust_animation_speed = 0.15
		self.display_surface = surface
		self.create_jump_particles = create_jump_particles

		# player movement
		self.direction = pygame.math.Vector2(0,0)
		self.gravity = 0.8
		self.jump_speed = -20

		# player status
		self.status = 'idle'
		self.facing_right = True
		self.on_enemy = False#############################
		self.be_bited = True#################
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False
		self.hitting = False
		self.canmove = True
		self.fire = False
		self.sit = False
		self.focus = False
		self.kame_sound = pygame.mixer.Sound("../music/kamehameha.wav")
	
		#set flag for else statement in status function
		self.else_flag = True
  
		#set time counter for fire ball
		self.past_time = -100000

	def import_character_assets(self):
		if self.ssj == False:
			character_path = '../graphics/character/'
		else:
			character_path = '../graphics/ssj/'
		self.animations = {'idle':[],'run':[],'jump':[],'fall':[], 'hit':[], 'firing':[], 'sit':[],'be_bited_left':[], 'be_bited_right':[], 'focus':[],'die':[], 'win': []}###########################

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def import_dust_run_particles(self):
		self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')

	def animate(self):
		animation = self.animations[self.status]

		# loop over frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		image = animation[int(self.frame_index)]
		if self.facing_right:
			self.image = image
		else:
			flipped_image = pygame.transform.flip(image,True,False)
			self.image = flipped_image

		# set the rect
		if self.on_ground and self.on_right:
			self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
		elif self.on_ground and self.on_left:
			self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		elif self.on_ground:
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		elif self.on_ceiling and self.on_right:
			self.rect = self.image.get_rect(topright = self.rect.topright)
		elif self.on_ceiling and self.on_left:
			self.rect = self.image.get_rect(topleft = self.rect.topleft)
		elif self.on_ceiling:
			self.rect = self.image.get_rect(midtop = self.rect.midtop)

	def run_dust_animation(self):
		if self.status == 'run' and self.on_ground:
			self.dust_frame_index += self.dust_animation_speed
			if self.dust_frame_index >= len(self.dust_run_particles):
				self.dust_frame_index = 0

			dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

			if self.facing_right:
				pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
				self.display_surface.blit(dust_particle,pos)
			else:
				pos = self.rect.bottomright - pygame.math.Vector2(6,10)
				flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
				self.display_surface.blit(flipped_dust_particle,pos)

	def get_input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT] and self.canmove:
			self.direction.x = 1
			self.facing_right = True
		elif keys[pygame.K_LEFT] and self.canmove:
			self.direction.x = -1
			self.facing_right = False
		else:
			self.direction.x = 0
		
		if keys[pygame.K_SPACE] and self.on_ground:
			self.jump()
			self.create_jump_particles(self.rect.midbottom)
        
		if keys[pygame.K_DOWN] and self.on_ground:#######################################################
			self.sit = True#######################################################
		else: self.sit = False
			

		if keys[pygame.K_x] and self.on_ground:
			self.hitting = True
		else: self.hitting = False
		
		current_time = pygame.time.get_ticks()
		
		if keys[pygame.K_z] and self.on_ground:
			if current_time - self.past_time >= 2000:
				self.fire = True
				self.past_time = current_time
    
		if keys[pygame.K_c] and self.on_ground:
			self.focus = True
		else: self.focus = False
		
		if self.manaBar.mana >= 100:
			if keys[pygame.K_v] and self.on_ground:
					self.ssj = True
					self.import_character_assets()
 
 

	def get_status(self):
		current_time = pygame.time.get_ticks()
  
		#when we hit firing status, we have to wait for 0.5 second to perform firing pose
		#this if statement only work if we lock else_flag, then we have to wait for 0.5 second to unlock the last else statement
		if current_time - self.past_time > 500:
			self.else_flag = True
			self.canmove = True
   
		#Check ssj status
		if self.manaBar.mana == 0:
			self.ssj = False
			self.import_character_assets()
        #check the status of player
		if self.healthBar.health == -9999:########################
			self.status = 'win'##################################
			self.canmove = False##########################
		elif self.healthBar.health <= 0:########################
			self.status = 'die'##################################
			self.canmove = False##########################
		
		elif self.focus == True:
			self.status = 'focus'
			self.canmove = False
		elif self.fire == True:
			self.status = 'firing'
			self.canmove = False
			self.else_flag = False
		elif self.hitting == True:
			self.status = 'hit'
			self.canmove = False
		elif self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 1:
			self.status = 'fall'
		elif self.sit == True:#############################
			self.status = 'sit' ###############################################3
		elif self.be_bited == False:
			self.status = 'be_bited_right'################################ 
			if self.facing_right :#######################################
				self.status = 'be_bited_left'############################# 
		elif self.else_flag == True:
			self.canmove = True
			if self.direction.x != 0:
				self.status = 'run'
			else:
				self.status = 'idle'

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def jump(self):
		self.direction.y = self.jump_speed	

	def update(self):########################################
		if self.status == 'win' : ################### vi ta cap nhat truc tiep status khong thong qua get_status nen de tranh
      ## bi chong code nen check truoc luon
			if self.time_end == 0: self.time_end = pygame.time.get_ticks()###############################
			else: #####################################################
				if(pygame.time.get_ticks() - self.time_end>=1000):##############################
					endGame('win')############################
		self.get_input()
		self.get_status()
		self.animate()
		self.run_dust_animation()
		if self.status == 'die' : ################### 
				if self.time_end == 0: self.time_end = pygame.time.get_ticks()###############################
				else: #####################################################
					if(pygame.time.get_ticks() - self.time_end>=1000):##############################
						endGame('lose')############################

		#self.healthBar.update()  ###############################  	
        
		
		