import pygame
import sys
import random

pygame.init()


class Window:
    def __init__(self):
        self.play = True
        self.proportions = 1000
        self.screen = pygame.display.set_mode((self.proportions, self.proportions))
        self.apple = False
        self.scale = 20
        self.paused = False
        pygame.display.set_caption("Snake")
        self.font = pygame.font.Font(pygame.font.get_default_font(), int(self.proportions / self.scale))
        self.score = 0
        self.scorelable = self.font.render(f"{self.score}", True, (255, 255, 255))

    def mainloop(self):
        S.draw()
        while self.play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and S.direction != "down" and not self.paused:
                    S.direction = "up"
                    if not S.alive:
                        S.alive = True
                    else:
                        pygame.mixer.Sound.play(S.movesound)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and S.direction != "up" and not self.paused:
                    S.direction = "down"
                    if not S.alive:
                        S.alive = True
                    else:
                        pygame.mixer.Sound.play(S.movesound)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and S.direction != "right" and not self.paused:
                    S.direction = "left"
                    if not S.alive:
                        S.alive = True
                    else:
                        pygame.mixer.Sound.play(S.movesound)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and S.direction != "left" and not self.paused:
                    S.direction = "right"
                    if not S.alive:
                        S.alive = True
                    else:
                        pygame.mixer.Sound.play(S.movesound)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if not self.paused:
                        self.paused = True
                    else:
                        self.paused = False
            pygame.time.delay(150)
            if S.alive and not self.paused:
                if not self.apple:
                    A.create()
                S.newhead()
                S.draw()


class Snake:
    def __init__(self):
        self.proportions = Win.proportions / Win.scale
        self.coords = [[Win.proportions / 2, Win.proportions / 2]]
        self.velocity = self.proportions
        self.direction = "up"
        self.alive = False
        self.deathsound = pygame.mixer.Sound("death.wav")
        self.movesound = pygame.mixer.Sound("move.wav")
    def draw(self):
        Win.screen.fill((0, 0, 0))
        for coord in self.coords:
            pygame.draw.rect(Win.screen, (255, 0, 0), (coord[0], coord[1], self.proportions, self.proportions))
        if Win.apple:
            pygame.draw.rect(Win.screen, (0, 255, 0), (A.x, A.y, self.proportions, self.proportions))

        Win.screen.blit(Win.scorelable, dest=(0, 0))
        pygame.display.update()

    def newhead(self):
        newcoord = ""
        if self.direction == "left":
            newcoord = [self.coords[0][0] - self.proportions, self.coords[0][1]]
        elif self.direction == "right":
            newcoord = [self.coords[0][0] + self.proportions, self.coords[0][1]]
        elif self.direction == "up":
            newcoord = [self.coords[0][0], self.coords[0][1] - self.proportions]
        elif self.direction == "down":
            newcoord = [self.coords[0][0], self.coords[0][1] + self.proportions]
        if newcoord in self.coords or newcoord[0] < 0 or newcoord[0] > (Win.proportions - self.velocity) or newcoord[
            1] < 0 or newcoord[1] > (Win.proportions - self.velocity):
            self.death()
        else:
            self.coords.insert(0, newcoord)
            if newcoord == [A.x, A.y] and Win.apple:
                Win.apple = False
                Win.score += 1
                Win.scorelable = Win.font.render(f"{Win.score}", True, (255, 255, 255))
            else:
                self.coords.pop()

    def death(self):
        pygame.mixer.Sound.play(self.deathsound)
        self.alive = False
        Win.screen.fill((255, 0, 0))
        for coord in self.coords:
            pygame.draw.rect(Win.screen, (0, 0, 0), (coord[0], coord[1], self.proportions, self.proportions))
        pygame.display.update()
        S.coords = [[Win.proportions / 2, Win.proportions / 2]]
        Win.apple = False
        self.alive = False
        pygame.time.delay(2000)

        self.direction = ""
        Win.score = 0
        Win.scorelable = Win.font.render(f"{Win.score}", True, (255, 255, 255))


class Apple:
    def __init__(self):
        self.x = 0
        self.y = 0

    def create(self):
        creating = True
        while creating:
            self.x = random.randint(0, Win.scale - 1) * (Win.proportions / Win.scale)
            self.y = random.randint(0, Win.scale - 1) * (Win.proportions / Win.scale)
            if [self.x, self.y] in S.coords:
                pass
            else:
                creating = False
                Win.apple = True


Win = Window()
S = Snake()
A = Apple()
Win.mainloop()
