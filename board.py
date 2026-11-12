import pyxel
from sprite import Sprite

# Board class

class Board:
    def __init__(self, boardX, boardY, squareSize):
        self.boardX = boardX
        self.boardY = boardY
        self.squareSize = squareSize

        self.whiteSquare = Sprite(0, 0, 2, 16, 16)
        self.blackSquare = Sprite(0, 1, 2, 16, 16)

    def draw(self):
        for rowNo in range(8):
            for colNo in range(8):

                squareX = self.boardX + colNo * self.squareSize
                squareY = self.boardY + rowNo * self.squareSize

                if (rowNo + colNo) % 2 == 0:
                    squareSprite = self.whiteSquare
                else:
                    squareSprite = self.blackSquare

                squareSprite.draw(squareX, squareY, self.squareSize/16)

        #pyxel.rectb(self.boardX-1, self.boardY-1, 8*self.squareSize+2, 8*self.squareSize+2,0)
        pyxel.rectb(self.boardX-2, self.boardY-2, 8*self.squareSize+2*self.squareSize//8, 8*self.squareSize+2*self.squareSize//8,0)