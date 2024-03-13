import pygame
from game import Game
from colours import Colours
from bot import Bot

#Button Class For Handling The Buttons
class Button:
	def __init__(self,text,width,height,pos,elevation,top_color,bottom_color,highlight):
		#Core attributes 
		self.pressed = False
		self.elevation = elevation
		self.dynamic_elecation = elevation
		self.highlight = highlight
		self.original_y = pos[1]

		# top rectangle 
		self.top_rect = pygame.Rect(pos,(width,height))
		self.top_color = top_color
		self.base_top = top_color

		# bottom rectangle 
		self.bottom_rect = pygame.Rect(pos,(width,height))
		self.bottom_color = bottom_color
  
		#text
		self.text_surf = gui_font.render(text,True,'#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

	def draw(self):
		# elevation logic 
		self.top_rect.y = self.original_y - self.dynamic_elecation
		self.text_rect.center = self.top_rect.center 

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

		pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius =60)
		pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 60)
		screen.blit(self.text_surf, self.text_rect)
		self.check_click()

	def check_click(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			self.top_color = self.highlight
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elecation = 0
				self.pressed = True
			else:
				self.dynamic_elecation = self.elevation
				if self.pressed == True:
					print('clicked')
					self.pressed = False
		else:
			self.dynamic_elecation = self.elevation
			self.top_color = self.base_top


pygame.init()

title_font = pygame.font.Font(None, 40)
score_surface =  title_font.render("Score", True, Colours.white)
next_surface = title_font.render("Next", True, Colours.white)
score_rect = pygame.Rect (10, 55, 170, 60)
next_rect = pygame.Rect(10, 215, 170, 180)
game_over_surface = title_font.render("GAME OVER", True, Colours.white)


backgroundcolour = (85, 85, 85) 
WIDTH = 550
HEIGHT = 720

game = Game()
bot = Bot()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 500)
 
screen = pygame.display.set_mode((WIDTH,HEIGHT))

clock = pygame.time.Clock()


WIDTH = 550
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Gui Menu')
clock = pygame.time.Clock()
gui_font = pygame.font.Font(None,30)

playGame = False
watchAI = False
restartButton = Button('Restart',180,50,(5,590),5,Colours.light_purple,Colours.purple,(190, 0, 210))
menuButton = Button('Main Menu',180,50,(5,650),5,Colours.light_purple,Colours.purple,(190, 0, 210))
button1 = Button('Start',306,94,(122,200),5,'#998181','#847272','#7E6B6B')
button2 = Button('Watch AI',306,94,(122,350),5,'#998181','#847272','#7E6B6B')
button3 = Button('Quit',306,94,(122,500),5,'#998181','#847272','#7E6B6B')

while True:
	if not playGame and not watchAI:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		screen.fill('#BDABAB')
		button1.draw()
		button2.draw()
		button3.draw()
		
		if(button1.pressed):
			title_font = pygame.font.Font(None, 40)
			score_surface =  title_font.render("Score", True, Colours.white)
			next_surface = title_font.render("Next", True, Colours.white)
			score_rect = pygame.Rect (10, 55, 170, 60)
			next_rect = pygame.Rect(10, 215, 170, 180)
			game_over_surface = title_font.render("GAME OVER", True, Colours.white)


			backgroundcolour = (85, 85, 85) 
			WIDTH = 550
			HEIGHT = 720

			game = Game()

			GAME_UPDATE = pygame.USEREVENT
			pygame.time.set_timer(GAME_UPDATE, 500)

			screen = pygame.display.set_mode((WIDTH,HEIGHT))

			clock = pygame.time.Clock()
			button1.pressed = False
			playGame = True
      
		elif(button2.pressed):
			title_font = pygame.font.Font(None, 40)
			score_surface =  title_font.render("Score", True, Colours.white)
			next_surface = title_font.render("Next", True, Colours.white)
			score_rect = pygame.Rect (10, 55, 170, 60)
			next_rect = pygame.Rect(10, 215, 170, 180)
			game_over_surface = title_font.render("GAME OVER", True, Colours.white)


			backgroundcolour = (85, 85, 85) 
			WIDTH = 550
			HEIGHT = 720

			game = Game()
			bot = Bot()
			GAME_UPDATE = pygame.USEREVENT
			pygame.time.set_timer(GAME_UPDATE, 40)

			screen = pygame.display.set_mode((WIDTH,HEIGHT))

			clock = pygame.time.Clock()			
			button2.pressed = False
			watchAI = True
		elif(button3.pressed):
			pygame.quit()
		
		
		

		
	if playGame:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if game.game_over == True:
					game.game_over = False
					game.reset()
				if event.key == pygame.K_LEFT and game.game_over == False:
					game.move_left()
				if event.key == pygame.K_RIGHT and game.game_over == False:
					game.move_right()
				if event.key == pygame.K_DOWN and game.game_over == False:
					game.move_down()
					game.update_score(0, 1)
				if event.key == pygame.K_UP and game.game_over == False:
					game.rotate()
				if(event.key == pygame.K_SPACE and game.game_over == False):
					while(game.state != "block_locked"):
						game.move_down()
			if event.type == GAME_UPDATE and game.game_over == False:
				game.move_down()

		score_value_surface = title_font.render(str(game.score), True, Colours.white)

		screen.fill(backgroundcolour)
		screen.blit(score_surface, (55, 10, 50, 50))
		screen.blit(next_surface, (65, 170, 50, 50))
		if game.game_over == True:
			screen.blit(game_over_surface, (10, 450, 50, 50))
		pygame.draw.rect(screen, Colours.light_purple, score_rect, 0, 40)
		screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
		pygame.draw.rect(screen, Colours.light_purple, next_rect, 0, 40)
		game.draw(screen)
		menuButton.draw()
		restartButton.draw()
		if(restartButton.pressed):
			game = Game()
			bot = Bot()
		if(menuButton.pressed):
			WIDTH = 550
			HEIGHT = 720
			screen = pygame.display.set_mode((WIDTH,HEIGHT))
			pygame.display.set_caption('Gui Menu')
			clock = pygame.time.Clock()
			gui_font = pygame.font.Font(None,30)
			menuButton.pressed = False
			playGame = False
			watchAI = False

	if  watchAI:

		run = True
		# Closing the game
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				quit()
					
				
			if event.type == GAME_UPDATE and game.game_over == False:
				bot.handle_block(game)


		score_value_surface = title_font.render(str(game.score), True, Colours.white)


		screen.fill(backgroundcolour)
		screen.blit(score_surface, (55, 10, 50, 50))
		screen.blit(next_surface, (65, 170, 50, 50))
		if game.game_over == True:
			screen.blit(game_over_surface, (10, 450, 50, 50))
		pygame.draw.rect(screen, Colours.light_purple, score_rect, 0, 40)
		screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
		pygame.draw.rect(screen, Colours.light_purple, next_rect, 0, 40)
		game.draw(screen)
		menuButton.draw()
		restartButton.draw()
		if(restartButton.pressed):
			game = Game()
			bot = Bot()
		if(menuButton.pressed):
			WIDTH = 550
			HEIGHT = 720
			screen = pygame.display.set_mode((WIDTH,HEIGHT))
			pygame.display.set_caption('Gui Menu')
			clock = pygame.time.Clock()
			gui_font = pygame.font.Font(None,30)
			menuButton.pressed = False
			playGame = False
			watchAI = False
   
	pygame.display.update()
	clock.tick(60 )