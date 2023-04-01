from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.Font(None, 36)
img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"

enemy_list = ['ufo.png', 'asteroid.png', 'images.png']


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        '''
    def change_fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx +10, self.rect.top, 15, 20, -15)
        bullets.add(bullet)'''


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
 
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global store
        global max_lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        '''
        keys = key.get_pressed()
        if keys[K_UP]:
            self.change_fire()'''
 
        
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

store = 0
lost = 0
max_lost = 100


ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
    rand_num = randint(0, 2)
    if rand_num == 2:
        monster = Enemy(enemy_list[rand_num], randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monster = Enemy(enemy_list[rand_num], randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
        elif e.type == KEYDOWN:
            if e.key == K_1:
                fire_sound.play()
                ship.fire()

        

    if not finish:
        window.blit(background, (0,0))
        text = font2.render("Счет:" + str(store), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10,50))

        win_text = font2.render("вы выйграли" , 1, (255, 255, 255))

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        display.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            store = store + 1
            monster = Enemy(enemy_list[rand_num], randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(text_lose, (200, 200))

        if store >= max_lost:
            finish = True
            window.blit(win_text, (200, 200))

    else:
        finish = False
        store = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

    if lost > 1000:
        text_lose = font2.render("пропущено" + str(lost), 1, (255, 0, 0))
        window.blit(text_lose, (10, 50))  
        run = True
        

    time.delay(50)

display.update()