from dataclasses import dataclass

from board import Board
from piece import PieceColour, Piece, PieceType

PROMOTION_TYPES = (
    PieceType.QUEEN,
    PieceType.ROOK,
    PieceType.BISHOP,
    PieceType.KNIGHT,
    PieceType.KING
)

@dataclass(frozen=True)
class Move:
    start: tuple
    end: tuple
    capturedSquare: tuple = None
    promotionType: PieceType = None

    @property
    def isCapture(self):
        return self.capturedSquare is not None

class Game:
    def __init__(self):
        self.board = Board()

        self.currentTurn = PieceColour.WHITE
        self.enPassantTarget = None
        self.gameFinished = False
        self.winner = None

    def reset(self):
        self.board.reset()

        self.currentTurn = PieceColour.WHITE
        self.enPassantTarget = None
        self.gameFinished = False
        self.winner = None

    @staticmethod
    def getOpponent(colour):
        if colour == PieceColour.WHITE:
            return PieceColour.BLACK
        return PieceColour.WHITE

    @staticmethod
    def isInside(row, col):
        return Board.isInside(row, col)

    def getAllLegalMoves(self):
        if self.gameFinished:
            return []

        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.getPiece(row, col)
                if piece is None or piece.colour != self.currentTurn:
                    continue
                moves.extend(self.getPossibleMoves(row, col))

        captureMoves = [move for move in moves if move.isCapture]
        if captureMoves:
            return captureMoves
        return moves

    def getLegalMoves(self, row, col):
        if self.gameFinished:
            return []

        piece = self.board.getPiece(row, col)
        if piece is None or piece.colour != self.currentTurn:
            return []

        return [move for move in self.getAllLegalMoves() if move.start == (row, col)]

    def getPossibleMoves(self, row, col):
        piece = self.board.getPiece(row, col)
        if piece is None:
                    return []

        if piece.pieceType == PieceType.PAWN:
            return self.getPawnMoves(row, col, piece)
        if piece.pieceType == PieceType.KNIGHT:
            return self.getKnightMoves(row, col, piece)
        if piece.pieceType == PieceType.BISHOP:
            return self.getSlidingMoves(row, col, piece, ((1, 1), (1, -1), (-1, 1), (-1, -1)))
        if piece.pieceType == PieceType.ROOK:
            return self.getSlidingMoves(row, col, piece, ((1, 0), (-1, 0), (0, 1), (0, -1)))
        if piece.pieceType == PieceType.QUEEN:
            directions = (
                (1, 0), (-1, 0), (0, 1), (0, -1),
                (1, 1), (1, -1), (-1, 1), (-1, -1)
            )
            return self.getSlidingMoves(row, col, piece, directions)
        if piece.pieceType == PieceType.KING:
            return self.getKingMoves(row, col, piece)

        return []

    def addPawnMove(self, moves, start, end, capturedSquare=None):
        piece = self.board.getPiece(*start)
        promotionRow = 0 if piece.colour == PieceColour.WHITE else 7

        if end[0] == promotionRow:
            for promotionType in PROMOTION_TYPES:
                moves.append(Move(start, end, capturedSquare, promotionType))
        else:
            moves.append(Move(start, end, capturedSquare))

    def getPawnMoves(self, row, col, piece):
        moves = []
        direction = -1 if piece.colour == PieceColour.WHITE else 1
        startRow = 6 if piece.colour == PieceColour.WHITE else 1
        start = (row, col)

        # Move forward by one square, provided it is empty.
        oneStepRow = row + direction
        if self.isInside(oneStepRow, col) and self.board.getPiece(oneStepRow, col) is None:
            self.addPawnMove(moves, start, (oneStepRow, col))

            # Pawns may move two squares from their starting row.
            twoStepRow = row + 2 * direction
            if row == startRow and self.board.getPiece(twoStepRow, col) is None:
                moves.append(Move(start, (twoStepRow, col)))

        # Pawns capture diagonally, not forwards.
        for colChange in (-1, 1):
            targetRow = row + direction
            targetCol = col + colChange
            if not self.isInside(targetRow, targetCol):
                continue

            targetPiece = self.board.getPiece(targetRow, targetCol)
            if targetPiece is not None and targetPiece.colour != piece.colour:
                self.addPawnMove(moves, start, (targetRow, targetCol), (targetRow, targetCol))

            # En passant: the target square is empty, but the adjacent pawn
            # that moved two squares is removed.
            elif self.enPassantTarget == (targetRow, targetCol):
                capturedSquare = (row, targetCol)
                capturedPiece = self.board.getPiece(*capturedSquare)
                if (
                    capturedPiece is not None
                    and capturedPiece.pieceType == PieceType.PAWN
                    and capturedPiece.colour != piece.colour
                ):
                    moves.append(Move(start, (targetRow, targetCol), capturedSquare))

        return moves

    def getKnightMoves(self, row, col, piece):
        moves = []
        offsets = (
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        )

        for rowChange, colChange in offsets:
            targetRow = row + rowChange
            targetCol = col + colChange

            if not self.isInside(targetRow, targetCol):
                continue

            targetPiece = self.board.getPiece(targetRow, targetCol)
            if targetPiece is None:
                moves.append(Move((row, col), (targetRow, targetCol)))
            elif targetPiece.colour != piece.colour:
                moves.append(Move((row, col), (targetRow, targetCol), (targetRow, targetCol)))

        return moves

    def getKingMoves(self, row, col, piece):
        moves = []
        for rowChange in (-1, 0, 1):
            for colChange in (-1, 0, 1):
                if rowChange == 0 and colChange == 0:
                    continue

                targetRow = row + rowChange
                targetCol = col + colChange
                if not self.isInside(targetRow, targetCol):
                    continue

                targetPiece = self.board.getPiece(targetRow, targetCol)

                if targetPiece is None:
                    moves.append(Move((row, col), (targetRow, targetCol)))
                elif targetPiece.colour != piece.colour:
                    moves.append(Move((row, col), (targetRow, targetCol), (targetRow, targetCol)))

        return moves

    def getSlidingMoves(self, row, col, piece, directions):
         moves = []
 
         for rowChange, colChange in directions:
             targetRow = row + rowChange
             targetCol = col + colChange
 
             while self.isInside(targetRow, targetCol):
                 targetPiece = self.board.getPiece(targetRow, targetCol)
 
                 if targetPiece is None:
                     moves.append(Move((row, col), (targetRow, targetCol)))
                 else:
                     if targetPiece.colour != piece.colour:
                         moves.append(Move((row, col), (targetRow, targetCol), (targetRow, targetCol)))
                     # A sliding piece cannot move beyond either colour.
                     break
 
                 targetRow += rowChange
                 targetCol += colChange
 
         return moves

    def makeMove(self, move):
        if self.gameFinished or move not in self.getAllLegalMoves():
            return False

        piece = self.board.getPiece(*move.start)
        if piece is None:
            return False

        if move.capturedSquare is not None:
            self.board.setPiece(*move.capturedSquare, None)

        self.board.setPiece(*move.start, None)
        self.board.setPiece(*move.end, piece)

        if move.promotionType is not None:
            if piece.pieceType != PieceType.PAWN or move.promotionType not in PROMOTION_TYPES:
                raise ValueError("Invalid promotion move")
            piece.pieceType = move.promotionType

        self.enPassantTarget = None
        startRow, startCol = move.start
        endRow, endCol = move.end
        if piece.pieceType == PieceType.PAWN and abs(endRow - startRow) == 2:
            self.enPassantTarget = ((startRow + endRow) // 2, startCol)

        self.currentTurn = self.getOpponent(self.currentTurn)
        self.updateGameOver()
        return True

    def updateGameOver(self):
        whitePieces = self.board.countPieces(PieceColour.WHITE)
        blackPieces = self.board.countPieces(PieceColour.BLACK)

        # In antichess, a player wins by losing all their pieces.
        if whitePieces == 0:
            self.winner = PieceColour.WHITE
        elif blackPieces == 0:
            self.winner = PieceColour.BLACK
        # A player also wins if they have no legal moves on their turn.
        elif not self.getAllLegalMoves():
            self.winner = self.currentTurn
        else:
            self.winner = None

        self.gameFinished = self.winner is None