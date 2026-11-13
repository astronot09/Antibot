import pyxel

# Button class

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
            actualX <= mouseX and mouseX < actualX + self.width
            and self.y <= mouseY and mouseY < self.y + self.height
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

            spriteX = actualX + (self.width - spriteToDraw.width) // 2
            spriteY = self.y + (self.height - spriteToDraw.height) // 2

            spriteToDraw.draw(spriteX, spriteY)
        else:
            textX = actualX + (self.width - len(self.text) * 4) // 2
            textY = self.y + (self.height - 5) // 2
            pyxel.text(textX, textY, self.text, self.textColour)