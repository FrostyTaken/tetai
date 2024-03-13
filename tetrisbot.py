import pygame
from bot import Bot
from game import Game
from colours import Colours

# Screen Settings
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
pygame.time.set_timer(GAME_UPDATE, 5)

screen = pygame.display.set_mode((WIDTH,HEIGHT))

clock = pygame.time.Clock()
run = True




# Closing the game
while run == True:
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
    pygame.display.update() 