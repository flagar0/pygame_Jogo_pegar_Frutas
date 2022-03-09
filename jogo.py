import os
import pygame as pg
from classes import *
import math
import pygame_menu
from os.path import exists as file_exists
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
##############################
# Fazer game over,  , pontiacao
#
##################################


def main():
    try:
        menu.disable()
    except:
        print("travou")
    # Cria fonte
    pg.font.init()
    myfont = pg.font.SysFont('Comic Sans MS', 30)

    # Cria Background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187))

    screen.blit(background, (0, 0))
    pg.display.flip()

    # Gera os elementos
    cesto = Cesta()
    allsprites = pg.sprite.RenderPlain((cesto))
    fruta = pg.sprite.Group()

    # Seta variavies
    clock = pg.time.Clock()
    jogando = True
    cria_fruta = True
    pontos = 0
    dif = 0
    frutas_alive = 0
    vidas = 3
    while(jogando):
        clock.tick(60)

        # Cria Fruta
        if(cria_fruta):
            qtd = math.floor(dif)
            if(qtd == 0):
                fruta.add(Frutas(dif))
                frutas_alive += 1
            elif(frutas_alive <= 10):
                for n in range(0, 1+qtd-(frutas_alive)):
                    fruta.add(Frutas(dif))
                    frutas_alive += 1

            fruta_render = pg.sprite.RenderPlain((fruta))
            cria_fruta = False

        # Lista de eventos
        for event in pg.event.get():
            if(event.type == pg.QUIT):
                jogando = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                jogando = False

        # Colisao
        for colisoes in fruta.sprites():
            colidiu = colisoes.bateu(cesto)
            if(colidiu):
                pontos += 1
                if(colisoes.bomba == False and colisoes.hamburguer == False):
                    pg.mixer.music.load('data/Charge2.mp3')
                    pg.mixer.music.play(0)

                if(dif < 5):
                    dif += 0.2

                if(colisoes.bomba == True):
                    vidas -= 1
                    pontos -= 1
                    pg.mixer.music.load('data/Door.mp3')
                    pg.mixer.music.play(0)

                if(colisoes.hamburguer == True):
                    if(vidas > 2):
                        vidas = 3
                        pontos += 2
                    else:
                        vidas += 1
                        pontos += 2
                    pg.mixer.music.load('data/Find_Money.mp3')
                    pg.mixer.music.play(0)

                frutas_alive -= 1
                # if(frutas_alive == 0):
                cria_fruta = True

        # Deixou passar
        for f in fruta.sprites():
            if(f.rect.topleft[1] >= 620):
                f.kill()
                frutas_alive -= 1
                if(f.bomba == False and f.hamburguer == False):
                    pontos -= 1

                if(vidas >= 0 and f.bomba == False and f.hamburguer == False):
                    vidas -= 0.25

                if(dif > 0):
                    dif -= 0.2
                cria_fruta = True

        # Vidas perdidas
        if(vidas <= 4):
            coracoes = controle_vida(vidas)

        if(vidas == 0):
            jogando = False
            perdeu(pontos)
        else:
            try:
                # Atualiza sprites
                allsprites.update()
                fruta_render.update()

                # Renderiza tudo
                textsurface = myfont.render(str(pontos), False, (0, 0, 0))

                screen.blit(background, (0, 0))
                screen.blit(textsurface, (30, 540))
                allsprites.draw(screen)
                fruta_render.draw(screen)
                coracoes.draw(screen)
                pg.display.flip()
            except:
                jogando = False
                perdeu(pontos)


def perdeu(pts):
    try:
        menu.disable()
    except:
        print("travou")
    # Cria Background
    background2 = pg.Surface(screen.get_size())
    background2 = background2.convert()
    background2.fill((0, 0, 0))

    screen.blit(background2, (0, 0))
    pg.display.flip()

    # Pega pontuacao antiga
    old_pts, record = pega_pontos(pts)

    if(record == True):
        string_pts = str(pts) + "* Novo Record!"
    elif(record == False):
        string_pts = str(old_pts)
        string_pts = string_pts[2:len(string_pts)-1]

    # Cria fonte
    pg.font.init()
    myfont = pg.font.SysFont('Comic Sans MS', 60)
    myfont2 = pg.font.SysFont('Comic Sans MS', 45)
    myfont3 = pg.font.SysFont('Comic Sans MS', 35)

    # Gera botao
    button = pg.Rect(100, 370, 290, 70)
    button2 = pg.Rect(100, 450, 100, 70)

    espera = True
    clock = pg.time.Clock()
    while(espera):
        clock.tick(60)

        for event in pg.event.get():
            if(event.type == pg.QUIT):
                espera = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                espera = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button.collidepoint(mouse_pos):
                    espera = False
                    main()

                if button2.collidepoint(mouse_pos):
                    espera = False

        # Renderiza tudo
        screen.blit(background2, (0, 0))

        # Gera textos
        textsurface = myfont.render("Voce Perdeu :(", False, (255, 255, 255))
        textsurface2 = myfont2.render(
            "Total de pontos: " + str(pts), False, (255, 255, 255))

        pontos_antigos = myfont3.render(
            "Record: "+string_pts, False, (255, 0, 0))

        jogar_dnv = myfont2.render("Jogar denovo", False, (255, 255, 255))
        sair = myfont2.render("Sair", False, (0, 0, 0))

        # Carrega
        pg.draw.rect(screen, [255, 0, 0], button)
        pg.draw.rect(screen, [255, 255, 51], button2)
        screen.blit(textsurface, (100, 50))
        screen.blit(textsurface2, (100, 170))
        screen.blit(pontos_antigos, (100, 230))
        screen.blit(jogar_dnv, (105, 370))
        screen.blit(sair, (105, 455))

        pg.display.flip()



