import pyxel
from sprite import Sprite

# Board class

class BoardView:
    def __init__(self, boardX, boardY, squareSize):
        self.boardX = boardX
        self.boardY = boardY
        self.SQUARESIZE = squareSize

        self.whiteSquare = Sprite(0, 0, 2, width=16, height=16)
        self.blackSquare = Sprite(0, 1, 2, width=16, height=16)

        self.BOARDSIZE = 8 * self.SQUARESIZE
        self.BORDERGAP = 1
        self.BORDERTHICKNESS = 1

    def draw(self, board=None, pieceSprites=None):
        for rowNo in range(8):
            for colNo in range(8):

                squareX, squareY = self.getSquarePosition(rowNo, colNo)

                if (rowNo + colNo) % 2 == 0:
                    squareSprite = self.whiteSquare
                else:
                    squareSprite = self.blackSquare

                squareSprite.draw(squareX, squareY, self.SQUARESIZE/16)

        # Draw pieces if supplied
        if board is not None and pieceSprites is not None:
            for rowNo in range(8):
                for colNo in range(8):
                    piece = board.getPiece(rowNo, colNo)
                    if piece is None:
                        continue

                    sprite = pieceSprites[piece.colour][piece.pieceType]
                    squareX, squareY = self.getSquarePosition(rowNo, colNo)
                    sprite.draw(squareX, squareY, self.SQUARESIZE / 16)

        # Draw border
        borderX = self.boardX - self.BORDERGAP - self.BORDERTHICKNESS
        borderY = self.boardY - self.BORDERGAP - self.BORDERTHICKNESS
        borderSize = self.BOARDSIZE + 2 * (self.BORDERGAP + self.BORDERTHICKNESS)
        pyxel.rectb(borderX, borderY, borderSize, borderSize, 0)

    def getSquareFromMouse(self, mouseX, mouseY):
        localX = mouseX - self.boardX
        localY = mouseY - self.boardY

        if not (0 <= localX and 0 < self.BOARDSIZE) or not (0 <= localY and 0 < self.BOARDSIZE):
            return None

        col = localX // self.SQUARESIZE
        row = localY // self.SQUARESIZE
        
        return (row, col)

    def getSquarePosition(self, row, col):
        squareX = self.boardX + col * self.SQUARESIZE
        squareY = self.boardY + row * self.SQUARESIZE
        return squareX, squareY