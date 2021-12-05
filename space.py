from builtins import set, property
from datetime import time

import pygame  # necessaire pour charger les images et les sons
import random
import pickle
import time
td = pygame.time.Clock().tick(130)

pygame.mixer.init()
class Button():
    def __init__(self, pos:tuple = [0,0], text:str = None, img = None, size:tuple = None):
        self.size = size
        font = pygame.font.SysFont('cambria', 30, True)
        self.img = img
        if text != None:
            self.text = font.render(text, True, [255, 255, 255])
            self.size = self.text.get_size()
        else:
            self.text = None
        if img != None:
            self.img = img
            self.size = self.img.get_size()
            print(self.size)

        self.pos = [pos[0] - self.size[0]//2, pos[1] - self.size[1]//2]
    
    def onClick(self, effect = False):
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
        self.bonus = random.randint(1,3)
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
        self.velovityMax = 6
        self.speed = 0.2
        self.velovity = 0
        self.rightPressed = False
        self.leftPressed = False
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

        f = open('data.pirate', 'r')
        self.bestScore = int(f.read())

    def systemeTir(self, ennemis):
        for idEnnemi, ennemi in enumerate(ennemis):
            for idTir, tir in enumerate(self.tirs):
                pos = [tir.pos[0] - (len(self.tirs[idTir].death) // 2 * 50), tir.pos[1]]
                if tir.toucher(ennemi):
                    if ennemi.hp <= 0:
                        del ennemis[idEnnemi]
                        self.marquer()
                    if tir.type in [1, 2]:
                        pygame.mixer.Sound("touch.wav").play()
                        if tir.type == 2:
                            for bulletdeath in self.tirs[idTir].death:
                                self.tirs.append(Balle(pos, bulletdeath, self.ballImg[bulletdeath]))
                                pos = [pos[0] + 50, pos[1]]
                        del self.tirs[idTir]
                        break

    def update(self):
        if self.rightPressed and not self.leftPressed:
            self.velovity += self.speed * td
            if self.velovity >= self.velovityMax:
                self.velovity = self.velovityMax
        if not self.rightPressed and self.leftPressed:
            self.velovity -= self.speed
            if self.velovity <= - self.velovityMax:
                self.velovity = - self.velovityMax
        if not self.rightPressed and not self.leftPressed:
            if self.velovity < 0:self.velovity += self.speed
            elif self.velovity > 0:self.velovity -= self.speed

        if 800 - self.img.get_width() > self.pos[0] + self.velovity > 0:
            self.pos = [self.pos[0] + self.velovity, self.pos[1]]
        else: self.velovity = 0

    def changeBallTypes(self, unity):
        newBallType = self.ballType + unity

        for a in range(len(self.reloads)):
            if newBallType < 1 : newBallType = len(self.reloads)
            if newBallType > len(self.reloads): newBallType = 1
            if self.reloads[newBallType] > 0:
                self.ballType = newBallType
                break
            newBallType += unity

    def tirer(self):
        if self.reloads[self.ballType] > 0 and self.lastAttack + self.attacksSpeed[self.ballType] <= pygame.time.get_ticks():
            self.reloads[self.ballType] -=1
            self.lastAttack = pygame.time.get_ticks()
            self.tirs.append(Balle(self.pos, self.ballType, self.ballImg[self.ballType]))

        else: return False

    def marquer(self):
        self.score += 1
        if self.bestScore < self.score:
            self.bestScore = self.score

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
        soud[type].play()
        self.img = img
        self.pos = [pos[0]+16 , pos[1]]
        self.damage = damages[type]
        self.type = type
        if self.type == 2:
            self.death = [1, 1, 1]
        else: self.death = []
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
    def __init__(self, ennemiType):
        self.pos = [random.randint(100,700), random.randint(-300, -50)]
        self.type = ennemiType
        self.hps = [300, 500, 700]
        self.velocities = [0.2, 0.1, 0.05]
        self.imgs = [pygame.transform.rotate(pygame.transform.scale(pygame.image.load("invader1.png"), (64,64)), 90), pygame.transform.rotate(pygame.transform.scale(pygame.image.load("invader2.png"), (64,64)), 90), pygame.transform.rotate(pygame.transform.scale(pygame.image.load("invader3.png"), (64,64)), 90)]
        self.img = self.imgs[self.type]
        self.hpMax = self.hps[self.type]
        self.hp = self.hpMax
        self.vitesse = 0.2

    def __repr__(self):
        return '<ENNEMIS type : ' + str(self.type) + ' hp : ' + str(self.hp) + '>'

    def avancer(self):
        self.pos[1] += self.vitesse * td
        if self.pos[1] > 600:return True
        else: return False

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
