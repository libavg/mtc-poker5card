#!/usr/bin/python2.5

import os,  random
from libavg import avg
from libavg import Point2D
from libavg import AVGApp
from libavg.AVGAppUtil import getMediaDir
from pokereval import PokerEval

from card import Card
from hand import Hand

g_player = avg.Player.get()
pokereval = PokerEval()
myHand = None
holdarray = ["hold1",  "hold2",  "hold3",  "hold4",  "hold5"]
kartenarray = ["karte1",  "karte2",  "karte3",  "karte4",  "karte5"]
wintablearray = ["RoyalFlush", "StraightFlush", "Quads", "FullHouse", "Flush", "Straight", "Trips", "TwoPair", "OnePair"]
winpointsarray = ["10000",  "5000",  "3000",  "1000",  "300", "200", "50", "30",  "10"]


def slurp(filename):
    filename = getMediaDir(__file__, filename)
    f = open(filename,'r')
    contents = f.read()
    f.close()
    return contents


class Game(AVGApp):
    multitouch = True
    def init(self):
        self._parentNode.mediadir = getMediaDir(__file__, '.')
        mainNode = g_player.createNode(slurp("mtc5Poker5CardDraw.avg"))
        self._parentNode.appendChild(mainNode)
        g_player.getElementByID("buttonExit").setEventHandler(avg.CURSORUP,  avg.MOUSE | avg.TOUCH , lambda e: self.leave())

    def _enter(self):
        g_player.getElementByID("buttonStart").setEventHandler(avg.CURSORDOWN,  avg.MOUSE | avg.TOUCH , lambda e: self.startGame())

    def startGame(self):
        global myHand
        g_player.getElementByID("buttonStart").text = "Deal"
        g_player.getElementByID("buttonStart").setEventHandler(avg.CURSORDOWN,  avg.MOUSE | avg.TOUCH ,  self.DealCards)
        self.turn = 1
        self.money = 1000
        g_player.getElementByID("credits").text = "Credits = " + str(self.money)
        myHand = Hand()
        self.NewGame()
        self.SetPictures()
        self.ShowCards()
        
    def NewGame(self):
        global myHand
        myHand.holdKarte1 = 0
        myHand.holdKarte2 = 0
        myHand.holdKarte3 = 0
        myHand.holdKarte4 = 0
        myHand.holdKarte5 = 0
        for s in range(len(holdarray)):
            g_player.getElementByID(holdarray[s]).color = "000000"
        g_player.getElementByID("textzeile").text = ""
        for s in range(len(wintablearray)):
            g_player.getElementByID(wintablearray[s]).color = "FFFFFF"
        
    def SetPictures(self):
        global myHand
        for i in range(0, 5):
            myHand.Cards[i].NumberToPicture()

    def ShowCards(self):
        global g_player
        for s in range(len(kartenarray)):
            dummykarte = myHand.Cards[s].getPicture()
            g_player.getElementByID(kartenarray[s]).href = dummykarte
            g_player.getElementByID(kartenarray[s]).height = 160
            g_player.getElementByID(kartenarray[s]).width = 100
        
    def DealCards(self, event):
        global g_player
        self.NewGame()
        self.money -= 5
        g_player.getElementByID("credits").text = "Credits = " + str(self.money)
        zaehler = 0 
        for i in range(0, 10, 1):
            myHand.tenCards[i] = 0
        while zaehler < 10:
            dummynumber = random.randrange(1, 52, 1)
            if not dummynumber in myHand.tenCards:
                myHand.tenCards[zaehler] = dummynumber
                zaehler += 1
                        
        g_player.getElementByID("buttonStart").setEventHandler(avg.CURSORDOWN,  avg.MOUSE | avg.TOUCH ,  self.ChangeCards)
        g_player.getElementByID("karte1").setEventHandler(avg.CURSORDOWN,  avg.MOUSE | avg.TOUCH ,  self.HoldKarte1)
        g_player.getElementByID("karte2").setEventHandler(avg.CURSORDOWN,  avg.MOUSE | avg.TOUCH ,  self.HoldKarte2)
        g_player.getElementByID("karte3").setEventHandler(avg.CURSORDOWN,  avg.MOUSE | avg.TOUCH ,  self.HoldKarte3)
        g_player.getElementByID("karte4").setEventHandler(avg.CURSORDOWN,  avg.MOUSE | avg.TOUCH ,  self.HoldKarte4)
        g_player.getElementByID("karte5").setEventHandler(avg.CURSORDOWN,  avg.MOUSE | avg.TOUCH ,  self.HoldKarte5)
        
        for i in range(0, 5, 1):
            myHand.Cards[i].Number = myHand.tenCards[i]
            myHand.Cards[i].NumberToPicture()
        self.ShowCards()
                
    def ChangeCards(self, event):
        if myHand.holdKarte1 == 0:
            myHand.Cards[0].Number = int(myHand.tenCards[5])
        if myHand.holdKarte2 == 0:
            myHand.Cards[1].Number = int(myHand.tenCards[6])
        if myHand.holdKarte3 == 0:
            myHand.Cards[2].Number = int(myHand.tenCards[7])
        if myHand.holdKarte4 == 0:
            myHand.Cards[3].Number = int(myHand.tenCards[8])
        if myHand.holdKarte5 == 0:
            myHand.Cards[4].Number = int(myHand.tenCards[9])
        for i in range(0, 5, 1):
            myHand.Cards[i].NumberToPicture()
        g_player.getElementByID("buttonStart").setEventHandler(avg.CURSORDOWN,  avg.MOUSE | avg.TOUCH ,  self.DealCards)
        self.ShowCards()
        self.CheckWin()
        
    def CheckWin(self):
        Akkr = ["00","Ac","As","Ah","Ad","Kc","Ks","Kh","Kd","Qc","Qs","Qh","Qd","Jc","Js","Jh","Jd","Tc","Ts","Th","Td","9c","9s","9h","9d","8c","8s","8h","8d","7c","7s","7h","7d","6c","6s","6h","6d","5c","5s","5h","5d","4c","4s","4h","4d","3c","3s","3h","3d","2c","2s","2h","2d"]
        hand = [Akkr[myHand.Cards[0].Number], Akkr[myHand.Cards[1].Number], Akkr[myHand.Cards[2].Number], Akkr[myHand.Cards[3].Number], Akkr[myHand.Cards[4].Number] ]
        # best_hand = pokereval.best_hand("hi", hand)
        testmu = pokereval.best("hi", hand)
        testmu2 = testmu[1]
        testmu3 = testmu2[0]
        # g_player.getElementByID("textzeile").text = testmu3
        if not testmu3 == "NoPair":
            node = g_player.getElementByID(str(testmu3))
            if node:
                node.color = "FF0000"
                self.money += int(winpointsarray[wintablearray.index(str(testmu3))])
                g_player.getElementByID("credits").text = "Credits = " + str(self.money)
            
    def HoldKarte1(self,  event):
            global g_player,  myHand
            if myHand.holdKarte1 == 0:
                myHand.holdKarte1 = 1
                g_player.getElementByID("hold1").color = "FFFFFF"
            else:
                myHand.holdKarte1 = 0
                g_player.getElementByID("hold1").color = "000000"
            
    def HoldKarte2(self,  event):
            global g_player,  myHand
            if myHand.holdKarte2 == 0:
                myHand.holdKarte2 = 1
                g_player.getElementByID("hold2").color = "FFFFFF"
            else:
                myHand.holdKarte2 = 0
                g_player.getElementByID("hold2").color = "000000"
                
    def HoldKarte3(self,  event):
            global g_player,  myHand
            if myHand.holdKarte3 == 0:
                myHand.holdKarte3 = 1
                g_player.getElementByID("hold3").color = "FFFFFF"
            else:
                myHand.holdKarte3 = 0
                g_player.getElementByID("hold3").color = "000000"
            
    def HoldKarte4(self,  event):
            global g_player,  myHand
            if myHand.holdKarte4 == 0:
                myHand.holdKarte4 = 1
                g_player.getElementByID("hold4").color = "FFFFFF"
            else:
                myHand.holdKarte4 = 0
                g_player.getElementByID("hold4").color = "000000"
                
    def HoldKarte5(self,  event):
            global g_player,  myHand
            if myHand.holdKarte5 == 0:
                myHand.holdKarte5 = 1
                g_player.getElementByID("hold5").color = "FFFFFF"
            else:
                myHand.holdKarte5 = 0
                g_player.getElementByID("hold5").color = "000000"


if __name__=='__main__':
    Game.start(resolution=(1280,720))

