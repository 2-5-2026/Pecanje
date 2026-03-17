import pygame
import random

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fishing Game")

clock = pygame.time.Clock()

BLUE = (70,140,255)
DARK_BLUE = (20,70,200)
WHITE = (255,255,255)
GREEN = (60,200,100)
RED = (200,60,60)
BLACK = (0,0,0)
FISH_COLOR = (230,140,60)

font = pygame.font.SysFont(None, 36)

score = 0
highscore = 0

GAME_TIME = 60
start_time = pygame.time.get_ticks()
time_left = GAME_TIME

hook_x = WIDTH//2
hook_y = 80
hook_speed = 6

game_state = "fishing"

current_fish = None


class Fish:

    def __init__(self):

        self.width = 60
        self.height = 30

        self.x = random.randint(100, WIDTH-100)
        self.y = random.randint(300,550)

        self.speed = random.choice([-3,-2,2,3])

    def move(self):

        self.x += self.speed

        if self.x < 0 or self.x > WIDTH-self.width:
            self.speed *= -1

    def draw(self):

        pygame.draw.ellipse(screen,FISH_COLOR,(self.x,self.y,self.width,self.height))

        if self.speed > 0:

            points = [
                (self.x,self.y+self.height//2),
                (self.x-15,self.y),
                (self.x-15,self.y+self.height)
            ]

            eye_x = self.x + self.width - 10

        else:

            points = [
                (self.x+self.width,self.y+self.height//2),
                (self.x+self.width+15,self.y),
                (self.x+self.width+15,self.y+self.height)
            ]

            eye_x = self.x + 10

        pygame.draw.polygon(screen,FISH_COLOR,points)

        pygame.draw.circle(screen,WHITE,(eye_x,self.y+10),4)
        pygame.draw.circle(screen,BLACK,(eye_x,self.y+10),2)


fish_list = [Fish() for _ in range(6)]


# MINIGAME

bar_x = 150
bar_width = 600
bar_y = HEIGHT//2

square_x = bar_x
square_speed = 7

green_width = 120
green_zone = random.randint(bar_x, bar_x + bar_width - green_width)


def start_minigame():

    global square_x, square_speed, green_zone

    square_x = bar_x
    square_speed = random.choice([6,7,8])

    green_zone = random.randint(bar_x, bar_x + bar_width - green_width)


running = True

while running:

    screen.fill(BLUE)
    pygame.draw.rect(screen,DARK_BLUE,(0,250,WIDTH,HEIGHT))

    # TIMER

    if game_state != "gameover":

        elapsed = (pygame.time.get_ticks() - start_time) / 1000
        time_left = max(0, GAME_TIME - int(elapsed))

        if time_left <= 0:
            game_state = "gameover"

            if score > highscore:
                highscore = score


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


        if game_state == "minigame":

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

                if green_zone <= square_x <= green_zone+green_width:

                    score += 1

                    if current_fish in fish_list:
                        fish_list.remove(current_fish)

                    fish_list.append(Fish())

                game_state = "fishing"


        if game_state == "gameover":

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:

                score = 0
                hook_y = 80
                fish_list.clear()

                for i in range(6):
                    fish_list.append(Fish())

                start_time = pygame.time.get_ticks()
                game_state = "fishing"


    keys = pygame.key.get_pressed()

    if game_state == "fishing":

        if keys[pygame.K_UP]:
            hook_y -= hook_speed

        if keys[pygame.K_DOWN]:
            hook_y += hook_speed

        hook_y = max(50, min(HEIGHT, hook_y))

        pygame.draw.line(screen,WHITE,(hook_x,0),(hook_x,hook_y),2)
        pygame.draw.circle(screen,BLACK,(hook_x,hook_y),7)

        for fish in fish_list:

            fish.move()
            fish.draw()

            if abs(hook_x - fish.x) < 40 and abs(hook_y - fish.y) < 20:

                current_fish = fish
                start_minigame()
                game_state = "minigame"


    elif game_state == "minigame":

        pygame.draw.rect(screen,WHITE,(bar_x,bar_y,bar_width,30))
        pygame.draw.rect(screen,GREEN,(green_zone,bar_y,green_width,30))

        square_x += square_speed

        if square_x < bar_x or square_x > bar_x+bar_width-20:
            square_speed *= -1

        pygame.draw.rect(screen,RED,(square_x,bar_y,20,30))

        text = font.render("KLIKNI SPACE KADA JE CRVENI PRAVOKUTNIK U ZELENOJ ZONI!", True, WHITE)
        text_rect = text.get_rect(center=(bar_x + bar_width // 2, bar_y - 20))
        screen.blit(text, text_rect)


    elif game_state == "gameover":

        text = font.render("VRIJEME JE ISTEKLO!", True, WHITE)
        screen.blit(text,(WIDTH//2-150,HEIGHT//2-40))

        text2 = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text2,(WIDTH//2-70,HEIGHT//2))

        text3 = font.render(f"Highscore: {highscore}", True, WHITE)
        screen.blit(text3,(WIDTH//2-100,HEIGHT//2+40))

        text4 = font.render("PRITISNI R ZA RESTART", True, WHITE)
        screen.blit(text4,(WIDTH//2-160,HEIGHT//2+80))


    score_text = font.render(f"Score: {score}",True,WHITE)
    screen.blit(score_text,(20,20))

    highscore_text = font.render(f"Highscore: {highscore}",True,WHITE)
    screen.blit(highscore_text,(20,60))

    time_text = font.render(f"Time: {time_left}", True, WHITE)
    screen.blit(time_text,(WIDTH-150,20))


    pygame.display.update()
    clock.tick(60)

pygame.quit()
