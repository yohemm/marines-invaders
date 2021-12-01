from builtins import set, property
from datetime import time

import pygame  # necessaire pour charger les images et les sons
import random
import time
td = pygame.time.Clock().tick(130)

class Button():
    def __init__(self, pos:tuple = [0,0], text:str = None, img = None, size:tuple = None):
        self.size = size
        font = pygame.font.SysFont('cambria', 30, True)
        self.img = img
        if text != None:
            self.text = font.render(text, True, [255, 255, 255], [0, 0, 0])
            self.size = self.text.get_size()
        else:
            self.text = None
        if img != None:
            self.img = img
            self.size = self.img.get_size()

        self.pos = [pos[0] - self.size[0]//2, pos[1] - self.size[1]//2]
    
    def onClick(self, effect = True):
        if self.pos[0] < pygame.mouse.get_pos()[0] < self.pos[0] + self.size[0] and self.pos[1] < pygame.mouse.get_pos()[1] < self.pos[1] + self.size[1]:
            return not effect
        return effect

class Bonus():
    def __init__(self, imgDict):
        nbReload = {
            1 : [10, 20],
            2 : [5, 10],
            3 : [1, 5]
        }
        self.pos = [random.randint(20, 780), -20]
        self.bonus = random.randint(2,3)
        self.quantity = random.choice(nbReload[self.bonus])
        self.velocity = 0.9
        self.img = imgDict[self.bonus]

    def __repr__(self):
        return 'bonus : '+ str(self.bonus) + ' pos : ' + str(self.pos)

    def move(self):
        self.pos = [self.pos[0], self.pos[1]+ self.velocity * td]

    def touchPlayer(self, player):
        if objsTouch(self, player):
            player.reloads[self.bonus] += self.quantity
            print(player.reloads)
            return True
        else: return False

class Joueur() : # classe pour créer le vaisseau du joueur
    def __init__(self) :
        self.sens = 1
        self.img = pygame.transform.flip(pygame.transform.scale(pygame.image.load("vaisseau.png"), (100,100)), False, True)
        self.pos = (400, 500)
        self.score = 0

        self.lastAttack = 0

        self.ballType = 1
        self.reloads = {
            1 : 50,
            2 : 0,
            3 : 0,
        }

        # creation de la balle

        self.ballTypes = {
            1: 'normal',
            2: 'perforante',
            3: 'lazer'
        }
        self.ballImg = {
            1: pygame.image.load("balle.png").convert_alpha(),
            2: pygame.transform.scale(pygame.image.load("bullet.png").convert_alpha(), (30, 30)),
            3: pygame.transform.scale(pygame.image.load("encre.png").convert_alpha(), (30, 30))
        }

        self.attacksSpeed = {
            1: 200,
            2: 500,
            3: 700
        }

        self.tirs = []

    def systemeTir(self, ennemis):
        for idEnnemi, ennemi in enumerate(ennemis):
            ennemi.playerTouch(self)
            for idTir, tir in enumerate(self.tirs):
                if tir.toucher(ennemi):
                    if ennemi.hp <= 0:
                        del ennemis[idEnnemi]
                        self.marquer()
                        datas = {
                            'player': self,
                            'ennemis': ennemis,
                        }
                    if tir.type in [1, 4]:
                        del self.tirs[idTir]
                        break

    def deplacer(self):
        if 0 <= self.pos[0] + 1 * self.sens*td <= 800 - self.img.get_width():
            self.pos = [self.pos[0] + 1 * self.sens*td, self.pos[1]]

    def changeBallTypes(self, unity):
        newBallType = self.ballType + unity
        while newBallType == self.ballType:
            if self.reloads[newBallType] > 0:
                self.ballType = newBallType
                break
            if newBallType < 0 : newBallType = len(self.reloads)
            if newBallType > len(self.reloads): 0
        print(self.ballType + ' '+ newBallType)

    def tirer(self):
        if self.reloads[self.ballType] > 0 and self.lastAttack + self.attacksSpeed[self.ballType] <= pygame.time.get_ticks():
            self.reloads[self.ballType] -=1
            self.lastAttack = pygame.time.get_ticks()
            self.tirs.append(Balle(self, self.ballType, self.ballImg[self.ballType]))
            print(self.reloads[self.ballType])

        else: return False

    def marquer(self):
        self.score += 1

class Balle():
    """docstring for ClassName"""
    def __init__(self,joueur, type ,img):
        damages = {
            1: 100,
            2: 150,
            3: 300,
        }
        self.img = img
        self.pos = [joueur.pos[0]+16, joueur.pos[1 ]]
        self.joueur = joueur
        self.damage = damages[type]
        self.type = type
        self.EnnemisTouch = []

    def bouger(self):
        if self.pos[1]>0:
            self.pos[1]-=1*td
            return True
        else:
            return False
    def toucher(self,ennemi):
        if objsTouch(self, ennemi) and not ennemi in self.EnnemisTouch:
            self.EnnemisTouch.append(ennemi)
            ennemi.hp -= self.damage
            return True
        else: return False



class Ennemi():
    """docstring for ClassName"""
    NbEnnemis = 10
    def __init__(self):
        self.pos = [random.randint(100,700), -50]
        self.type = random.randint(1,2)
        self.img = pygame.transform.scale(pygame.image.load("invader1.png"), (64,64))
        self.hpMax = 400
        self.hp = 400
        self.vitesse = 0.2

    def avancer(self):
        self.pos[1] += self.vitesse * td
        if self.pos[1] > 600:return True
        else: return False

    def playerTouch(self, player):
        if objsTouch(self, player):
            del player

    def hurt(self, damage):
        if self.hp - damage <= 0:
            return True
        else:
            self.hp -= damage
            return False

def objsTouch(obj1, obj2):
    return (obj1.pos[0] < obj2.pos[0] < obj1.pos[0] + obj1.img.get_width() or obj2.pos[0] < obj1.pos[
        0] < obj2.pos[0] + obj2.img.get_width()) and (
            obj1.pos[1] < obj2.pos[1] < obj1.pos[1] + obj1.img.get_height() or obj2.pos[1] < obj1.pos[
        1] < obj2.pos[1] + obj2.img.get_height())
