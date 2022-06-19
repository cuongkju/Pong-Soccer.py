'''
The Last Dance
This is pong with a soccer theme. Hope you enjoy!
Created by: Richard Cao
Created on: 06/01/2022
Last modified: 06/14/2022   '''

import pygame,sys, random

pygame.init()
clock = pygame.time.Clock()

width = 1280
height = 960
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong')

white = (255, 255, 255)

black = (0, 0, 0)

light_grey = (200,200,200)

yellow = (235, 223, 9)

#Load images 
soccerball_image =  pygame.transform.scale(pygame.image.load('soccer.png'),(35,35))
soccerfield_image =  pygame.transform.scale(pygame.image.load('soccerfieldresize.png'),(1280,960))
soccerscoreboard_image =  pygame.transform.scale(pygame.image.load('scoreboardresize.png'),(1280,400))

bright_red = (247, 2, 2)
red = (204, 27, 27)

#Ball starting position
BallPositionX, BallPositionY = width/2 - 15, height/2 -15
ball = pygame.Rect(BallPositionX, BallPositionY, 30,30)

#Ball speed
ball_vel_x,ball_vel_y = 7,7

player_vel_y = 0

opponent_vel = 10


#Text fonts used in the game
game_font = pygame.font.Font("freesansbold.ttf", 38)

countdown_font = pygame.font.Font("freesansbold.ttf", 60) 

name_font = pygame.font.SysFont("georgia", 38)

score_time = True

winner_font = pygame.font.Font('freesansbold.ttf',100)

#Sound
pong_sound = pygame.mixer.Sound('ponghitsound.wav')
winner_sound = pygame.mixer.Sound('winnerlosersound.mp3')
goal_sound = pygame.mixer.Sound('goalsound.mp3')

#Draw the text when the player win or lose
def draw_winner_text(text):
    winner_text = winner_font.render(text,1,red)
    win.blit(winner_text,(width/2 - winner_text.get_width()/2, height/2 - winner_text.get_height()/2))
    pygame.display.update()
   
#Input the player's name
def user_name():
    name = input("What's your name?: ")
    return name

#Write the score of each play in a text file
def write_score(name,score):
    score_file = open("scorefile.txt","a")
    if score[-1][0] > score[-1][1]:
        score_file.write("VICTORY! " + name+":"+ str(score[-1][0])+" "+"computer:"+str(score[-1][1])+"\n")
    elif score[-1][0] < score[-1][1]:    
        score_file.write("DEFEAT! " + name+":"+ str(score[-1][0])+" "+"computer:"+str(score[-1][1])+"\n")

#Draw basically everything of the game onto the screen
def draw_window(name):
    win.blit(soccerfield_image, (0,0)) 
    win.blit(soccerscoreboard_image,(40,-100))
    display_username  = name_font.render(name,False,black)
    display_opponent = name_font.render("Computer",False,black)

    win.blit(display_username,(width/3 - display_username.get_width(), 50))
    win.blit(display_opponent,(width - display_opponent.get_width() - 250, 50))

    pygame.draw.rect(win,light_grey,player)
    pygame.draw.rect(win,light_grey,opponent)
    pygame.draw.ellipse(win,light_grey,ball)
    win.blit(soccerball_image,(ball.x-3,ball.y-3))
    if score_time:
        ball_restart()

    player_text = game_font.render(f"{player_score}",False,white)
    win.blit(player_text,(613,50))
    
    opponent_text = game_font.render(f"{opponent_score}",False,white)
    win.blit(opponent_text,(669,50))
    
    pygame.display.update()

#The logic behind the ball's movement
def ball_movement():
    global ball_vel_x,ball_vel_y, player_score, opponent_score, score_time
    
    ball.x += ball_vel_x
    ball.y += ball_vel_y 


    if ball.top <= 0 or ball.bottom >= height:
        ball_vel_y *= -1
    

    #Opponent score
    if ball.left <= 0: 
        pygame.mixer.Sound.play(goal_sound)
        opponent_score += 1   
        score_time = pygame.time.get_ticks()
        
    
    #Player score
    if ball.right >= width:
        pygame.mixer.Sound.play(goal_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()
        

    #Ball hit the player
    if ball.colliderect(player) and ball_vel_x < 0: 
        if abs(ball.left - player.right) < 10:
            ball_vel_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_vel_y > 0:
            ball_vel_y  *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_vel_y < 0:
            ball_vel_y *= -1
        pygame.mixer.Sound.play(pong_sound)

    #Ball hit the opponent
    if ball.colliderect(opponent) and ball_vel_x > 0:
        if abs(ball.right - opponent.left) < 10:
            ball_vel_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_vel_y > 0:
            ball_vel_y  *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_vel_y < 0:
            ball_vel_y *= -1
        pygame.mixer.Sound.play(pong_sound)

#Player's movement
def player_movement():
    player.y += player_vel_y        
    if player.top <= 0:
        player.top = 0
    if player.bottom >= height:
        player.bottom = height      

#Computer's movement. Determining whenever the ball is higher and lower than the computer, it will go either up or down
def opponent_movement():
    if opponent.top < ball.y:
        opponent.top += opponent_vel
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_vel
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= height:
        opponent.bottom = height      

#Ball restart after someone scores. Countdown and random ball direction after it restarts. 
def ball_restart():
    global ball_vel_x,ball_vel_y,score_time
    current_time = pygame.time.get_ticks()
    ball.center = (width/2,height/2)
    
    if current_time - score_time < 700:
        number_three = countdown_font.render("3",False, yellow)
        win.blit(number_three,(width/2 -15, height/2 + 20))

    if 700 <current_time - score_time < 1400:
        number_three = countdown_font.render("2",False, yellow)
        win.blit(number_three,(width/2 -15, height/2 + 20))

    if 1400 <current_time - score_time < 2100:
        number_three = countdown_font.render("1",False, yellow)
        win.blit(number_three,(width/2 -15, height/2 + 20))



    if current_time - score_time < 2100:
        ball_vel_x,ball_vel_y = 0,0
    
    else: 
        ball_vel_x = 7 * random.choice((-1,1))
        ball_vel_y = 7 * random.choice((-1,1))
        score_time = None

score_list = []

#Main function which runs everything. Whoever reaches 5 first win! After that, the game will restart and ask the player's name again
def main():
    global score_list, player_vel_y, player_score, opponent_score,opponent, player
    
    winner_display = {"Player Win":"YOU WIN!","Computer Win":"YOU LOSE!"}
    name = user_name()
    player_score = 0
    opponent_score = 0

    player = pygame.Rect(10, height/2 - 70, 10, 140)
    opponent = pygame.Rect(width -20, height/2 - 70, 10, 140)

    run = True
    
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:  
                    player_vel_y -= 7
                if event.key == pygame.K_s:  
                    player_vel_y += 7
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:  
                    player_vel_y += 7
                if event.key == pygame.K_s:  
                    player_vel_y -= 7
        
        draw_window(name)
        winner_text = ""
        if player_score == 5:
            winner_text = winner_display["Player Win"]
        if opponent_score == 5:
            winner_text = winner_display["Computer Win"]
        if winner_text != "":
            draw_winner_text(winner_text)
            pygame.mixer.Sound.play(winner_sound)
            score_list.append((player_score,opponent_score))
            write_score(name,score_list)
            break
        
        
        ball_movement() 

        player_movement()    
        opponent_movement()
        if score_time:
            ball_restart()
        pygame.display.update()
        clock.tick(60)
    
    main()

if __name__ == "__main__":
    main()
