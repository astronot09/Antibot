import pyxel
from enum import Enum, auto

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

# Sprite class

class Sprite:
    def __init__(self, imageBank, sourceX, sourceY, width, height, transparentColour=None):
        self.imageBank = imageBank

        self.sourceX = sourceX
        self.sourceY = sourceY
        self.width = width
        self.height = height

        self.transparentColour = transparentColour

    def draw(self, x, y, scale=1):
        pyxel.blt(x, y, self.imageBank, self.sourceX, self.sourceY, self.width, self.height, self.transparentColour, scale=scale)


# Button Class

class Button:
    def __init__(self, x, y, width, height, text, bgColour=0, textColour=7, sprite=None, hoverSprite=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.bgColour = bgColour
        self.textColour = textColour
        self.sprite = sprite
        self.hoverSprite = hoverSprite

    def isMouseOver(self, mouseX, mouseY, offsetX = 0):
        actualX = self.x + offsetX
        return (
            actualX <= mouseX and mouseX <= actualX + self.width
            and self.y <= mouseY and mouseY <= self.y + self.height
        )

    def isClicked(self, mouseX, mouseY, mousePressed, offSetX=0):
        return mousePressed and self.isMouseOver(mouseX, mouseY,offSetX)

    def draw(self, offsetX=0):
        actualX = self.x + offsetX
        mouseOver = self.isMouseOver(pyxel.mouse_x, pyxel.mouse_y, offsetX)

        buttonColour = 5 if mouseOver else self.bgColour

        # Draw button background
        pyxel.rect(actualX, self.y, self.width, self.height, buttonColour)

        # Draw button border
        #pyxel.rectb(actualX, self.y, self.width, self.height, 7)

        if self.sprite != None:

            spriteToDraw = self.sprite

            if mouseOver and self.hoverSprite != None:
                spriteToDraw = self.hoverSprite

            self.spriteX = actualX + (self.width - spriteToDraw.width) // 2
            self.spriteY = self.y + (self.height - spriteToDraw.height) // 2

            spriteToDraw.draw(self.spriteX, self.spriteY)
        else:
            textX = actualX + (self.width - len(self.text) * 4) // 2
            textY = self.y + (self.height - 5) // 2
            pyxel.text(textX, textY, self.text, self.textColour)


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

        pyxel.init(screenWidth, screenHeight, title="Antibot", display_scale=None, fps=60)
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

        self.createScreenObjects()
        pyxel.run(self.update, self.draw)

    def createScreenObjects(self):
        # Icons
        self.settingsIcon = Sprite(0,0,0,8,8)
        self.hoverSettingsIcon = Sprite(0,8,0,8,8)

        # Main menu
        self.titleTextBox = Textbox(self.screenWidth//2-self.buttonWidth//2, 50,
                            self.buttonWidth, self.buttonHeight, "Antibot", bgColour=11)
        self.newGameButton = Button(self.screenWidth//2 - self.buttonWidth//2,
                                    self.screenHeight//2 - self.buttonHeight//2,
                                    self.buttonWidth,self.buttonHeight,"New Game", bgColour=3)
        
        self.settingsButton = Button(self.trayWidth, self.screenHeight//2-self.buttonWidth//2,
                                     self.buttonHeight,self.buttonWidth,"O/O", bgColour=3, sprite=self.settingsIcon, hoverSprite=self.hoverSettingsIcon)
        self.hintsButton = Button(-self.buttonHeight,self.screenHeight//2-self.buttonWidth//2,
                                  self.buttonHeight,self.buttonWidth,"?", bgColour=3)

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
            self.setScreen(ScreenState.GAME)
        elif self.settingsButton.isClicked(mouseX, mouseY, mousePressed, self.settingsX):
            self.openTray(TrayState.SETTINGS)
        elif self.hintsButton.isClicked(mouseX, mouseY, mousePressed, self.hintsX):
            self.openTray(TrayState.HINTS)


    # Settings

    def drawSettings(self):
            pyxel.rect(self.settingsX, 0, self.trayWidth, self.screenHeight, 3)

            # Title
            pyxel.text(self.settingsX + self.trayWidth // 2 - 24, 40, "Settings", 7)


    # Hints

    def drawHints(self):
        pyxel.rect(self.hintsX, 0, self.trayWidth, self.screenHeight, 3)

        pyxel.text(self.hintsX + self.trayWidth // 2 - 24, 40, "Hints", 7)


    # Game

    def drawGame(self):
        pyxel.cls(4)

    def updateGame(self, mouseX, mouseY, mousePressed):
        if self.settingsButton.isClicked(mouseX, mouseY, mousePressed, self.settingsX):
            self.openTray(TrayState.SETTINGS)
        elif self.hintsButton.isClicked(mouseX, mouseY, mousePressed, self.hintsX):
            self.openTray(TrayState.HINTS)

    # Game Over

    def drawGameOver(self):
        pyxel.text(125, 90, "GAME OVER", 7)
    
GUI(320,180)