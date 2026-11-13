import pyxel

# Sprite class

class Sprite:
    def __init__(self, imageBank, sourceX, sourceY, transparentColour=None, width=16, height=16):
        self.imageBank = imageBank

        self.sourceX = sourceX*16
        self.sourceY = sourceY*16
        self.width = width
        self.height = height

        self.transparentColour = transparentColour

    def draw(self, x, y, scale=1):
        drawX = x - (self.width * (1 - scale)) / 2
        drawY = y - (self.height * (1 - scale)) / 2
        pyxel.blt(drawX, drawY, self.imageBank, self.sourceX, self.sourceY, self.width, self.height, self.transparentColour, scale=scale)