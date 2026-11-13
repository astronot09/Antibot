from piece import PieceColour, Piece, PieceType

class Board:
    BOARD_SIZE = 8

    BACK_RANK = (
        PieceType.ROOK,
        PieceType.KNIGHT,
        PieceType.BISHOP,
        PieceType.QUEEN,
        PieceType.KING,
        PieceType.BISHOP,
        PieceType.KNIGHT,
        PieceType.ROOK
        )

    def __init__(self):
        self.reset()

    def reset(self):
        self.boardState = [[None for col in range(self.BOARD_SIZE)] for row in range(self.BOARD_SIZE)]

        for col, pieceType in enumerate(self.BACK_RANK):
            # Black pieces
            self.boardState[0][col] = Piece(pieceType, PieceColour.BLACK)
            self.boardState[1][col] = Piece(PieceType.PAWN, PieceColour.BLACK)

            # White pieces
            self.boardState[6][col] = Piece(PieceType.PAWN, PieceColour.WHITE)
            self.boardState[7][col] = Piece(pieceType, PieceColour.WHITE)

    @staticmethod
    def isInside(row, col):
        return 0 <= row and row < 8 and 0 <= col and col < 8

    def getPiece(self, row, col):
        if not self.isInside(row, col):
            return None
        return self.boardState[row][col]

    def setPiece(self, row, col, piece):
        if not self.isInside(row, col):
            raise IndexError("Board coordinates must be between 0 and 7")
        self.boardState[row][col] = piece

    def countPieces(self, colour):
        return sum(1 for row in self.boardState for piece in row if piece is not None and PieceColour == colour)