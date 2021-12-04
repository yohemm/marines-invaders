import random
from builtins import print, property

import pygame # importation de la librairie pygame
import space
import sys # pour fermer correctement l'application

def pauseSytem():
    global isPaused
    pygame.mixer.Sound("pause.wav").play()
    isPaused = not isPaused
    if isPaused:
        pygame.mixer.music.load('musicMenu.mp3')
    else: pygame.mixer.music.load('musicGame.mp3')
    pygame.mixer.music.play(-1)


# lancement des modules inclus dans pygame
pygame.init() 

# création d'une fenêtre de 800 par 600
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Marins Invader")
# chargement de l'image de fond
fond = pygame.image.load('background.png')

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

btnPause = space.Button( [screen.get_size()[0]//2,screen.get_size()[1]//3], 'pause')
btnLeave = space.Button([screen.get_size()[0]//2,screen.get_size()[1]//1.5], 'leave')

gameover = False

pygame.mixer.music.load('musicMenu.mp3')
pygame.mixer.music.play(-1)


for indice in waves[0]:
    nb = waves[0][indice]
    print(nb)
    for a in range(nb):
        vaisseau = space.Ennemi(indice)
        listeEnnemis.append(vaisseau)

Clock = pygame.time.Clock()

### BOUCLE DE JEU  ###
running = True # variable pour laisser la fenêtre ouverte
isPaused = True
isMenu = True
isMarket = False
while running : # boucle infinie pour laisser la fenêtre ouverte
    # dessin du fond
    screen.blit(fond,(0,0))
    if bonusTime <= pygame.time.get_ticks():
        bonusTime = pygame.time.get_ticks() + random.randint(2000, 5000)
        bonus.append(space.Bonus(player.ballImg))
        print(bonus)


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
                if isPaused :pauseSytem()
            if event.key == pygame.K_ESCAPE:pauseSytem()

        else:
            player.sens=0

    ### Actualisation de la scene ###
    # Gestions des collisions

    if not isPaused:
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
        bestScoreText = pygame.font.SysFont('corbel', 40, True).render('meilleur score : ' + str(player.bestScore), True, [80, 100, 80])
        screen.blit(bestScoreText, ((screen.get_width() - bestScoreText.get_width())//2, 0))
        scoreText = pygame.font.SysFont('corbel', 40, True).render('score : ' + str(player.score), True, [10, 200, 40])
        screen.blit(scoreText, (screen.get_width() - scoreText.get_width(), 10))
        ballReloaderText = pygame.font.SysFont('corbel', 40, True).render(str(player.reloads[player.ballType]), True, [80, 80, 80])
        screen.blit(ballReloaderText, (screen.get_width() - ballReloaderText.get_width(), screen.get_height()  - player.ballImg[player.ballType].get_height() - ballReloaderText.get_height()))
        screen.blit(player.ballImg[player.ballType], (screen.get_width() - player.ballImg[player.ballType].get_width(), screen.get_height() - player.ballImg[player.ballType].get_height()))

        if len(listeEnnemis) < 1:
            if player.score > 0:
                actualyWave += 1
                for ennemisType in waves[actualyWave].keys():
                    nb = waves[actualyWave][ennemisType]
                    for a in range(nb):
                        vaisseau = space.Ennemi(ennemisType)
                        listeEnnemis.append(vaisseau)
            else:
                isPaused = True
                gameover = True

    elif gameover:
        screen.blit(pygame.transform.scale(pygame.image.load('gameover.jpg'), screen.get_size()), (0, 0))
    else:
        screen.blit(pygame.transform.scale(pygame.image.load('control.png'), (300, 300)), (0, screen.get_height()//3))
        screen.blit(btnPause.text, btnPause.pos)
        screen.blit(btnLeave.text, btnLeave.pos)
        if pygame.mouse.get_pressed(3)[0]:
            isPaused = btnPause.onClick(isPaused)
            running = btnLeave.onClick(running)

    Clock.tick(130)
    pygame.display.update() # pour ajouter tout changement à l'écran