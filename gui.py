import pyxel
from enum import Enum, auto
from sprite import Sprite
from board_view import BoardView
from game import Game
from piece import PieceType, PieceColour
from button import Button

# Enums

class ScreenState(Enum):
    MAIN_MENU = auto()
    GAME = auto()
    GAME_OVER = auto()

class TrayState(Enum):
    NONE = auto()
    SETTINGS = auto()
    HINTS = auto()

class Difficulty(Enum):
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()

# Textbox class
class Textbox:
    def __init__(self, x, y, width, height, text, bgColour=0, textColour=7):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text
            self.bgColour = bgColour
            self.textColour = textColour

    def draw(self):
        # Draw background
        pyxel.rect(self.x, self.y, self.width, self.height, self.bgColour)

        # Draw border
        #pyxel.rectb(self.x, self.y, self.width, self.height, 7)

        textX = self.x + (self.width - len(self.text) * 4) // 2
        textY = self.y + (self.height - 5) // 2
        pyxel.text(textX, textY, self.text, self.textColour)


class GUI:
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        pyxel.init(screenWidth, screenHeight, title="Antibot", fps=60)
        pyxel.load("myantibot.pyxres")
        pyxel.mouse(True)

        self.currentScreen = ScreenState.MAIN_MENU
        self.currentTray = TrayState.NONE
        self.visibleTrays = set()

        self.buttonHeight = 25
        self.buttonWidth = 125

        self.trayWidth = int(screenWidth * 0.75)
        self.settingsX = -self.trayWidth # Is hidden on left
        self.hintsX = self.screenWidth # Is hidden on right

        self.game = Game()
        self.boardView = BoardView(100, 25, 16)

        self.selectedSquare = None
        self.selectedMoves = []

        self.createScreenObjects()
        pyxel.run(self.update, self.draw)

    def createScreenObjects(self):
        # Icons
        self.settingsIcon = Sprite(0,0,0)
        self.hoverSettingsIcon = Sprite(0,1,0)
        self.hintsIcon = Sprite(0,0,1)
        self.hoverHintsIcon = Sprite(0,1,1)

        # Main menu
        self.titleTextBox = Textbox(self.screenWidth//2-self.buttonWidth//2, 50,
                            self.buttonWidth, self.buttonHeight, "Antibot", bgColour=11)
        self.newGameButton = Button(self.screenWidth//2 - self.buttonWidth//2,
                                    self.screenHeight//2 - self.buttonHeight//2,
                                    self.buttonWidth,self.buttonHeight,"New Game", bgColour=3)
        
        self.settingsButton = Button(self.trayWidth, self.screenHeight//2-self.buttonWidth//2,
                                     self.buttonHeight,self.buttonWidth,"O/O", bgColour=3, sprite=self.settingsIcon, hoverSprite=self.hoverSettingsIcon)
        self.hintsButton = Button(-self.buttonHeight,self.screenHeight//2-self.buttonWidth//2,
                                  self.buttonHeight,self.buttonWidth,"?", bgColour=3, sprite=self.hintsIcon, hoverSprite=self.hoverHintsIcon)

        self.pieceSprites = {
            PieceColour.WHITE: {
                PieceType.ROOK: Sprite(1, 0, 0, 15),
                PieceType.PAWN: Sprite(1, 1, 0, 15),
                PieceType.BISHOP: Sprite(1, 2, 0, 15),
                PieceType.KNIGHT: Sprite(1, 3, 0, 15),
                PieceType.QUEEN: Sprite(1, 4, 0, 15),
                PieceType.KING: Sprite(1, 5, 0, 15)
            },

            PieceColour.BLACK: {
                PieceType.ROOK: Sprite(1, 0, 1, 15),
                PieceType.PAWN: Sprite(1, 1, 1, 15),
                PieceType.BISHOP: Sprite(1, 2, 1, 15),
                PieceType.KNIGHT: Sprite(1, 3, 1, 15),
                PieceType.QUEEN: Sprite(1, 4, 1, 15),
                PieceType.KING: Sprite(1, 5, 1, 15)
            }
        }

        self.hintsBoard = BoardView(0,50,12)

    def update(self):
        mouseX = pyxel.mouse_x
        mouseY = pyxel.mouse_y
        mousePressed = pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)

        self.animateTrays()

        if self.currentTray != TrayState.NONE:
            self.updateOpenTray(mouseX, mouseY, mousePressed)
            return
        
        if self.currentScreen == ScreenState.MAIN_MENU:
            self.updateMainMenu(mouseX, mouseY, mousePressed)
        elif self.currentScreen == ScreenState.GAME:
            self.updateGame(mouseX, mouseY, mousePressed)


    # Trays

    def animateTrays(self):
        targetSettingsX = 0 if self.currentTray == TrayState.SETTINGS else -self.trayWidth
        self.settingsX += (targetSettingsX - self.settingsX) * 0.15

        targetHintsX = (self.screenWidth - self.trayWidth) if self.currentTray == TrayState.HINTS else self.screenWidth
        self.hintsX += (targetHintsX - self.hintsX) * 0.15

        if abs(self.settingsX + self.trayWidth) < 0.5:
            self.visibleTrays.discard(TrayState.SETTINGS)
        if abs(self.hintsX - self.screenWidth) < 0.5:
            self.visibleTrays.discard(TrayState.HINTS)

    def openTray(self, tray):
        self.currentTray = tray
        self.visibleTrays.add(tray)
        self.clearSelection()

    def closeTray(self):
        self.currentTray = TrayState.NONE

    def updateOpenTray(self, mouseX, mouseY, mousePressed):
        if not mousePressed:
            return

        if self.currentTray == TrayState.SETTINGS:
            if self.hintsButton.isClicked(mouseX, mouseY, mousePressed, self.hintsX):
                self.openTray(TrayState.HINTS)
            elif mouseX >= self.settingsX + self.trayWidth:
                self.closeTray()
            elif self.settingsButton.isClicked(mouseX, mouseY, mousePressed, self.settingsX):
                self.closeTray()

        elif self.currentTray == TrayState.HINTS:
            if self.settingsButton.isClicked(mouseX, mouseY, mousePressed, self.settingsX):
                self.openTray(TrayState.SETTINGS)
            elif mouseX < self.hintsX:
                self.closeTray()
            elif self.hintsButton.isClicked(mouseX, mouseY, mousePressed, self.hintsX):
                self.closeTray()
    
    # Draw

    def draw(self):
        pyxel.cls(11)

        match self.currentScreen:
            case ScreenState.MAIN_MENU:
                self.drawMainMenu()
            case ScreenState.GAME:
                self.drawGame()
            case ScreenState.GAME_OVER:
                self.drawGameOver()

        if TrayState.SETTINGS in self.visibleTrays:
            self.drawSettings()
        if TrayState.HINTS in self.visibleTrays:
            self.drawHints()

        self.settingsButton.draw(self.settingsX)
        self.hintsButton.draw(self.hintsX)
        

    def setScreen(self, targetScreen):
        self.currentScreen = targetScreen


    # Main menu

    def drawMainMenu(self):
            self.titleTextBox.draw()
            self.newGameButton.draw()

    def updateMainMenu(self, mouseX, mouseY, mousePressed):
        if self.newGameButton.isClicked(mouseX, mouseY, mousePressed):
            self.game.reset()
            self.setScreen(ScreenState.GAME)
        elif self.settingsButton.isClicked(mouseX, mouseY, mousePressed, self.settingsX):
            self.openTray(TrayState.SETTINGS)
        elif self.hintsButton.isClicked(mouseX, mouseY, mousePressed, self.hintsX):
            self.openTray(TrayState.HINTS)


    # Settings

    def drawSettings(self):
            pyxel.rect(self.settingsX, 0, self.trayWidth, self.screenHeight, 3)
            pyxel.text(self.settingsX + self.trayWidth // 2 - 24, 40, "Settings", 7)


    # Hints

    def drawHints(self):
        pyxel.rect(self.hintsX, 0, self.trayWidth, self.screenHeight, 3)
        pyxel.text(self.hintsX + self.trayWidth // 2 - 24, 40, "Hints", 7)

        self.hintsBoard.boardX = self.hintsX + 50
        self.hintsBoard.draw()


    # Game

    def drawGame(self):
        self.boardView.draw(self.game.board, self.pieceSprites)
        self.drawMoveHighlights()

    def drawMoveHighlights(self):
        if self.selectedSquare is not None:
            row, col = self.selectedSquare
            squareX, squareY = self.boardView.getSquarePosition(row, col)
            pyxel.rectb(squareX, squareY, self.boardView.SQUARESIZE, self.boardView.SQUARESIZE, 10)

        destinations = {move.end: move for move in self.selectedMoves}

        for destination, move in destinations.items():
            row, col = destination
            squareX, squareY = self.boardView.getSquarePosition(row, col)
            size = self.boardView.SQUARESIZE

            if move.isCapture:
                pyxel.rectb(squareX + 2, squareY + 2, size - 4, size - 4, 8)
            else:
                pyxel.circ(squareX + size //2, squareY + size //2, 2, 8)

    def updateGame(self, mouseX, mouseY, mousePressed):
        if not mousePressed:
            return

        self.handleBoardClick(self.boardView.getSquareFromMouse(mouseX, mouseY))

        if self.settingsButton.isClicked(mouseX, mouseY, mousePressed, self.settingsX):
            self.openTray(TrayState.SETTINGS)
            return
        elif self.hintsButton.isClicked(mouseX, mouseY, mousePressed, self.hintsX):
            self.openTray(TrayState.HINTS)
            return

    def handleBoardClick(self, square):
        if square is None:
            self.clearSelection()
            return

        # If legal destination make move
        if self.selectedSquare is not None:
            matchingMoves = [move for move in self.selectedMoves if move.end == square]
            if matchingMoves:
                selectedMove = next((move for move in matchingMoves if move.promotionType == PieceType.QUEEN), matchingMoves[0])

                if self.game.makeMove(selectedMove):
                    self.clearSelection()
                    self.game.updateGameOver()
                    if self.game.gameFinished:
                        self.setScreen(ScreenState.GAME_OVER)
                return

        # Clicking pieces selects it

        row, col = square
        piece = self.game.board.getPiece(row, col)
        if piece is not None and piece.colour == self.game.currentTurn:
            if square == self.selectedSquare:
                self.clearSelection()
                return
            
            legalMoves = self.game.getLegalMoves(row, col)
            if legalMoves:
                self.selectedSquare = square
                self.selectedMoves = legalMoves
            else:
                self.clearSelection()
        else:
            self.clearSelection()

    def clearSelection(self):
        self.selectedSquare = None
        self.selectedMoves = []

    # Game Over

    def drawGameOver(self):
        pyxel.text(125, 90, "GAME OVER", 7)


# To run in browser: https://kitao.github.io/pyxel/web/launcher/?run=astronot09%2FAntibot%2Fmain%2Fantibot&gamepad=enabled
# Browser URL maker: https://kitao.github.io/pyxel/wasm/launcher/?<Command>=<GitHub username>.<Repository Name>.<App Directories>.<File Name Without Extension>
