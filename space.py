from builtins import set, property
from datetime import time

import pygame  # necessaire pour charger les images et les sons
import random
import pickle
import time


pygame.mixer.init()
class Button():
    def __init__(self, pos:tuple = [0,0], text:str = None, img = None, size:tuple = None):
        self.size = size
        font = pygame.font.SysFont('cambria', 30, True)
        self.img = img

        if text != None:
            self.text = font.render(text, True, [255, 255, 255])
            self.size = self.text.get_size() # taille du btn et celle du text
        else:
            self.text = None
        if img != None:
            self.img = img
            self.size = self.img.get_size() # taille du btn et celle de l'image

        self.pos = [pos[0] - self.size[0]//2, pos[1] - self.size[1]//2]
    
    def onClick(self, effect = False):
        if self.pos[0] < pygame.mouse.get_pos()[0] < self.pos[0] + self.size[0] and self.pos[1] < pygame.mouse.get_pos()[1] < self.pos[1] + self.size[1]: # si on click
            return not effect #inverse l'effect
        return effect

class Bonus():
    def __init__(self, imgDict):
        nbReload = {
            1 : [10, 20],
            2 : [5, 10],
            3 : [1, 5]
        }

        self.pos = [random.randint(20, 780), -20]
        self.velocity = 2

        self.bonus = random.randint(1,3)#type de ball aleatoire
        self.quantity = random.choice(nbReload[self.bonus])

        self.img = imgDict[self.bonus]

    def __repr__(self):
        return 'bonus : '+ str(self.bonus) + ' pos : ' + str(self.pos)

    def move(self):
        self.pos = [self.pos[0], self.pos[1]+ self.velocity]#change la pos

    def touchPlayer(self, player):
        if objsTouch(self, player):
            player.reloads[self.bonus] += self.quantity # augmante le chargeur du joueur
            return True
        else: return False

class Joueur() : # classe pour créer le vaisseau du joueur
    def __init__(self) :
        self.hpMax = 300
        self.hp = self.hpMax

        self.velovityMax = 10
        self.speed = 0.4
        self.velovity = 0

        self.rightPressed = False
        self.leftPressed = False

        self.img = pygame.transform.flip(pygame.transform.scale(pygame.image.load("vaisseau.png"), (100,100)), False, True)

        self.pos = (400, 500)

        self.score = 0

        self.contactAttack = 10

        self.lastAttack = 0

        self.ballType = 1
        self.reloads = {
            1 : 50,
            2 : 5,
            3 : 1,
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


        #regade le melleur score
        f = open('data.pirate', 'r')
        self.bestScore = int(f.read())

    def systemeTir(self, ennemis):
        for idEnnemi, ennemi in enumerate(ennemis):
            if objsTouch(self, ennemi): #si on touche l'ennemis
                # attack dans les 2 sens
                ennemi.hp -= self.contactAttack
                self.hp -= ennemi.contactAttack

            for idTir, tir in enumerate(self.tirs):
                if tir.toucher(ennemi):
                    if tir.type in [1, 2]:
                        pygame.mixer.Sound("touch.wav").play() # sond de toucher
                        if tir.type == 2:
                            pos = [tir.pos[0] - (len(self.tirs[idTir].death) // 2 * 50), tir.pos[1]] # premier pos de ball
                            # invoque les bullet pour le canon
                            for bulletdeath in self.tirs[idTir].death:
                                self.tirs.append(Balle(pos, bulletdeath, self.ballImg[bulletdeath]))
                                pos = [pos[0] + 50, pos[1]]
                        del self.tirs[idTir]
                        break
            if ennemi.hp <= 0:
                del ennemis[idEnnemi] # supprime les ennemis
                self.marquer()

    def update(self):
        if self.rightPressed and not self.leftPressed:
            self.velovity += self.speed # augmante la vitesse du joueur
            if self.velovity >= self.velovityMax: self.velovity = self.velovityMax #met un maximum a la vitese
        if not self.rightPressed and self.leftPressed:
            self.velovity -= self.speed
            if self.velovity <= - self.velovityMax: self.velovity = - self.velovityMax

        if not self.rightPressed and not self.leftPressed: #ralentissement
            if self.velovity < 0:self.velovity += self.speed
            elif self.velovity > 0:self.velovity -= self.speed

        if 800 - self.img.get_width() > self.pos[0] + self.velovity > 0: # si on sors pas de l'écran
            self.pos = [self.pos[0] + self.velovity, self.pos[1]] #avance
        else: self.velovity = 0 # arrete le perso

    def changeBallTypes(self, unity):
        newBallType = self.ballType + unity # ball theorique suivante

        for a in range(len(self.reloads)):
            if newBallType < 1 : newBallType = len(self.reloads) #evite de sortir du chargeur
            if newBallType > len(self.reloads): newBallType = 1 #evite de sortir du chargeur
            if self.reloads[newBallType] > 0: # si on a des balles
                self.ballType = newBallType #on met a jour le type de balles
                break
            newBallType += unity

    def tirer(self):
        if self.reloads[self.ballType] > 0 and self.lastAttack + self.attacksSpeed[self.ballType] <= pygame.time.get_ticks(): # si on a des balls et que on a attendu pour attacker
            self.reloads[self.ballType] -=1 #enleve 1 au chargeur
            self.lastAttack = pygame.time.get_ticks() #mets a joour la dernier attaque
            self.tirs.append(Balle(self.pos, self.ballType, self.ballImg[self.ballType])) # créé une nouvelle balles

        else: return False

    def marquer(self):
        self.score += 1
        if self.bestScore < self.score: self.bestScore = self.score #met a jour le meilleur score

class Balle():
    """docstring for ClassName"""
    def __init__(self,pos, type ,img):
        damages = {
            1: 150,
            2: 150,
            3: 300,
        }
        soud = {
            1: pygame.mixer.Sound("gun.wav"),
            2: pygame.mixer.Sound("canon.wav"),
            3: pygame.mixer.Sound("anchor.wav"),
        }
        velocity = {
            1: 10,
            2: 5,
            3: 3,
        }
        soud[type].play()
        self.img = img
        self.pos = [pos[0] +50 - (self.img.get_size()[0]//2) , pos[1]]
        self.damage = damages[type]
        self.velocity = velocity[type]
        self.type = type
        if self.type == 2: #pour la division de la boule en 3 balles
            self.death = [1, 1, 1]
        else: self.death = []
        self.EnnemisTouch = []

    def bouger(self):#avance le joueur
        if self.pos[1]>0:
            self.pos[1]-= self.velocity
            return True
        else:
            return False
    def toucher(self,ennemi):
        if objsTouch(self, ennemi) and not ennemi in self.EnnemisTouch:
            self.EnnemisTouch.append(ennemi) #pour ne pas toucher 2 fois l'ennemi
            ennemi.hp -= self.damage #remet a jour les hp
            return True
        else: return False



class Ennemi():
    """docstring for ClassName"""
    NbEnnemis = 10
    def __init__(self, ennemiType):
        self.pos = [random.randint(100,700), random.randint(-300, -50)]
        self.type = ennemiType
        self.hps = [300, 500, 700]
        self.contactAttack = 2
        self.velocities = [1, 0.5, 0.3]
        self.imgs = [pygame.transform.rotate(pygame.transform.scale(pygame.image.load("invader1.png"), (64,64)), 90), pygame.transform.rotate(pygame.transform.scale(pygame.image.load("invader2.png"), (64,64)), 90), pygame.transform.rotate(pygame.transform.scale(pygame.image.load("invader3.png"), (64,64)), 90)]
        self.img = self.imgs[self.type]
        self.hpMax = self.hps[self.type]
        self.hp = self.hpMax
        self.vitesse = self.velocities[self.type]

    def __repr__(self):
        return '<ENNEMIS type : ' + str(self.type) + ' hp : ' + str(self.hp) + '>'

    def avancer(self, player):
        #avance si il ne touche pas l'ennemi
        if not objsTouch(self, player):
            self.pos[1] += self.vitesse
        else:
            self.pos[1] -= self.vitesse
        if self.pos[1] > 600:return True
        else: return False

def objsTouch(obj1, obj2):
    #compare les pos entre 2 entité
    return (obj1.pos[0] < obj2.pos[0] < obj1.pos[0] + obj1.img.get_width() or obj2.pos[0] < obj1.pos[
        0] < obj2.pos[0] + obj2.img.get_width()) and (
            obj1.pos[1] < obj2.pos[1] < obj1.pos[1] + obj1.img.get_height() or obj2.pos[1] < obj1.pos[
        1] < obj2.pos[1] + obj2.img.get_height())
