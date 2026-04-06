
import pygame
import random

pygame.init() #Pokreće pygame

WIDTH, HEIGHT = 900, 600 #Dimenzije prozora
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Kreiranje prozora 
pygame.display.set_caption("Pecanje") #Imenovanje prozora

clock = pygame.time.Clock() #Stvara "objekt" koji pomaže u praćenju vremena
#Imenovanje boja (za lakše korištenje kasnije)
BLUE = (70,140,255)
DARK_BLUE = (20,70,200)
WHITE = (255,255,255)
GREEN = (60,200,100)
RED = (200,60,60)
BLACK = (0,0,0)
FISH_COLOR = (230,140,60)

font = pygame.font.SysFont(None, 36) #Font za tekst

score = 0 
highscore = 0

GAME_TIME = 60 #Trajanje igre
start_time = pygame.time.get_ticks() #Koliko je milisekundi prošlo od pokretanja pygamea
time_left = GAME_TIME

hook_x = WIDTH//2 #Početna pozicija udice
hook_y = 80 #Početna pozicija udice
hook_speed = 6 #Brzina micanja udice

game_state = "fishing" #1. faza igre - pecanje ribe

current_fish = None


class Fish: #Definira kako će riba izgledati, brzinu i poziciju

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

        pygame.draw.ellipse(screen,FISH_COLOR,(self.x,self.y,self.width,self.height)) #Tijelo ribe

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

        pygame.draw.polygon(screen,FISH_COLOR,points) #Rep ribe
        
        pygame.draw.circle(screen,WHITE,(eye_x,self.y+10),4) #Vanjski dio oka
        pygame.draw.circle(screen,BLACK,(eye_x,self.y+10),2) #Unutarnji dio oka


fish_list = [Fish() for _ in range(6)] #Broj riba


# 2.faza igre - mini game nakon što je riba upecana
# Pozicija,veličina i izgled bara za 1.upecanu ribu
bar_x = 150 #Pozicija bara
bar_width = 600 #Širina bara
bar_y = HEIGHT//2 #Pozicija bara

square_x = bar_x #Početna pozicija crvenog pravokutnika
square_speed = 7 #Brzina crvenog pravokutnika

green_width = 120 #Širina zelene zone
green_zone = random.randint(bar_x, bar_x + bar_width - green_width) #Nasumična pozicija zelene zone


def start_minigame(): #Početak mini gamea, za 2.upecanu ribu i sve nakon nje

    global square_x, square_speed, green_zone #Omogućuje korištenje i mijenjanje varijabli izvan funkcije 

    square_x = bar_x #Početna pozicija crvenog pravokutnika
    square_speed = random.choice([6,7,8]) #Brzina crvenog pravokutnika

    green_zone = random.randint(bar_x, bar_x + bar_width - green_width) #Nasumična pozicija zelene zone

#Omogućuje trajanje igre dok je istekne vrijeme
running = True

