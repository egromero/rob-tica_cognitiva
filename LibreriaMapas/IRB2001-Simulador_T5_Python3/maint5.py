# Importamos la libreria
import pygame
import irbt5

# Instanciamos el mapa
mp = irbt5.map(30, 48, 'irb2001t5-map01.csv')

# Ejemplo basico de movimiento del robot, sin ningun tipo de path planning:

# Mover el robot al este
mp.moverobot('east')

# Reseteamos el mapa
mp.reset()
mp.drawsmall(True)
tile = mp.gettile(1,1)
tile.solidity = "virtual"
tile.visual = "tilevirtual"
mp.setfulldraw(False)
mp.redrawmap()

# Mover el robot al norte
for _ in range(0, 8):
    mp.moverobot('north')

for _ in range(0,5):
    mp.rotate(False)

for _ in range(0,3):
    mp.rotate(True)

# Mover hacia el este hasta llegar a la meta
for _ in range(0, 20):
    mp.moverobot('east')

# out = input("done")

# Esto es para generar la ventana de PyGame. Debe ir siempre.
while pygame.event.wait().type != pygame.locals.QUIT:
    pass
