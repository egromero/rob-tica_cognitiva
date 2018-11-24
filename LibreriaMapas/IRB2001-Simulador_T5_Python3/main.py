import irbt5
import pygame



class Robot:
	def __init__(self):
		self.px = None
		self.py = None
		self.dir = None

mp = irbt5.map(30, 48, 'irb2001t5-map01.csv')



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

def DistanceToWall(x,y):
	direcciones = {'W' : None, 
				   'E' : None, 
				   'S' : None,
				   'N' : None}
	dif = 0
	try:
		while not direcciones['W']:
			direcciones['W'] = dif if mp.gettile(x+dif, y).visual=='tilewall' else None
			dif+=1
	except IndexError:
		print('Muralla de borde Oeste')
		direcciones['W'] = dif
	dif = 0
	try:
		while not direcciones['E']:
			direcciones['E'] = dif if mp.gettile(x-dif, y).visual=='tilewall' else None
			dif+=1
			if x-dif < 1:
				raise Exception("negativo")
	except (IndexError, Exception):
		print('Muralla de borde Este')
		direcciones['E'] = dif
	dif = 0
	try:
		while not direcciones['S']:
			direcciones['S'] = dif if mp.gettile(x, y+dif).visual=='tilewall' else None
			dif+=1
	except IndexError:
		print('Muralla de borde Sur')
		direcciones['S'] = dif
	dif = 0
	try:
		while not direcciones['N']:	
			direcciones['N'] = dif if mp.gettile(x, y-dif).visual=='tilewall' else None
			dif+=1
			if y-dif < 1:
				raise Exception("negativo")
	except (IndexError, Exception):
		print('Muralla de borde Norte')
		direcciones['N'] = dif

	
	return direcciones

def StateSetSee(posible):
	pass



