import random
from builtins import print, property

import pygame # importation de la librairie pygame
import space
import sys # pour fermer correctement l'application

def blitPlayer():
    screen.blit(player.img, player.pos)  # appel de la fonction qui dessine le vaisseau du joueur


    # Bar de point de vie
    pygame.draw.rect(screen, (255, 100, 100),
                     (player.pos[0] -10, player.pos[1], 10 , player.img.get_size()[1]))
    pygame.draw.rect(screen, (00, 255, 00), (
        player.pos[0] - 10, player.pos[1], 10, player.img.get_size()[1] * (player.hp / player.hpMax)))

    #bar de rechagement de ball
    nextAttactTime = player.lastAttack + player.attacksSpeed[player.ballType] - pygame.time.get_ticks()
    if nextAttactTime > 0:
        pygame.draw.rect(screen, (20, 40, 100), (
            player.pos[0] + player.img.get_size()[0], player.pos[1], 10, player.img.get_size()[1] * (nextAttactTime/player.attacksSpeed[player.ballType])))

def blitScore():
    # AFFICHAGE DU SCORE
    bestScoreText = pygame.font.SysFont('corbel', 40, True).render('meilleur score : ' + str(player.bestScore), True,
                                                                   [80, 80, 80])
    screen.blit(bestScoreText, ((screen.get_width() - bestScoreText.get_width()) // 2, 0))
    scoreText = pygame.font.SysFont('corbel', 40, True).render('score : ' + str(player.score), True, [10, 180, 40])
    screen.blit(scoreText, (screen.get_width() - scoreText.get_width(), 10))

def pauseSytem():
    global isSettings
    global isPaused
    global gameover
    pygame.mixer.Sound("pause.wav").play()

    #reset le jeu en cas de game overt
    if gameover: gameReset()
    #sors des settings
    elif isSettings: isSettings = not isPaused
    #sort de paus
    else: isPaused = not isPaused

    #met la musique a jour
    if isPaused:
        pygame.mixer.music.load('musicMenu.mp3')
    else: pygame.mixer.music.load('musicGame.mp3')
    pygame.mixer.music.play(-1)

def waveSpawn(waveToSpawn):
    #CHANGE DE VAGUE MET A JOUR LA LIST D4ENNEMIS
    for ennemisType in waveToSpawn.keys():
        nb = waveToSpawn[ennemisType]
        for a in range(nb):
            vaisseau = space.Ennemi(ennemisType)
            listeEnnemis.append(vaisseau)

def gameReset():
    #REMET TOUT LES VARIABLE DU JEU A 0
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
waves = [ # differente waves
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


#BAR SOUND SETTINGS
soudBarText = font.render('Music :', True, [20, 20, 20])
soundBar = pygame.rect.Rect(screen.get_size()[0]//2 - 100, screen.get_size()[1]//2 - 20, 200, 20)
soundBarCursor = pygame.rect.Rect(20, 15, 20, 30)

#BTN MENU
btnPause = space.Button( [screen.get_size()[0]//2,screen.get_size()[1]//3], 'pause')
btnLeave = space.Button([screen.get_size()[0]//2,screen.get_size()[1]//1.5], 'leave')
btnSettings = space.Button([25,25], img=pygame.transform.scale(pygame.image.load('settings.png'), (50, 50)))
crossbtn = space.Button([screen.get_size()[0] - 25, 25], img=pygame.transform.scale(pygame.image.load('cross.png'), (50, 50)))


#MUSIC MENU
pygame.mixer.music.load('musicMenu.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1)

waveSpawn(waves[actualyWave]) # cré la permiere vague

Clock = pygame.time.Clock()

### BOUCLE DE JEU  ###
running = True # variable pour laisser la fenêtre ouverte
isPaused = True
isSettings = False
gameover = False

pygame.mouse.set_visible(False) # Curseur windows invisible

while running : # boucle infinie pour laisser la fenêtre ouverte
    # dessin du fond
    screen.blit(fond,(0,0))
    ### Gestion des événements   ###
    for event in pygame.event.get(): # parcours de tous les event pygame dans cette fenêtre
        if event.type == pygame.QUIT : # si l'événement est le clic sur la fermeture de la fenêtre
            f = open('data.pirate', 'w')
            f.write(str(player.bestScore))
            running = False # running est sur False
            sys.exit() # pour fermer correctement

       # gestion du clavier

        elif event.type == pygame.MOUSEBUTTONUP:
            if isPaused:
                isPaused = btnPause.onClick(isPaused) # click sur paus
                running = btnLeave.onClick(running) #click sur keave
                isSettings = btnSettings.onClick(isSettings) # click sur settings
                if crossbtn.onClick(): pauseSytem() # click sur la croix
        if event.type == pygame.KEYUP : # si une touche a été tapée KEYUP quand on relache la touche
            if event.key == pygame.K_LEFT : # si la touche est la fleche gauche
                player.leftPressed = False
            if event.key == pygame.K_RIGHT : # si la touche est la fleche droite
                player.rightPressed = False
        elif event.type == pygame.KEYDOWN : # si une touche a été tapée KEYUP quand on relache la touche
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
        if bonusTime <= pygame.time.get_ticks(): # si il est temps de créé un bonus
            bonusTime = pygame.time.get_ticks() + random.randint(2000, 5000) # nouveau temps du prochain bonus
            bonus.append(space.Bonus(player.ballImg)) # Cré le bonus
        player.systemeTir(listeEnnemis)
        # placement des objets
        # le joueur
        player.update() # appel de la fonction qui dessine le vaisseau du joueur
        # la balle
        for id in range(len(player.tirs)):
            tir = player.tirs[id]
            screen.blit(tir.img, tir.pos)
            if not tir.bouger():
                del player.tirs[id] #enlever la balles
                break
        blitPlayer()

        # les ennemis
        temp = []
        for ennemi in listeEnnemis:
            if ennemi.avancer(player): # si on les ennemis attein le bout
                player.score -= 2
                pygame.mixer.Sound("hurt.wav").play()
            else: temp.append(ennemi)
            screen.blit(ennemi.img,ennemi.pos) # appel de la fonction qui dessine le vaisseau du joueur
            pygame.draw.rect(screen, (100, 100, 100), (ennemi.pos[0], ennemi.pos[1] + ennemi.img.get_size()[1], ennemi.img.get_size()[0], 5)) #base de vie max du ennemi
            pygame.draw.rect(screen, (00, 255, 00), (ennemi.pos[0], ennemi.pos[1] + ennemi.img.get_size()[1], ennemi.img.get_size()[0]*(ennemi.hp / ennemi.hpMax), 5)) #bar de vie actuel du ennemi
        listeEnnemis = temp[:]
        for id in range(len(bonus)):
            singleBonus = bonus[id]
            singleBonus.move() #avance les bonus
            screen.blit(singleBonus.img, singleBonus.pos) # les affiche
            if singleBonus.touchPlayer(player):
                del bonus[id] #tue le bonus
                break

        blitScore()

        ballReloaderText = pygame.font.SysFont('corbel', 40, True).render(str(player.reloads[player.ballType]), True, [80, 80, 80]) # Numbre de balles
        screen.blit(ballReloaderText, (screen.get_width() - ballReloaderText.get_width(), screen.get_height()  - player.ballImg[player.ballType].get_height() - ballReloaderText.get_height()))
        screen.blit(player.ballImg[player.ballType], (screen.get_width() - player.ballImg[player.ballType].get_width(), screen.get_height() - player.ballImg[player.ballType].get_height()))

        if len(listeEnnemis) < 1:
            if player.score > 0 and actualyWave + 1 < len(waves): # si on a fni la vague
                actualyWave += 1
                waveSpawn(waves[actualyWave])
            else: #si on a gagné
                isPaused = True
                gameover = True
        if player.hp <= 0: # si on est mort on gameover
            isPaused = True
            gameover = True
    else:
        if gameover:
            if actualyWave >= len(waves) or player.hp <= 0:
                #perdu
                screen.blit(pygame.transform.scale(pygame.image.load('gameover.jpg'), screen.get_size()), (0, 0))
            else:
                #Si on gagne
                blitScore()
                screen.blit(pygame.transform.scale(pygame.image.load('winScreen.jpg'), screen.get_size()), (0, 0))
        elif isSettings:
            soundBarCursor.topleft = [pygame.mixer.music.get_volume() * soundBar.size[0] + soundBar.x, soundBar.y - 5] # pos du curseur est celle du niveau du son sur la bar
            screen.blit(soudBarText, [soundBar.centerx - soudBarText.get_width()//2 , soundBar.y - 30])
            pygame.draw.rect(screen, [25, 10, 200], soundBar) #blit la bar du son
            pygame.draw.rect(screen, [30, 30, 39], soundBarCursor) # blit l curseur du son
            if pygame.mouse.get_pressed()[0]:
                if soundBar.topleft[0] < pygame.mouse.get_pos()[0] < soundBar.topleft[0] + soundBar.size[0] and soundBar.topleft[1] < pygame.mouse.get_pos()[1] < soundBar.topleft[1] + soundBar.size[1]: # si le curseur est sur la bar
                    pygame.mixer.music.set_volume((pygame.mouse.get_pos()[0] - soundBar.left) / soundBar.size[0]) # change le son
        else: # Si on est juste en pause
            screen.blit(pygame.transform.scale(pygame.image.load('control.png'), (300, 300)), (0, screen.get_height()//3)) # image des control
            screen.blit(btnSettings.img, btnSettings.pos) #btn settings
            screen.blit(btnPause.text, btnPause.pos) #btn continuer
            screen.blit(btnLeave.text, btnLeave.pos) #btn leave

        screen.blit(crossbtn.img, crossbtn.pos)


    #CURSEUR PERSONNALISER
    screen.blit(pygame.transform.scale(pygame.image.load('cursor.png'), (32, 32)), pygame.mouse.get_pos())

    Clock.tick(60)
    pygame.display.update() # pour ajouter tout changement à l'écran