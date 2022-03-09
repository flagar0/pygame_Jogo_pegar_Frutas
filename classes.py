import os
import pygame as pg
import random
from random import randint

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()




class Cesta(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("Assets/bowl.png",-1, scale=3)
        self.fist_offset = (-45,-30)
        self.rect.inflate_ip(-20, -20)

    def update(self):
        pos = pg.mouse.get_pos()
        if(pos[1]>=300):
            self.rect.topleft = pos
            self.rect.move_ip(self.fist_offset)


class Frutas(pg.sprite.Sprite):
    def __init__(self,vel):
        pg.sprite.Sprite.__init__(self)
        self.frame =0
        #Gera img aleatoria
        img = randint(0,4)

        #Gera bomba aleatoria
        ale = randint(1,6)
        ale2= randint(1,10)
        if(ale ==5):
            self.bomba = True
            self.hamburguer = False
            self.image, self.rect = load_image("Assets/bomba1.png",-1,scale=4)
            self.imgs = []
            self.imgs.append(load_image("Assets/bomba1.png",-1,scale=4))
            self.imgs.append(load_image("Assets/bomba2.png",-1,scale=4))

        elif(ale2 ==2):
            self.bomba = False
            self.hamburguer = True
            self.image, self.rect = load_image("Assets/Foods/Food_27.png",-1,scale=4)
        else:
            self.bomba = False
            self.hamburguer = False
            self.image, self.rect = load_image("Assets/Foods/food_"+ str(img*6) +".png",-1,scale=4)

        self.rect.inflate_ip(-17, -50)

        #Gera posicao aleatoria
        posx = randint(50, 560)
        posy = randint(1,100)

        self.rect.topleft = posx, posy
        
        #Movimento aleatorio
        rnd = random.uniform(1.5,3)
        self.move = (round(rnd,2))+vel


    def update(self):
        if(self.bomba==True):
            self.troca_foto()
        self._move()

    def _move(self):
        newpos = self.rect.move((0,self.move))
        self.rect = newpos

    def bateu(self,onde):
        if(pg.sprite.collide_rect(self,onde)):
            self.kill()
            return True

    def troca_foto(self):
        old_rect = self.rect
        if(self.frame ==0):
                self.frame +=1
        elif(self.frame==1):
                self.frame -=1
        self.image, self.rect = self.imgs[self.frame]
        self.rect = old_rect


class Vidas(pg.sprite.Sprite):
    def __init__(self,posx,posy,vida):
        pg.sprite.Sprite.__init__(self)

        # vida = 4 cheia vida = 1 só 1/4 de coracao
        if(vida == 4):
            self.image, self.rect = load_image("Assets/cora1.png",-1,scale=3)
        elif(vida == 3):
            self.image, self.rect = load_image("Assets/cora2.png",-1,scale=3)
        elif(vida == 2):
            self.image, self.rect = load_image("Assets/cora3.png",-1,scale=3)
        elif(vida == 1):
            self.image, self.rect = load_image("Assets/cora4.png",-1,scale=3)

        self.rect.topleft = posx, posy

def controle_vida(life):
    #vida = 3
    if(life ==3):
        heart1 = Vidas(10,20,4)
        heart2 = Vidas(60,20,4)
        heart3 = Vidas(110,20,4)
        return pg.sprite.RenderPlain((heart1,heart2,heart3))

    if(life==2.75):
        heart1 = Vidas(10,20,4)
        heart2 = Vidas(60,20,4)
        heart3 = Vidas(110,20,3)
        return pg.sprite.RenderPlain((heart1,heart2,heart3))

    if(life==2.50):
        heart1 = Vidas(10,20,4)
        heart2 = Vidas(60,20,4)
        heart3 = Vidas(110,20,2)
        return pg.sprite.RenderPlain((heart1,heart2,heart3))

    if(life==2.25):
        heart1 = Vidas(10,20,4)
        heart2 = Vidas(60,20,4)
        heart3 = Vidas(110,20,1)
        return pg.sprite.RenderPlain((heart1,heart2,heart3))

    if(life==2):
        heart1 = Vidas(10,20,4)
        heart2 = Vidas(60,20,4)
        return pg.sprite.RenderPlain((heart1,heart2))

    if(life==1.75):
        heart1 = Vidas(10,20,4)
        heart2 = Vidas(60,20,3)
        return pg.sprite.RenderPlain((heart1,heart2))

    if(life==1.50):
        heart1 = Vidas(10,20,4)
        heart2 = Vidas(60,20,2)
        return pg.sprite.RenderPlain((heart1,heart2))

    if(life==1.25):
        heart1 = Vidas(10,20,4)
        heart2 = Vidas(60,20,1)
        return pg.sprite.RenderPlain((heart1,heart2))

    if(life==1):
        heart1 = Vidas(10,20,4)
        return pg.sprite.RenderPlain((heart1))

    if(life==0.75):
        heart1 = Vidas(10,20,3)
        return pg.sprite.RenderPlain((heart1))

    if(life==0.5):
        heart1 = Vidas(10,20,2)
        return pg.sprite.RenderPlain((heart1))

    if(life==0.25):
        heart1 = Vidas(10,20,1)
        return pg.sprite.RenderPlain((heart1))

