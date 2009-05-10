

class Card:
    def __init__(self):
        self.Number = 0
        self.Picture = "media/cards/0.png"
    def setNumber(self, number):
        self.Number = number
    def getNumber(self):
        return self.Number
    def getPicture(self):
        return self.Picture
    def NumberToPicture(self):
        self.Picture = "media/cards/" + str(self.getNumber()) + ".png"
