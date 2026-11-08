import pyxel
from enum import Enum, auto

# Enums

class ScreenState(Enum):
    MAIN_MENU = auto()
    SETTINGS = auto()
    RULES = auto()
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

    def isMouseOver(self, mouseX, mouseY):
        return (
            self.x <= mouseX and mouseX <= self.x + self.width
            and self.y <= mouseY and mouseY <= self.y + self.height
        )

    def isClicked(self, mouseX, mouseY, mousePressed):
        return mousePressed and self.isMouseOver(mouseX, mouseY)

    def draw(self):
        mouseOver = self.isMouseOver(pyxel.mouse_x, pyxel.mouse_y)

        if mouseOver:
            buttonColour = 12
        else:
            buttonColour = 5

        # Draw button background
        pyxel.rect(
            self.x,
            self.y,
            self.width,
            self.height,
            buttonColour
        )

        # Draw button border
        pyxel.rectb(
            self.x,
            self.y,
            self.width,
            self.height,
            7
        )

        textX = self.x + (self.width - len(self.text) * 4) // 2
        textY = self.y + (self.height - 5) // 2

        pyxel.text(textX, textY, self.text, 7)


class GUI:
    def __init__(self, screenWidth, screenHeight):
        pyxel.init(screenWidth, screenHeight, title="Antibot", display_scale=None, fps=60)

        pyxel.load("myantibot.pyxres")

        pyxel.mouse(True)

        self.currentScreen = ScreenState.MAIN_MENU

        pyxel.run(self.update, self.draw)

    def update(self):
        mouseX = pyxel.mouse_x
        mouseY = pyxel.mouse_y
        mousePressed = pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)

    def draw(self):
        if self.currentScreen == ScreenState.MAIN_MENU:
            self.drawMainMenu()

    def drawMainMenu(self):

            pyxel.cls(1)

            # Title
            pyxel.text(155, 35, "ANTIBOT", 7)


GUI(640, 360)