from vpython import *


class Turtle3D():
    """ Clase Turtle3D """

    def __init__(self):
        """ Este es el iniciador de la tortuga """
        # parametros de l'escena
        scene.height = scene.width = 1000
        scene.autocenter = True
        scene.caption = """\nTo rotate "camera", drag with right button or Ctrl-drag.\nTo zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.\n  On a two-button mouse, middle is left + right.\nTo pan left/right and up/down, Shift-drag.\nTouch screen: pinch/extend to zoom, swipe or two-finger rotate.\nPress any Key to exit"""

        self.paint = True
        self.alpha = 0
        self.beta = 0
        self.turt = box(pos=vector(0, 0, 0), axis=vector(1, 0, 0), size=vector(0.2, 0.2, 0.2), color=color.blue, opacity=0)

    def color(self, r, g, b):
        """ Esta función se encarga de cambiar el color de la tortuga y la estela que deja en su camino """
        self.turt.color = vector(r, g, b)

    def forward(self, mida):
        """ Esta función hace que la tortuga avance hacia la dirección que esta mirando "mida" unidades """
        # Coordenadas x,y,z de la posición actual de la tortuga
        actx = self.turt.pos.x
        acty = self.turt.pos.y
        actz = self.turt.pos.z
        # Coordenadas x,y,z del vector dirección hacia la que debe avanzar la tortuga
        x = sin(self.alpha) * cos(self.beta)
        y = sin(self.beta)
        z = cos(self.alpha) * cos(self.beta)
        # Movimiento de la tortuga
        mov = vector(actx+(mida*x), acty+(mida*y), actz+(mida*z))
        self.turt.pos = mov

        # Dibujo de la estela de la tortuga
        if self.paint:
            sph1 = sphere(pos=vector(actx, acty, actz), radius=0.1, color=self.turt.color)
            cil = cylinder(pos=vector(actx, acty, actz), axis=mov-vector(actx, acty, actz), radius=0.1, color=self.turt.color)
            sph2 = sphere(pos=mov, radius=0.1, color=self.turt.color)

    def backward(self, mida):
        """ Esta función hace que la tortuga retoceda "mida" unidades en dirección contraria a la que esta mirando """
        # Coordenadas x,y,z de la posición actual de la tortuga
        actx = self.turt.pos.x
        acty = self.turt.pos.y
        actz = self.turt.pos.z
        # Coordenadas x,y,z del vector dirección hacia la que debe avanzar la tortuga
        x = sin(self.alpha) * cos(self.beta)
        y = sin(self.beta)
        z = cos(self.alpha) * cos(self.beta)
        # Movimiento de la tortuga
        mov = vector(actx-(mida*x), acty-(mida*y), actz-(mida*z))
        self.turt.pos = mov

        # Dibujo de la estela de la tortuga
        if self.paint:
            sph1 = sphere(pos=vector(actx, acty, actz), radius=0.1, color=self.turt.color)
            cil = cylinder(pos=vector(actx, acty, actz), axis=mov-vector(actx, acty, actz), radius=0.1, color=self.turt.color)
            sph2 = sphere(pos=mov, radius=0.1, color=self.turt.color)

    def up(self, ang):
        """ Esta función rota la tortuga hacía arriba "ang" grados """
        # Paso de ang de grados a radianes para aplicar el rotate
        self.beta = self.beta + (ang * 2 * pi) / 360
        self.turt.rotate(angle=self.beta, axis=vector(1, 0, 0))

    def down(self, ang):
        """ Esta función rota la tortuga hacia abajo "ang" grados """
        # Paso de ang de grados a radianes para aplicar el rotate
        self.beta = self.beta - (ang * 2 * pi) / 360
        self.turt.rotate(angle=self.beta, axis=vector(1, 0, 0))

    def left(self, ang):
        """ Esta función rota la tortuga hacia la izquierda "ang" grados """
        # Paso de ang de grados a radianes para aplicar el rotate
        self.alpha = self.alpha - (ang * 2 * pi) / 360
        self.turt.rotate(angle=self.alpha, axis=vector(0, 1, 0))

    def right(self, ang):
        """ Esta función rota la tortuga hacia la derecha "ang" grados """
        # Paso de ang de grados a radianes para aplicar el rotate
        self.alpha = self.alpha + (ang * 2 * pi) / 360
        self.turt.rotate(angle=self.alpha, axis=vector(0, 1, 0))

    def hide(self):
        """ Esta función hace que no se dibuje la estela que deja la tortuga """
        self.paint = False

    def show(self):
        """ Esta función hace que se dibuje la estela de la tortuga """
        self.paint = True

    def home(self):
        """ Esta función coloca a la tortuga en la posición inicial de la escena """
        self.turt.pos = vector(0, 0, 0)
        self.alpha = 0
        self.beta = 0

    def delete(self):
        """ Elimina la escena cuando se toca una tecla cualquiera """
        scene.waitfor('keydown')
        scene.delete()
