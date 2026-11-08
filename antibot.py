import pyxel
from enum import Enum, auto

# Enums

class ScreenState(Enum):
    MAIN_MENU = auto()
    SETTINGS = auto()
    HINTS = auto()
    GAME = auto()
    GAME_OVER = auto()


class Difficulty(Enum):
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()



# Button Class

class Button:
    def __init__(self, x, y, width, height, text, bgColour=0, textColour=7):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.bgColour = bgColour
        self.textColour = textColour

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

        if mouseOver:
            buttonColour = 5
        else:
            buttonColour = self.bgColour

        # Draw button background
        pyxel.rect(actualX, self.y, self.width, self.height, buttonColour)

        # Draw button border
        #pyxel.rectb(actualX, self.y, self.width, self.height, 7)

        textX = actualX + (self.width - len(self.text) * 4) // 2
        textY = self.y + (self.height - 5) // 2
        pyxel.text(textX, textY, self.text, 7)


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

        self.buttonHeight = 25
        self.buttonWidth = 125

        self.trayWidth = int(screenWidth * 0.75)
        self.settingsX = -self.trayWidth # Is hidden on left
        self.hintsX = self.screenWidth # Is hidden on right

        self.createScreenObjects()
        pyxel.run(self.update, self.draw)

    def createScreenObjects(self):

        # Main menu
        self.titleTextBox = Textbox(self.screenWidth//2-self.buttonWidth//2, 50,
                            self.buttonWidth, self.buttonHeight, "Antibot", bgColour=11)
        self.newGameButton = Button(self.screenWidth//2 - self.buttonWidth//2,
                                    self.screenHeight//2 - self.buttonHeight//2,
                                    self.buttonWidth,self.buttonHeight,"New Game", bgColour=3)
        
        self.settingsButton = Button(self.trayWidth, self.screenHeight//2-self.buttonWidth//2,
                                     self.buttonHeight,self.buttonWidth,"O/O", bgColour=3)
        self.hintsButton = Button(-self.buttonHeight,self.screenHeight//2-self.buttonWidth//2,
                                  self.buttonHeight,self.buttonWidth,"?", bgColour=3)

    def update(self):
        mouseX = pyxel.mouse_x
        mouseY = pyxel.mouse_y
        mousePressed = pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)

        self.animateTrays()

        match self.currentScreen:
            case ScreenState.MAIN_MENU:
                self.updateMainMenu(mouseX, mouseY, mousePressed)
            case ScreenState.SETTINGS:
                self.updateSettings(mouseX, mouseY, mousePressed)
            case ScreenState.HINTS:
                self.updateHints(mouseX, mouseY, mousePressed)

    def draw(self):
        pyxel.cls(11)

        self.drawMainMenu()

        if self.settingsX > -self.trayWidth:
            self.drawSettings()
        if self.hintsX < self.screenWidth:
            self.drawHints()
    
    def animateTrays(self):
        targetSettingsX = 0 if self.currentScreen == ScreenState.SETTINGS else -self.trayWidth
        self.settingsX += (targetSettingsX - self.settingsX) * 0.15

        targetHintsX = (self.screenWidth - self.trayWidth) if self.currentScreen == ScreenState.HINTS else self.screenWidth
        self.hintsX += (targetHintsX - self.hintsX) * 0.15

    def openScreen(self, targetScreen):
        self.currentScreen = targetScreen


    # Main menu

    def drawMainMenu(self):
            self.titleTextBox.draw()
            self.newGameButton.draw()

            if self.currentScreen != ScreenState.SETTINGS:
                self.settingsButton.draw(self.settingsX)
            if self.currentScreen != ScreenState.HINTS:
                self.hintsButton.draw(self.hintsX)

    def updateMainMenu(self, mouseX, mouseY, mousePressed):
        if self.newGameButton.isClicked(mouseX, mouseY, mousePressed):
            # start new game
            pass
        elif self.settingsButton.isClicked(mouseX, mouseY, mousePressed, self.settingsX):
            self.openScreen(ScreenState.SETTINGS)
        elif self.hintsButton.isClicked(mouseX, mouseY, mousePressed, self.hintsX):
            self.openScreen(ScreenState.HINTS)


    # Settings

    def drawSettings(self):

            pyxel.rect(self.settingsX, 0, self.trayWidth, self.screenHeight, 3)

            # Title
            pyxel.text(self.settingsX + self.trayWidth // 2 - 24, 40, "Settings", 7)
            # Tray's coords used for elements inside
            self.settingsButton.draw(self.settingsX)

    def updateSettings(self, mouseX, mouseY, mousePressed):

        if self.settingsButton.isClicked(mouseX, mouseY, mousePressed, self.settingsX):
            self.openScreen(ScreenState.MAIN_MENU)


    # Hints

    def drawHints(self):
        pyxel.rect(self.hintsX, 0, self.trayWidth, self.screenHeight, 3)

        pyxel.text(self.hintsX + self.trayWidth // 2 - 24, 40, "Hints", 7)

        # Buttons
        self.hintsButton.draw(self.hintsX)

    def updateHints(self, mouseX, mouseY, mousePressed):
        if self.hintsButton.isClicked(mouseX, mouseY, mousePressed, self.hintsX):
            self.openScreen(ScreenState.MAIN_MENU)

GUI(640,360)