import random
from builtins import print, property

import pygame # importation de la librairie pygame
import space
import sys # pour fermer correctement l'application

def pauseSytem():
    global isSettings
    global isPaused
    global gameover
    pygame.mixer.Sound("pause.wav").play()
    if gameover: gameReset()
    elif isSettings: isSettings = not isPaused
    else: isPaused = not isPaused
    if isPaused:
        pygame.mixer.music.load('musicMenu.mp3')
    else: pygame.mixer.music.load('musicGame.mp3')
    pygame.mixer.music.play(-1)

def waveSpawn(waveToSpawn):
    for ennemisType in waveToSpawn.keys():
        nb = waveToSpawn[ennemisType]
        for a in range(nb):
            vaisseau = space.Ennemi(ennemisType)
            listeEnnemis.append(vaisseau)

def gameReset():
    global player, listeEnnemis, actualyWave, bonusTime, gameover
    player = space.Joueur()
    actualyWave = 0
    bonusTime = 0
    gameover = 0
    waveSpawn(waves[actualyWave])


# lancement des modules inclus dans pygame
pygame.init() 

# création d'une fenêtre de 800 par 600
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Marins Invader")
# chargement de l'image de fond
fond = pygame.transform.scale2x(pygame.image.load('background.jpg'))

font = pygame.font.SysFont('cambria', 30, True)
# creation du joueur
player = space.Joueur()
# creation des ennemis
listeEnnemis = []

actualyWave = 0

waves = [
    {0 : 5, 1 : 0, 2 : 0,},
    {0 : 7, 1 : 1, 2 : 0,},
    {0 : 7, 1 : 2,2 : 0,},
    {0 : 10,1 : 2,2 : 1,},
    {0 : 13,1 : 5,2 : 1,},
    {0 : 13,1 : 6,2 : 2,},
    {0 : 15,1 : 8,2 : 2,},
    {0 : 17,1 : 8,2 : 3,},
    {0 : 20,1 : 9,2 : 3,},
    {0 : 20,1 : 10,2 : 4,},
    {0 : 23,1 : 10,2 : 5,},
    {0 : 25,1 : 10,2 : 5,},
    {0 : 25,1 : 12,2 : 7,},
]
#Bonus
bonusTime = 0
bonus = [space.Bonus(player.ballImg)]

crossbtn = space.Button([screen.get_size()[0] - 25, 25], img=pygame.transform.scale(pygame.image.load('cross.png'), (50, 50)))

