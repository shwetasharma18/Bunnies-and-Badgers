import sys, pygame

from pygame.locals import * 

import math

import random

pygame.init()

pygame.mixer.init()

width, height = 640, 480

screen = pygame.display.set_mode((width, height))

def game():
	acc = [0,0]
	
	arrows = []
	
	badtimer = 100
	
	badtimer1 = 0
	
	badguys = [[640,100]]
	
	healthvalue = 194
	
	keys = [False, False, False, False, False]
	
	playerpos=[100,100]
	
	grass = pygame.image.load("resources/images/grass.png")
	
	castle = pygame.image.load("resources/images/castle.png")
	
	player = pygame.image.load("resources/images/dude.png")
	
	arrow = pygame.image.load("resources/images/bullet.png")
	
	healthbar = pygame.image.load("resources/images/healthbar.png")
	
	health = pygame.image.load("resources/images/health.png")
	
	badguyimg1 = pygame.image.load("resources/images/badguy.png")
	
	badguyimg = badguyimg1
	
	gameover = pygame.image.load("resources/images/gameover.png")
	
	youwin = pygame.image.load("resources/images/gameover.png")
	
	hit = pygame.mixer.Sound("resources/audio/explode.wav")
	
	enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
	
	shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
	
	hit.set_volume(0.05)
	
	enemy.set_volume(0.05)
	
	shoot.set_volume(0.05)
	
	pygame.mixer.music.load("resources/audio/moonlight.wav")
	
	pygame.mixer.music.play(-1, 0.0)
	
	pygame.mixer.music.set_volume(0.25)
	
	running = 1
	
	exitcode = 0
	
	while running:
	
		pygame.display.flip()
	
		for event in pygame.event.get():
	
			if event.type == pygame.QUIT: sys.exit()
	
		screen.fill(0)
	
	
		for x in range(width/grass.get_width()+1):
			for y in range(height/grass.get_height()+1):
				screen.blit(grass,(x*100,y*100))
		screen.blit(castle,(0,30))
		screen.blit(castle,(0,135))
		screen.blit(castle,(0,240))
		screen.blit(castle,(0,345 ))
		position = pygame.mouse.get_pos()
		angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
		playerrot = pygame.transform.rotate(player, 360-angle*57.29)
		playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
		screen.blit(playerrot,playerpos1)
		for bullet in arrows:
			index = 0
			velx = math.cos(bullet[0])*10
			vely = math.sin(bullet[0])*10
			bullet[1]+=velx
			bullet[2]+=vely
			if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
				arrows.pop(index)
			index += 1
			for projectile in arrows:
				arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
				screen.blit(arrow1, (projectile[1], projectile[2]))
		if badtimer == 0:
			badguys.append([640, random.randint(50,430)])
			badtimer = 100-(badtimer1*2)
			if badtimer1 >= 35:
				badtimer1 = 35
			else:
				badtimer1 += 5
		index = 0
		for badguy in badguys:
			if badguy[0]<-64:
				badguys.pop(index)
			badguy[0]-=7
			badrect = pygame.Rect(badguyimg.get_rect())
			badrect.top = badguy[1]
			badrect.left = badguy[0]
			if badrect.left<64:
				hit.play()
				healthvalue -= random.randint(5,20)
				badguys.pop(index)
			
			index1 = 0
		
			for bullet in arrows:
				bullrect = pygame.Rect(arrow.get_rect())
				bullrect.left = bullet[1]
				bullrect.top = bullet[2]
				if badrect.colliderect(bullrect):
					enemy.play()
					acc[0] += 1
					badguys.pop(index)
					arrows.pop(index1)
					
				index1 += 1
			index += 1
	
		for badguy in badguys:
			screen.blit(badguyimg, badguy)
	
		font = pygame.font.Font(None,24)
		survivedtext = font.render(str((90000-pygame.time.get_ticks())/60000)+":"+str((90000-pygame.time.get_ticks())/1000%60).zfill(2),True, (0,0,0))
		textRect = survivedtext.get_rect()
		textRect.topright=[635,5]
		screen.blit(survivedtext, textRect)
		screen.blit(healthbar, (5,5))
		
		for health1 in range(healthvalue):
			screen.blit(health, (health1 + 8, 8))
		
		pygame.display.flip()
		
		for event in pygame.event.get():
	        # check if the event is the X button 
			if event.type == pygame.MOUSEBUTTONDOWN:
				position = pygame.mouse.get_pos()
				acc[1] += 1
				arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])
			
			if event.type == pygame.KEYDOWN:
				if event.key==K_w:
					keys[0]=True
	     
				elif event.key==K_a:
					keys[1]=True
	
				elif event.key==K_s:
					keys[2]=True
				
				elif event.key==K_d:
					keys[3]=True
	
				
			if event.type == pygame.KEYUP:
				
				if event.key==pygame.K_w:
					keys[0]=False
				
				if event.key==pygame.K_a:
					keys[1]=False
				
				if event.key==pygame.K_s:
					keys[2]=False
				
				if event.key==pygame.K_d:
					keys[3]=False
	
		
		if keys[0]:
			playerpos[1] -= 5
		elif keys[2]:
			playerpos[1] += 5
		if keys[1]:
			playerpos[0] -= 5
		elif keys[3]:
			playerpos[0] += 5
		badtimer -= 1
	
		if pygame.time.get_ticks()>=90000:
			running = 0
			exitcode = 1
		if healthvalue<=0:
			running = 0
			exitcode = 0
		if acc[1]!=0:
			accuracy = acc[0]*1.0/acc[1]*100
		else:
			accuracy = 0
	
	
	
	if exitcode == 0:
		pygame.font.init()
		font = pygame.font.Font(None, 24)
		text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
		textRect = text.get_rect()
		textRect.centerx = screen.get_rect().centerx
		textRect.centery = screen.get_rect().centery+24
		screen.blit(gameover, (0,0))
		screen.blit(text, textRect)
	else:
		pygame.font.init()
		font = pygame.font.Font(None, 24)
		text = font.render("Accuracy: "+str(accuracy)+"%", True, (0,255,0))
		textRect = text.get_rect()
		textRect.centerx = screen.get_rect().centerx
		textRect.centery = screen.get_rect().centery+24
		screen.blit(gameover, (0,0))
		screen.blit(text, textRect)

game()


bigfont = pygame.font.Font(None, 80)

smallfont = pygame.font.Font(None, 45)




def play_again():
	while True:
		text = bigfont.render('Play again?', 13, (0, 0, 0))
		textx = width / 2 - text.get_width() / 2
		texty = height / 2 - text.get_height() / 2
		textx_size = text.get_width()
		texty_size = text.get_height()
		pygame.draw.rect(screen, (255, 255, 255), ((textx - 5, texty - 5),
                                              (textx_size + 10, texty_size +
                                               10)))
		screen.blit(text, (width / 2 - text.get_width() / 2,
                      height / 2 - text.get_height() / 2))
		clock = pygame.time.Clock()

		pygame.display.flip()
   
		in_main_menu = True
  
		while in_main_menu:
	
			clock.tick(50)
	
			for event in pygame.event.get():
		
				if event.type == pygame.QUIT:
			
					in_main_menu = False
					pygame.display.quit()
			
					pygame.quit()
			
					quit()

		
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			
					x, y = event.pos
			
					if x >= textx - 5 and x <= textx + textx_size + 5:
				
						if y >= texty - 5 and y <= texty + texty_size + 5:
					
							in_main_menu = False
							break		
							
    		game()

play_again()

