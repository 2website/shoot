from pygame import *
from random import randint


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < w - 85:
            self.rect.x += self.speed

    def fire(self):
        pass


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > w:
            self.rect.y = 0
            self.rect.x = randint(0, w - 85)
            if self in monsters:
                lost += 1
                self.speed = randint(2, 5)
            if self in asteroids:
                self.speed = randint(2, 3)



class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
        global score
        for monster in monsters:
            if sprite.collide_rect(self, monster):
                self.kill()
                monster.rect.y = 0
                monster.rect.x = randint(0, w - 85)
                monster.speed = randint(2, 5)
                score += 1


w = 800
h = 800
lost = 0
score = 0

window = display.set_mode((w, h))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (w, h))
hero = Player('rocket.png', 0, h - 105, 25, 90, 80)

monsters = sprite.Group()
for i in range(6):
    monster = Enemy('ufo.png', randint(0, w - 105), 0, randint(2, 5), 90, 70)
    monster.add(monsters)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(0, w - 105), 0, randint(2, 3), 90, 70)
    asteroids.add(asteroid)

bullets = sprite.Group()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

font.init()
font = font.Font(None, 36)

clock = time.Clock()
FPS = 60

num_fire = 0
rel_time = False
ticks = 0
run = True
finish = False
while run:
    if not finish:
        window.blit(background, (0, 0))
        hero.reset()
        hero.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        text_win = font.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text_win, (0, 0))
        text_lose = font.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (0, 36))

        if score >= 10:
            finish = True
            txt_win = font.render('You won', 1, (255, 255, 255))
            window.blit(txt_win, (w // 2 - 50, h // 2 - 50))
        if lost >= 3 or sprite.spritecollide(hero, monsters, False) or sprite.spritecollide(hero, asteroids, False):
            finish = True
            txt_lose = font.render('You lose', 1, (255, 255, 255))
            window.blit(txt_lose, (w // 2 - 50, h // 2 - 50))
        display.update()
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and not rel_time:
                    bullet = Bullet('bullet.png', hero.rect.centerx, hero.rect.top, 10, 10, 20)
                    bullets.add(bullet)
                    num_fire += 1
                if num_fire >= 5 and not rel_time:
                    rel_time = True
                if rel_time and ticks < 5:
                    ticks += 1
                if rel_time and ticks >= 5:
                    ticks = 0
                    num_fire = 0
                    rel_time = False
            if e.key == K_r:
                hero.rect.x = 350
                for monster in monsters:
                    monster.rect.y = 0
                    monster.rect.x = randint(0, w - 105)
                for asteroid in asteroids:
                    asteroid.rect.y = 0
                    asteroid.rect.x = randint(0, w - 105)
                score = 0
                lost = 0
                ticks = 0
                num_fire = 0
                rel_time = False
                for bullet in bullets:
                    bullet.kill()
                finish = False

    clock.tick(FPS)