soudBarText = font.render('Music :', True, [20, 20, 20])
soundBar = pygame.rect.Rect(screen.get_size()[0]//2 - 100, screen.get_size()[1]//2 - 20, 200, 20)
soundBarCursor = pygame.rect.Rect(20, 15, 20, 30)

btnPause = space.Button( [screen.get_size()[0]//2,screen.get_size()[1]//3], 'pause')
btnLeave = space.Button([screen.get_size()[0]//2,screen.get_size()[1]//1.5], 'leave')
btnSettings = space.Button([25,25], img=pygame.transform.scale(pygame.image.load('settings.png'), (50, 50)))

gameover = False

pygame.mixer.music.load('musicMenu.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1)

waveSpawn(waves[actualyWave])

Clock = pygame.time.Clock()

### BOUCLE DE JEU  ###
running = True # variable pour laisser la fenêtre ouverte
isPaused = True
isMenu = True
isMarket = False
isSettings = False

while running : # boucle infinie pour laisser la fenêtre ouverte
    # dessin du fond
    screen.blit(fond,(0,0))
    ### Gestion des événements  ###
    for event in pygame.event.get(): # parcours de tous les event pygame dans cette fenêtre
        if event.type == pygame.QUIT : # si l'événement est le clic sur la fermeture de la fenêtre
            f = open('data.pirate', 'w')
            f.write(str(player.bestScore))
            running = False # running est sur False
            sys.exit() # pour fermer correctement

       # gestion du clavier
        if event.type == pygame.KEYUP : # si une touche a été tapée KEYUP quand on relache la touche
            if event.key == pygame.K_LEFT : # si la touche est la fleche gauche
                player.leftPressed = False
            if event.key == pygame.K_RIGHT : # si la touche est la fleche droite
                player.rightPressed = False
        if event.type == pygame.KEYDOWN : # si une touche a été tapée KEYUP quand on relache la touche
            if event.key == pygame.K_LEFT : # si la touche est la fleche gauche
                player.leftPressed = True
            if event.key == pygame.K_RIGHT : # si la touche est la fleche droite
                player.rightPressed = True
            if event.key == pygame.K_UP:
                player.changeBallTypes(1)
            if event.key == pygame.K_DOWN:
                player.changeBallTypes(-1)
            if event.key == pygame.K_SPACE : # espace pour tirer
                player.tirer()
                if isPaused and not gameover :pauseSytem()
            if event.key == pygame.K_ESCAPE:pauseSytem()

        else:
            player.sens=0

    ### Actualisation de la scene ###
    # Gestions des collisions

    if not isPaused:
        if bonusTime <= pygame.time.get_ticks():
            bonusTime = pygame.time.get_ticks() + random.randint(2000, 5000)
            bonus.append(space.Bonus(player.ballImg))
        player.systemeTir(listeEnnemis)
        # placement des objets
        # le joueur
        player.update() # appel de la fonction qui dessine le vaisseau du joueur
        # la balle
        for id in range(len(player.tirs)):
            tir = player.tirs[id]
            screen.blit(tir.img, tir.pos)
            if not tir.bouger():
                del player.tirs[id]
                break
                print("bloquer")
        screen.blit(player.img, player.pos) # appel de la fonction qui dessine le vaisseau du joueur
        # les ennemis
        temp = []
        for ennemi in listeEnnemis:
            if ennemi.avancer():
                player.score -= 2
                pygame.mixer.Sound("hurt.wav").play()
            else: temp.append(ennemi)
            screen.blit(ennemi.img,ennemi.pos) # appel de la fonction qui dessine le vaisseau du joueur
            pygame.draw.rect(screen, (100, 100, 100), (ennemi.pos[0], ennemi.pos[1] + ennemi.img.get_size()[1], ennemi.img.get_size()[0], 5))
            pygame.draw.rect(screen, (00, 255, 00), (ennemi.pos[0], ennemi.pos[1] + ennemi.img.get_size()[1], ennemi.img.get_size()[0]*(ennemi.hp / ennemi.hpMax), 5))
        listeEnnemis = temp[:]
        for id in range(len(bonus)):
            singleBonus = bonus[id]
            singleBonus.move()
            screen.blit(singleBonus.img, singleBonus.pos)
            if singleBonus.touchPlayer(player):
                del bonus[id]
                break

        #AFFICHAGE DU SCORE
        bestScoreText = pygame.font.SysFont('corbel', 40, True).render('meilleur score : ' + str(player.bestScore), True, [80, 80, 80])
        screen.blit(bestScoreText, ((screen.get_width() - bestScoreText.get_width())//2, 0))
        scoreText = pygame.font.SysFont('corbel', 40, True).render('score : ' + str(player.score), True, [10, 180, 40])
        screen.blit(scoreText, (screen.get_width() - scoreText.get_width(), 10))
        ballReloaderText = pygame.font.SysFont('corbel', 40, True).render(str(player.reloads[player.ballType]), True, [80, 80, 80])
        screen.blit(ballReloaderText, (screen.get_width() - ballReloaderText.get_width(), screen.get_height()  - player.ballImg[player.ballType].get_height() - ballReloaderText.get_height()))
        screen.blit(player.ballImg[player.ballType], (screen.get_width() - player.ballImg[player.ballType].get_width(), screen.get_height() - player.ballImg[player.ballType].get_height()))

        if len(listeEnnemis) < 1:
            if player.score > 0:
                actualyWave += 1
                waveSpawn(waves[actualyWave])
            else:
                isPaused = True
                gameover = True
    else:

        if gameover:
            screen.blit(pygame.transform.scale(pygame.image.load('gameover.jpg'), screen.get_size()), (0, 0))
        elif isSettings:
            soundBarCursor.topleft = [pygame.mixer.music.get_volume() * soundBar.size[0] + soundBar.x, soundBar.y - 5]
            screen.blit(soudBarText, [soundBar.centerx - soudBarText.get_width()//2 , soundBar.y - 30])
            pygame.draw.rect(screen, [25, 10, 200], soundBar)
            pygame.draw.rect(screen, [30, 30, 39], soundBarCursor)
            if pygame.mouse.get_pressed()[0]:
                if soundBar.topleft[0] < pygame.mouse.get_pos()[0] < soundBar.topleft[0] + soundBar.size[0] and soundBar.topleft[1] < pygame.mouse.get_pos()[1] < soundBar.topleft[1] + soundBar.size[1]:
                    pygame.mixer.music.set_volume((pygame.mouse.get_pos()[0] - soundBar.left) / soundBar.size[0])
        else:
            screen.blit(pygame.transform.scale(pygame.image.load('control.png'), (300, 300)), (0, screen.get_height()//3))
            screen.blit(btnSettings.img, btnSettings.pos)
            screen.blit(btnPause.text, btnPause.pos)
            screen.blit(btnLeave.text, btnLeave.pos)
            if pygame.mouse.get_pressed(3)[0]:
                isPaused = btnPause.onClick(isPaused)
                running = btnLeave.onClick(running)
                isSettings = btnSettings.onClick(isSettings)

        screen.blit(crossbtn.img, crossbtn.pos)
        if pygame.mouse.get_pressed()[0]:
            if crossbtn.onClick(): pauseSytem()
    Clock.tick(130)
    pygame.display.update() # pour ajouter tout changement à l'écran