from card import Card

class Hand:
    def __init__(self):
        self.tenCards = range(0, 10, 1)
        self.Cards = [Card(), Card(), Card(), Card(), Card()]
        self.holdKarte1 = 0
        self.holdKarte2 = 0
        self.holdKarte3 = 0
        self.holdKarte4 = 0
        self.holdKarte5 = 0
