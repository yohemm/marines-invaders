import pygame # importation de la librairie pygame
import sys # pour fermer correctement l'application
import space

### INITIALISATION ###
# lancement des modules inclus dans pygame
pygame.init() 

# création d'une fenêtre de 800 par 600
screen = pygame.display.set_mode((200,600))
pygame.display.set_caption("Space vaders") 
# chargement de l image de fond
fond = pygame.image.load('background.png')

### BOUCLE DE JEU  ###
running = True # variable pour laisser la fenêtre ouverte

while running : # boucle infinie pour laisser la fenêtre ouverte
    # dessin du fond
    screen.blit(fond,(0,0))
    
    ### Gestion des événements  ###
    for event in pygame.event.get(): # parcours de tous les event pygame dans cette fenêtre
        if event.type == pygame.QUIT : # si l'événement est le clic sur la fermeture de la fenêtre
            running = False # pour stopper la boucle de jeu
            
       
       # gestion du clavier
        if event.type == pygame.KEYDOWN : # si une touche a été tapée
            print("Quelqu'un a appuyé sur une touche !")
            if event.key == pygame.K_LEFT : # si la touche est la fleche gauche
                print("j'ai appuyé sur la fleche gauche")
            if event.key == pygame.K_RIGHT : # si la touche est la fleche droite
                print("j'ai appuyé sur la fleche gauche")

    ### Actualisation de la scene ###
    pygame.display.update() # pour mettre à jour l'écran
pygame.quit()