while running:

    screen.fill(BLUE) #Crtanje neba
    pygame.draw.rect(screen,DARK_BLUE,(0,250,WIDTH,HEIGHT)) #Crtanje mora

    # Štoperica

    if game_state != "gameover":

        elapsed = (pygame.time.get_ticks() - start_time) / 1000 #Koliko je vremena prošlo
        time_left = max(0, GAME_TIME - int(elapsed)) #Preostalo vrijeme
        #Kraj igre kad istekne vrijeme
        if time_left <= 0:
            game_state = "gameover"
            #Promjena highscora ako je potrebno
            if score > highscore:
                highscore = score


    for event in pygame.event.get(): #Event - akcije korisnika npr. klik miša i pritisak tipke na tipkovnici, izvršava sve evente
        #Gasi sve pygame module i zatvara igru
        if event.type == pygame.QUIT:
            running = False

        
        if game_state == "minigame":
            #Dektektira pritisak spacea/razmaka
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                #Provjerava je li pravokutnik u zelenoj zoni
                if green_zone <= square_x <= green_zone+green_width:

                    score += 1 #Povećavanje scora ako da

                    if current_fish in fish_list: 
                        fish_list.remove(current_fish) #Izbacuje ulovljenu ribu

                    fish_list.append(Fish()) #Dodaje novu ribu

                game_state = "fishing" #Povratak na pecanje


        if game_state == "gameover":

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: #Dektektira pritisak tipke R za ponovno pokretanje igre
                #Reset varijabli
                score = 0
                hook_y = 80
                fish_list.clear() #Briše sve ribe

                for i in range(6):
                    fish_list.append(Fish()) #Dodavanje riba

                start_time = pygame.time.get_ticks() #Resetiranje vremena
                game_state = "fishing" #Povratak na pecanje


    keys = pygame.key.get_pressed() #Provjerava koje tipke "drži" korisnik

    if game_state == "fishing":
        #Spuštanje/dizanje udice ako korisnik stisne stelicu prema dolje/gore na tipkovnici
        if keys[pygame.K_UP]:
            hook_y -= hook_speed

        if keys[pygame.K_DOWN]:
            hook_y += hook_speed

        hook_y = max(50, min(HEIGHT, hook_y)) #Ograničenje da udica ne izađe iz programa
        #Crtanje udice
        pygame.draw.line(screen,WHITE,(hook_x,0),(hook_x,hook_y),2)
        pygame.draw.circle(screen,BLACK,(hook_x,hook_y),7)

        for fish in fish_list:

            fish.move()
            fish.draw()
            #Provjera dodira između ribe i udice
            if abs(hook_x - fish.x) < 40 and abs(hook_y - fish.y) < 20: #Pokreće minigame
        
                current_fish = fish
                start_minigame()
                game_state = "minigame"


    elif game_state == "minigame":

        pygame.draw.rect(screen,WHITE,(bar_x,bar_y,bar_width,30)) #Crtanje bijelog bara
        pygame.draw.rect(screen,GREEN,(green_zone,bar_y,green_width,30)) #Crtanje zelene zone

        square_x += square_speed #Micanje crvenog pravokutnika

        if square_x < bar_x or square_x > bar_x+bar_width-20:
            square_speed *= -1 #Promjena smjera crvenog pravokutnika kada dođe do kraja bara

        pygame.draw.rect(screen,RED,(square_x,bar_y,20,30)) #Crtanje crvenog pravokutnika
        
        text = font.render("KLIKNI SPACE KADA JE CRVENI PRAVOKUTNIK U ZELENOJ ZONI!", True, WHITE) #Pretvara tekst u "sliku"
        text_rect = text.get_rect(center=(bar_x + bar_width // 2, bar_y - 20)) #Pozicioniranje teksta
        screen.blit(text, text_rect) #Prikazuje sliku na ekranu (ali još nije vidljivo korisniku)


    elif game_state == "gameover":
        #Ispis poruka
        text = font.render("VRIJEME JE ISTEKLO!", True, WHITE) 
        screen.blit(text,(WIDTH//2-150,HEIGHT//2-40))

        text2 = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text2,(WIDTH//2-70,HEIGHT//2))

        text3 = font.render(f"Highscore: {highscore}", True, WHITE)
        screen.blit(text3,(WIDTH//2-100,HEIGHT//2+40))

        text4 = font.render("PRITISNI R ZA PONOVNO POKRETANJE", True, WHITE)
        screen.blit(text4,(WIDTH//2-160,HEIGHT//2+80))

    #Stalni tekst : score, highscore, vrijeme
    score_text = font.render(f"Score: {score}",True,WHITE)
    screen.blit(score_text,(20,20))

    highscore_text = font.render(f"Highscore: {highscore}",True,WHITE)
    screen.blit(highscore_text,(20,60))

    time_text = font.render(f"Vrijeme: {time_left}", True, WHITE)
    screen.blit(time_text,(WIDTH-150,20))

    pygame.display.update() #Pojavljivanje svega na ekranu
    clock.tick(60) #Ograničava igru na 60 FPS
#Završetak igre
pygame.quit()
