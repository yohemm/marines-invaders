from builtins import print, property

import pygame # importation de la librairie pygame
import space
import sys # pour fermer correctement l'application
import pickle

# lancement des modules inclus dans pygame
pygame.init() 

# création d'une fenêtre de 800 par 600
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Cake Invaders")
# chargement de l'image de fond
fond = pygame.image.load('background.png')

# creation du joueur
player = space.Joueur()
# creation des ennemis
listeEnnemis = []

#Bonus
bonusTime = 0
bonus = [space.Bonus(player.ballImg)]

btnPause = space.Button( [screen.get_size()[0]//2,screen.get_size()[1]//3], 'pause')
btnLeave = space.Button([screen.get_size()[0]//2,screen.get_size()[1]//1.5], 'leave')

btnMarket = space.Button((0, 0), img=pygame.transform.scale(pygame.image.load('market.png'), (60, 60)))
btnLoadGame = space.Button([screen.get_size()[0]//2,screen.get_size()[1]//3], 'Charger la parie')
btnNewGame = space.Button([screen.get_size()[0]//2,screen.get_size()[1]//1.5], 'Nouvelle partie')

for indice in range(space.Ennemi.NbEnnemis):
    vaisseau = space.Ennemi()
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
        bonusTime = pygame.time.get_ticks() + 9000
        bonus.append(space.Bonus(player.ballImg))


    ### Gestion des événements  ###
    for event in pygame.event.get(): # parcours de tous les event pygame dans cette fenêtre
        if event.type == pygame.QUIT : # si l'événement est le clic sur la fermeture de la fenêtre
            running = False # running est sur False
            sys.exit() # pour fermer correctement

       # gestion du clavier
        if event.type == pygame.KEYDOWN : # si une touche a été tapée KEYUP quand on relache la touche
            if event.key == pygame.K_LEFT : # si la touche est la fleche gauche
                player.sens = -1 # on déplace le vaisseau de 1 pixel sur la gauche
            if event.key == pygame.K_RIGHT : # si la touche est la fleche droite
                player.sens =  1 # on déplace le vaisseau de 1 pixel sur la gauche
            if event.key == pygame.K_UP:
                player.changeBallTypes(1)
            if event.key == pygame.K_DOWN:
                player.changeBallTypes(-1)
            if event.key == pygame.K_SPACE : # espace pour tirer
                player.tirer()
            if event.key == pygame.K_ESCAPE:
                pause = not pause

        else:
            player.sens=0

    ### Actualisation de la scene ###
    # Gestions des collisions

    if not isPaused:
        player.systemeTir(listeEnnemis)
        # placement des objets
        # le joueur
        player.deplacer() # appel de la fonction qui dessine le vaisseau du joueur
        # la balle
        for id in range(len(player.tirs)):
            tir = player.tirs[id]
            screen.blit(tir.img,tir.pos)
            if not tir.bouger():
                del player.tirs[id]
                break
                print("bloquer")
        screen.blit(player.img, player.pos) # appel de la fonction qui dessine le vaisseau du joueur
        # les ennemis
        temp = []
        for ennemi in listeEnnemis:
            if ennemi.avancer():
                player.score -= 10
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
        screen.blit(pygame.font.SysFont('corbel', 40, True).render(str(player.score), True, [10, 200, 40],), (screen.get_width() - 80, 10))

    elif isMenu:
        pause = True
        screen.blit(btnMarket.img, btnMarket.pos)

        screen.blit(btnLoadGame.text, btnLoadGame.pos)

        screen.blit(btnNewGame.text, btnNewGame.pos)
        if pygame.mouse.get_pressed(3)[0]:
            isMarket = btnMarket.onClick(isMarket)
            isMenu = btnNewGame.onClick(isMenu)
            if btnLoadGame.onClick(False):pass
    else:
        screen.blit(btnPause.text, btnPause.pos)
        screen.blit(btnLeave.text, btnLeave.pos)
        if pygame.mouse.get_pressed(3)[0]:
            isPaused = btnPause.onClick(isPaused)
            running = btnLeave.onClick(running)


    Clock.tick(130)
    pygame.display.update() # pour ajouter tout changement à l'écran