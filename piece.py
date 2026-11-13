from enum import Enum, auto

class PieceType(Enum):
    PAWN = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()

class PieceColour(Enum):
    WHITE = auto()
    BLACK = auto()

class Piece:
    def __init__(self, pieceType, colour):
        self.pieceType = pieceType
        self.colour = colour

    def __repr__(self):
            return f"Piece({self.pieceType.name}, {self.colour.name})"