def menus():
    try:
        menu_sobre.disable()
    except:
        print('oi')
    finally:
        tema = pygame_menu.themes.THEME_SOLARIZED.copy()

        fonte = pygame_menu.font.FONT_FRANCHISE
        tema.widget_font = fonte
        tema.title_font = fonte

        tema.title_font_size = 90

        tema.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE

        global menu
        menu = pygame_menu.Menu("Pega as Fruta", 600, 600,
                                theme=tema)

        menu.add.button('Jogar', main, font_size=90,
                        cursor=pg.SYSTEM_CURSOR_HAND)
        menu.add.button('Sobre', sobre, font_size=90,
                        cursor=pg.SYSTEM_CURSOR_HAND)
        menu.add.button('Sair', pygame_menu.events.EXIT, font_size=90)
        menu.add.url('https://github.com/flagar0', 'Por:Flagar0',
                     align=pygame_menu.locals.ALIGN_LEFT)
        menu.mainloop(screen)


def sobre():
    menu.disable()

    tema2 = pygame_menu.themes.THEME_SOLARIZED.copy()

    fonte = pygame_menu.font.FONT_FRANCHISE
    tema2.widget_font = fonte
    tema2.title_font = fonte

    tema2.title_font_size = 90

    tema2.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE

    global menu_sobre
    menu_sobre = pygame_menu.Menu("Sobre", 600, 600,
                                  theme=tema2)

    texto = 'Pegue todas as frutas / \n' \
        'Caso deixe alguma cair perdera vida e pontos / ' \
            'Pegue os hamburgueres para ganhar pontos e restaurar a vida / ' \
        'Nao pegue as bombas'

    menu_sobre.add.label(texto, max_char=30, font_size=55)
    menu_sobre.add.button('Voltar', menus,       # Link to exit action
                          align=pygame_menu.locals.ALIGN_RIGHT)

    menu_sobre.mainloop(screen)


def pega_pontos(new_pts):
    if file_exists('data/pontuacao.txt'):
        # Abre e pega dados do arquio
        AbrindoR = open("data/pontuacao.txt", 'r')
        for valor in AbrindoR:
            dec_old_pts = valor[2:len(valor)-1]
        AbrindoR.close()

        # Desencriptacao
        senha = b'Z9y9pinqq5RS8ZDAsVBfB-U3Prq1CP7ghQVEusoY6v8='
        print(senha)
        fernet = Fernet(senha)
        b2 = bytes(dec_old_pts, 'utf-8')
        try:
            old_pts = fernet.decrypt(b2)
        except:
            print("error nao consegui ler")
            old_pts = "0"

        # Reescreve arquivo com a nova pontuacao
        if(new_pts > int(old_pts)):
            # Encipta
            b3 = bytes(str(new_pts), 'utf-8')
            enc_new_pts = fernet.encrypt(b3)

            EscrevendoW = open("data/pontuacao.txt", 'w')
            EscrevendoW.write(str(enc_new_pts))
            EscrevendoW.close()
            return old_pts, True  # bool para record
        else:
            return old_pts, False
    else:
        # Encipta
        senha = b'Z9y9pinqq5RS8ZDAsVBfB-U3Prq1CP7ghQVEusoY6v8='
        print(senha)
        fernet = Fernet(senha)
        b = bytes(str(new_pts), 'utf-8')
        enc_new_pts2 = fernet.encrypt(b)

        # Cria e salva arquivo
        CriandoArq = open("data/pontuacao.txt", 'w+')
        CriandoArq.write(str(enc_new_pts2))
        CriandoArq.close()
        return "0", True


if __name__ == "__main__":
    # Cria janela
    pg.init()
    screen = pg.display.set_mode((600, 600), pg.SCALED)
    # pg.mouse.set_visible(False)
    menus()
