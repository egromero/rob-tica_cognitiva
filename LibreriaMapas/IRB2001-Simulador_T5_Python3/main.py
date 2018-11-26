import irbt5
import pygame
import random 
import operator


def StateSetAll(mp):
	posibles = list()
	gencol = [col for col in enumerate(mp.getmatrix(), start=1)]
	genindex = [(fil[0],list(enumerate(fil[1], start=1))) for fil in gencol]
	for columna in genindex:
		valorColumna = columna[0]
		for linea in columna:
			if type(linea) is not int:
				for elemento in linea:
					if elemento[1].solidity == 'empty':
						posibles.append((valorColumna, elemento[0])) # Para información del objeto agregar elemento[1].
	return posibles

def WhatDoISee(x,y, mp, direccion=None):

	direcciones = {'west' : None, 
				   'east' : None, 
				   'south' : None,
				   'north' : None}
	dif = 0
	try:
		while not direcciones['east']:
			direcciones['east'] = dif if mp.gettile(x+dif, y).visual=='tilewall' else None
			dif+=1
	except IndexError:
		#print('Muralla de borde Oeste')
		direcciones['east'] = dif
	dif = 0
	try:
		while not direcciones['west']:
			direcciones['west'] = dif if mp.gettile(x-dif, y).visual=='tilewall' else None
			dif+=1
			if x-dif < 1:
				raise Exception("negativo")
	except (IndexError, Exception):
		#print('Muralla de borde Este')
		direcciones['west'] = dif
	dif = 0
	try:
		while not direcciones['south']:
			direcciones['south'] = dif if mp.gettile(x, y+dif).visual=='tilewall' else None
			dif+=1
	except IndexError:
		#print('Muralla de borde Sur')
		direcciones['south'] = dif
	dif = 0
	try:
		while not direcciones['north']:	
			direcciones['north'] = dif if mp.gettile(x, y-dif).visual=='tilewall' else None
			dif+=1
			if y-dif < 1:
				raise Exception("negativo")
	except (IndexError, Exception):
		#print('Muralla de borde Norte')
		direcciones['north'] = dif

	if direccion:
		return direcciones[direccion]
	return direcciones

def StateSetSee(mp, posible):
	#comparar distancias con la del punto del robot.
	x,y = mp.getposition()
	distRobot = WhatDoISee(x, y, mp)
	newposible = list(filter(lambda x : WhatDoISee(x[0], x[1], mp) == distRobot, posible)) 
	return newposible
	

def LoadMap(numeromapa):
	maps = { 1 : (30, 48, 'irb2001t5-map01.csv'),
			 2 : (47, 57, 'irb2001t5-map02.csv'),
			 3 : (54, 61, 'irb2001t5-map03.csv'),
			 4 : (54, 61, 'irb2001t5-map04.csv') }
	x,y,mapa = maps[numeromapa]
	return irbt5.map(x, y, mapa)


encontrado = False
mp =  LoadMap(1)
mp.setfulldraw(False)
mp.drawsmall(True)
posible = StateSetAll(mp)
newposibles = StateSetSee(mp, posible)

if len(newposibles)<1:
	encontrado = True


n=0
while not encontrado:
	dist = WhatDoISee(newposibles[0][0], newposibles[0][1], mp)
	directions = list(dist.keys())
	try:
		for i in range(1, dist[directions[n]]):
			mp.moverobot(directions[n])
			posible = StateSetAll(mp)
			newposibles = StateSetSee(mp, posible)
			if len(newposibles)<2:
				encontrado = True
				msg ='Robot encontrado en la posicion: '
				break
	except IndexError:
		msg = 'Existen dos espacios iguales en el mapa, el robot tiene dos posiciones equiprobables: '
		break
	n+=1


print(msg, newposibles)


#### Heurística: Ir a las murallas



'''
## Pygame ventana
'''
while pygame.event.wait().type != pygame.locals.QUIT:
    pass

