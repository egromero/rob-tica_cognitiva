#import pygame
#import pygame.locals
import csv

#  clase de cada cuadro, me dio lata hacer una estructura
#  corresponde a cada cuadro del mapa, son los elementos
#  de la grilla. Contiene info sobre el tipo de cuadro y como se deberia ver


class maptile(object):
    #  constructor del cuadro, acepta el tipo y la visualizacion
    def __init__(self, in_solidity, in_visual):
        self.solidity = in_solidity
        self.visual = in_visual
        self.value = 0


#  clase mapa, contiene la matriz de cuadros y las funciones de uso
class map:
    #  constructor del mapa
    def __init__(self, widthoftiles, heightoftiles, filepath):
        #  guarda el path del archivo para resetear
        self.path = filepath
        #  leer archivo csv
        print('Cargando el mapa -> ' + filepath)
        reader = csv.reader(open(filepath, 'r'), delimiter=';')
        #  generacion de tabla de datos y booleanos de estado
        self.drawrobotborder = True
        self.hascrashed = False
        self.hasfinished = False
        self.width = widthoftiles
        self.height = heightoftiles
        self.qmovements = 0
        #self.clock = pygame.time.Clock()
        self.lastime = 0
        self.smalldraw = False
        self.drawpixels = 25
        #  maptable se lee desde el index 0
        print('Generando matriz de posiciones')
        self.maptable = [[maptile('empty', 'tileground') for y in range(1, self.width + 1)] for x in
                         range(1, self.height + 1)]
        #  asignar el valor real a cada cuadro segun el csv
        for y in range(1, self.width + 1):
            linelist = next(reader)
            for x in range(1, self.height + 1):
                self.maptable[x - 1][y - 1].visual = linelist[x - 1]
                if linelist[x - 1] == 'tilewall':
                    self.maptable[x - 1][y - 1].solidity = 'solid'
                if linelist[x - 1] == 'tilestart':
                    self.maptable[x - 1][y - 1].solidity = 'empty'
                    self.startx = x
                    self.starty = y
                    self.robotposx = x
                    self.robotposy = y
                    self.robotdir = 'north'
                if linelist[x - 1] == 'tilefinish':
                    self.maptable[x - 1][y - 1].solidity = 'empty'
                    self.finishx = x
                    self.finishy = y
        #  inicio de interfaz grafica
        print('Iniciando modulo grafico pygame')
        #pygame.init()
        print('Generando ventana grafica')
        #self.screen = pygame.display.set_mode([self.drawpixels * self.height, self.drawpixels * self.width])
        #self.screen.fill((25, 25, 25))
        #self.redrawmap()
        print('Mapa generado')

    #  dibujar en la ventana el mapa

    def redrawmap(self):
        if self.smalldraw:
            stringappend = '_small'
        else:
            stringappend = ''
        print('Dibujando mapa')
        #  carga cada path de cada imagen
        for x in range(1, self.height + 1):
            for y in range(1, self.width + 1):
                if x == self.robotposx and y == self.robotposy:
                    image = pygame.image.load('tilerobot' + stringappend + '.png').convert()
                    if self.robotdir == 'west':
                        image = pygame.transform.rotate(image,90)
                    elif self.robotdir == 'south':
                        image = pygame.transform.rotate(image,180)
                    elif self.robotdir == 'east':
                        image = pygame.transform.rotate(image,270)
                elif self.robotposx - 2 <= x <= self.robotposx + 2 and self.robotposy - 2 <= y <= self.robotposy + 2 and self.drawrobotborder:
                    image = pygame.image.load('tilerobot2' + stringappend + '.png').convert()
                else:
                    image = pygame.image.load(self.maptable[x - 1][y - 1].visual + stringappend + '.png').convert()
                self.screen.blit(image, ((x - 1) * self.drawpixels, (y - 1) * self.drawpixels))
        pygame.display.flip()
        print('Mapa dibujado')

    #  cambia el mapa de tamanio grafico

    def drawsmall(self, bool):
        if bool:
            self.smalldraw = True
            self.drawpixels = 6
        else:
            self.smalldraw = False
            self.drawpixels = 25
        self.screen = pygame.display.set_mode([self.drawpixels * self.height, self.drawpixels * self.width])
        self.redrawmap()

    #  Entrega el tamanio del mapa

    def getsize(self):
        return self.width, self.height

    #  entrega cuanto tiempo lleva desde el ultimo reset
    def qtime(self):
        self.lastime = self.clock.tick() + self.lastime
        print(self.lastime)
        return self.lastime

    #  Setea el dibujar el robot entero
    def setfulldraw(self, booldraw):
        self.drawrobotborder = booldraw
        self.redrawmap()

    #  Entrega las coordenadas de la meta
    def getfinish(self):
        return self.finishx, self.finishy

    #  Entrega las coordenadas de la partida
    def getstart(self):
        return self.startx, self.starty

    #  Entrega las coordenadas del robot
    def getposition(self):
        return self.robotposx, self.robotposy

    #  Entrega el maptile especificado
    def gettile(self, x, y):
        return self.maptable[x - 1][y - 1]

    #  Entrega la matriz entera del mapa
    def getmatrix(self):
        return self.maptable

    #  Mueve el robot en una direccion
    def moverobot(self, direction):
        print('Moviendo Robot en direccion -> ' + direction)
        #  Asigna un cuadro ya viajado en el espacio actual del robot
        self.maptable[self.robotposx - 1][self.robotposy - 1].visual = 'tiletraveled'
        #  Actualiza el cambio
        if direction == 'north':
            #  si es negativo
            if self.robotposy - 1 <= 0:
                print('El robot ha llegado al borde del mapa en la posicion [' + str(self.robotposx) + ',' + str(
                    self.robotposy) + '] y no se pudo mover en direccion north')
                return False
            else:
                self.robotposy -= 1
        if direction == 'south':
            #  si se sale del mapa
            if self.robotposy + 1 >= self.width:
                print('El robot ha llegado al borde del mapa en la posicion [' + str(self.robotposx) + ',' + str(
                    self.robotposy) + '] y no se pudo mover en direccion south')
                return False
            else:
                self.robotposy += 1
        if direction == 'east':
            #  si sale del mapa
            if self.robotposx + 1 >= self.height:
                print('El robot ha llegado al borde del mapa en la posicion [' + str(self.robotposx) + ',' + str(
                    self.robotposy) + '] y no se pudo mover en direccion east')
                return False
            else:
                self.robotposx += 1
        if direction == 'west':
            #  si es negativo
            if self.robotposx - 1 <= 0:
                print('El robot ha llegado al borde del mapa en la posicion [' + str(self.robotposx) + ',' + str(
                    self.robotposy) + '] y no se pudo mover en direccion west')
                return False
            else:
                self.robotposx -= 1
        print('Nueva posicion [' + str(self.robotposx) + ',' + str(self.robotposy) + ']')
        self.collisioncheck()
        self.redrawmap()
        self.finishcheck()
        self.qmovements += self.qmovements
        return True

    #  Rota al robot hacia la derecha si right es True
    def rotate(self, right):
        if right:
            print('Rotando hacia la derecha')
            if self.robotdir == 'north':
                self.robotdir = 'east'
            elif self.robotdir == 'east':
                self.robotdir = 'south'
            elif self.robotdir == 'south':
                self.robotdir = 'west'
            else:
                self.robotdir = 'north'
        else:
            print('Rotando hacia la izquierda')
            if self.robotdir == 'north':
                self.robotdir = 'west'
            elif self.robotdir == 'west':
                self.robotdir = 'south'
            elif self.robotdir == 'south':
                self.robotdir = 'east'
            else:
                self.robotdir = 'north'
        self.redrawmap()

    #  Mueve al robot a cualquier posicion
    def teleport(self, coordx, coordy):
        print('Teletransportando Robot a [' + str(coordx) + ',' + str(coordy) + ']')
        #  Asigna un cuadro ya viajado en el espacio actual del robot
        self.maptable[self.robotposx - 1][self.robotposy - 1].visual = 'tiletraveled'
        #  actualiza el cambio
        self.robotposy = coordy
        self.robotposx = coordx
        print('Nueva posicion [' + str(self.robotposx) + ',' + str(self.robotposy) + ']')
        self.collisioncheck()
        self.redrawmap()
        self.finishcheck()

    #  revisa si hay colisiones, utiliza un cuadro de 5x5
    def collisioncheck(self):
        for x in [-2, -1, 0, 1, 2]:
            for y in [-2, -1, 0, 1, 2]:
                #  si hay una pared, el robot choca, si se le acaba el mapa tambien choca
                try:
                    if self.maptable[self.robotposx - x - 1][self.robotposy - y - 1].solidity == 'solid' or \
                                                    self.robotposx - x - 1 < 0 or self.robotposy - y - 1 < 0:
                        self.hascrashed = True
                        print('El Robot ha colisionado con una pared en las coordenadas [' + str(
                            self.robotposx - x) + ',' + str(self.robotposy - y) + ']')
                except IndexError:
                    self.hascrashed = True
                    print('El Robot se ha salido del mapa en las coordenadas [' + str(self.robotposx - x) + ',' + str(
                        self.robotposy - y) + ']')
        #  si hay una pared virtual, el robot choca solo en la posicion central
        try:
            if self.maptable[self.robotposx - 1][self.robotposy - 1].solidity == 'virtual':
                self.hascrashed = True
                print('El Robot ha entrado en un espacio no valido en [' + str(self.robotposx) + ',' + str(
                    self.robotposy) + ']')
        except IndexError:
            self.hascrashed = True
            print('El Robot se ha salido del mapa en [' + str(self.robotposx) + ',' + str(self.robotposy) + ']')
        return self.hascrashed

    #  resetea el mapa
    def finishcheck(self):
        try:
            if self.maptable[self.robotposx - 1][self.robotposy - 1].visual == 'tilefinish':
                self.hasfinished = True
                print('El Robot ha llegado a la meta')
        except IndexError:
            pass
        return self.hasfinished


    def reset(self):
        #  resetea los estados
        print('Reiniciando mapa')
        self.drawrobotborder = True
        self.hascrashed = False
        self.hasfinished = False
        #  leer archivo csv
        reader = csv.reader(open(self.path, 'r'), delimiter=';')
        #  maptable se lee desde el index 0
        self.maptable = [[maptile('empty', 'tileground') for y in range(1, self.width + 1)] for x in
                         range(1, self.height + 1)]
        #  asignar el valor real a cada cuadro segun el csv
        for y in range(1, self.width + 1):
            linelist = next(reader)
            for x in range(1, self.height + 1):
                self.maptable[x - 1][y - 1].visual = linelist[x - 1]
                if linelist[x - 1] == 'tilewall':
                    self.maptable[x - 1][y - 1].solidity = 'solid'
                if linelist[x - 1] == 'tilestart':
                    self.maptable[x - 1][y - 1].solidity = 'empty'
                    self.startx = x
                    self.starty = y
                    self.robotposx = x
                    self.robotposy = y
                if linelist[x - 1] == 'tilefinish':
                    self.maptable[x - 1][y - 1].solidity = 'empty'
                    self.finishx = x
                    self.finishy = y
        #  inicio de interfaz grafica
        self.redrawmap()
        self.lastime = 0
        self.clock.tick()
        self.qmovements = 0

#  revisa si se inicia desde este archivo
if __name__ == '__main__':
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass
