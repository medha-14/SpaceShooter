import pygame
from random import randint,uniform

#classes
class player(pygame.sprite.Sprite):
   def __init__(self,groups):
      super().__init__(groups)
      self.image=pygame.image.load("images/player.png").convert_alpha()
      self.rect=self.image.get_frect(center=(  WINDOW_WIDTH/2,WINDOW_HEIGHT/2-100))
      self.direction=pygame.math.Vector2(0,0)
      self.speed=300

       #laser 
      self.can_shoot=True
      self.last_shoot_time=0
      self.cooldown_time=1000

   def Lasertimer(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_shoot_time >= self.cooldown_time:
            self.can_shoot=True   

   def update(self,dt):
        keys=pygame.key.get_pressed()
        self.direction.x= int(keys[pygame.K_RIGHT])-int(keys[pygame.K_LEFT])
        self.direction.y= int(keys[pygame.K_DOWN])-int(keys[pygame.K_UP])
        self.direction=self.direction.normalize()if self.direction else self.direction
        self.rect.center += self.direction*self.speed*dt  

        laserkey=pygame.key.get_just_pressed()
        if laserkey[pygame.K_SPACE] and self.can_shoot:
                      laser(laser_surf,self.rect.midtop,[all_sprites,laser_sprites])
                      self.can_shoot=False
                      self.last_shoot_time=pygame.time.get_ticks()
                      laser_sound.play()
                      

        self.Lasertimer()  

class star(pygame.sprite.Sprite):
    def __init__(self,groups):
            super().__init__(groups) 
            self.image=star_surf
            self.rect=self.image.get_frect(center=(randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)))

class meteor(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
            super().__init__(groups) 
            self.image=surf
            self.original_surf=surf
            self.rect=self.image.get_frect(center=pos)
            # timer
            self.lifetime=3000
            self.start_time=pygame.time.get_ticks()    
            self.direction=pygame.math.Vector2(uniform(-0.5,0.5),1)
            self.speed =randint(400,500)   
            self.rotation=0  
            self.rotation_speed=randint(400,500)
    def update(self,dt):
            self.rect.center += self.direction * self.speed * dt   
            if pygame.time.get_ticks()-self.start_time>=self.lifetime:
                self.kill() 
            self.rotation += self.rotation_speed *dt
            self.image=pygame.transform.rotozoom(self.original_surf,self.rotation,1)  
            self.rect=self.image.get_frect(center=self.rect.center)
            
class laser(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
            super().__init__(groups) 
            self.image=laser_surf
            self.rect=self.image.get_frect(midbottom = pos)

    def update(self,dt):
            self.rect.centery -= 400*dt
            if self.rect.bottom < 0:
                  self.kill()

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self,frames,pos,groups):
          super().__init__(groups)
          self.frames=frames
          self.frame_index=0  
          self.image=frames[self.frame_index]
          self.rect=self.image.get_frect(center=pos)
    def update(self,dt):
         self.frame_index +=20 *dt
         if self.frame_index < len(self.frames):
            self.image=self.frames[int(self.frame_index)]
         else:
              self.kill()   
          

#collisions
def collisions():
    global running

    if pygame.sprite.spritecollide(player,meteor_sprites,True,pygame.sprite.collide_mask):
          damage_sound.play()
          running=False       

    for lazer in laser_sprites:      
        collided_sprites=pygame.sprite.spritecollide(lazer,meteor_sprites,True)
        if collided_sprites:
             lazer.kill()
             AnimatedExplosion(explosion_frames,lazer.rect.midtop,all_sprites)
             explosion_sound.play()

#score
def display_score():
    current_time=pygame.time.get_ticks()//100
    text_surf=font.render(str(current_time),True,(240,240,240))
    text_rect=text_surf.get_rect(midbottom=(WINDOW_WIDTH/2,WINDOW_HEIGHT-50))
    pygame.draw.rect(display_surface,(240,240,240),text_rect.inflate(30,15).move(0,-8),5,10)
    display_surface.blit(text_surf,text_rect)
     

#general setup
pygame.init()
WINDOW_HEIGHT=720
WINDOW_WIDTH=1280
display_surface=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
Clock=pygame.time.Clock()
running=True

#imports
star_surf=pygame.image.load("images/star.png").convert_alpha()
laser_surf=pygame.image.load("images/laser.png").convert_alpha()
meteor_surf=pygame.image.load("images/meteor.png").convert_alpha()
font=pygame.font.Font("images/Oxanium-Bold.ttf",40)
explosion_frames=[pygame.image.load(f"images/explosion/{i}.png").convert_alpha() for i in range (21)]

laser_sound=pygame.mixer.Sound("audio/laser.wav")
laser_sound.set_volume(0.3)
game_music=pygame.mixer.Sound("audio/game_music.wav")
game_music.set_volume(0.4)
game_music.play()
explosion_sound=pygame.mixer.Sound("audio/explosion.wav")
damage_sound=pygame.mixer.Sound("audio/damage.ogg")

#sprites
all_sprites=pygame.sprite.Group()
meteor_sprites=pygame.sprite.Group()
laser_sprites=pygame.sprite.Group()
for i in range (1,20):
    star(all_sprites)
player=player(all_sprites)


#meteor_event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event,500)  

#game loop
while running:
    dt= Clock.tick()/1000 

    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False
        if event.type== meteor_event:
            pos=(randint(0,WINDOW_WIDTH),randint(-200,100))
            meteor(meteor_surf,pos,[all_sprites,meteor_sprites]) 
    
    #updates
    all_sprites.update(dt)
    collisions()
    

    #draw the game
    display_surface.fill("#3a2e3f")    

    display_score()
     
    all_sprites.draw(display_surface)

    
    pygame.display.update()

pygame.quit()    