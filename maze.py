#создай игру "Лабиринт"!
from pygame import *
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
   def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >5:
            self.rect.x -= self.speed 
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed 
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed


class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"


        if self.direction == "left":
            self.rect.x -= self.speed 
        else:
            self.rect.x += self.speed 


class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width 
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Лабиринт")
background = transform.scale(image.load('background.jpg'), (win_width, win_height))


mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

w1 = Wall(119, 119, 0, 100, 40, 10, 350)
w2 = Wall(119, 119, 0, 100, 40, 500, 10)
w3 = Wall(119, 119, 0, 200, 145, 10, 500)
w4 = Wall(119, 119, 0, 200, 145, 350, 10)
w5 = Wall(119, 119, 0, 450, 145, 10, 500)
player = Player("hero.png", 5, win_height - 80, 5)
cyborg = Enemy("cyborg.png", win_width - 80 , 280, 2)
treasure = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (255, 0, 0))


clock = time.Clock()
FPS = 60

game = True
finish = False 
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        cyborg.update()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()

        player.reset()
        cyborg.reset()
        treasure.reset()

        if sprite.collide_rect(player, treasure):
            window.blit(win, (200, 200))
            finish = True 
            money.play()

        if sprite.collide_rect(player, cyborg) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3) or sprite.collide_rect(player, w4) or sprite.collide_rect(player, w5):
            window.blit(lose, (200, 200))
            finish = True
            kick.play()

    display.update()
    clock.tick(FPS)