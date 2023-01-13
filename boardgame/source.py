import itertools
from sklearn.utils import shuffle
import wx
import random

def scale_bitmap(bitmap, width, height):
    image = bitmap.ConvertToImage()
    image = image.Scale(int(width), int(height), wx.IMAGE_QUALITY_HIGH)
    result = wx.Bitmap(image)
    return result
#card
class card:
    def __init__(self, bitmap, type, value):
        self.image = scale_bitmap(bitmap,224/4,312/4)
        self.type = type
        self.value = value
        self.enlarge = False
    
    def get_type(self):
        return self.type
    def set_type(self,type):
        self.type = type

    def set_value(self,val):
        self.value = val
    def get_value(self):
        return self.value

    def get_card_bitmap(self):
        return self.image
#deck
class deck:
    def __init__(self):
        self.deck_of_card = []
        for i in range(2,14):
            link = "card\\" + str(i)+"hearts.png"
            image = wx.Bitmap(link)
            self.deck_of_card.append(card(image,"hearts",i))

        for i in range(2,14):
            link = "card\\" + str(i)+"dia.png"
            image = wx.Bitmap(link)
            self.deck_of_card.append(card(image,"dia",i))

        for i in range(2,14):
            link = "card\\" + str(i)+"spades.png"
            image = wx.Bitmap(link)
            self.deck_of_card.append(card(image,"spades",i))

        for i in range(2,14):
            link = "card\\" + str(i)+"clubs.png"
            image = wx.Bitmap(link)
            self.deck_of_card.append(card(image,"clubs",i))

    def print_deck(self):
         for i in range(0,len(self.deck_of_card)):
            print(self.deck_of_card[i].get_name())


#chip
class chip:
    h = 20
    w = 20
    def __init__(self) :
        self.value = 0
        self.image = wx.Bitmap()
        

    def chip_value(self):
        return self.value
    def chip_image(self):
        return self.image

#red
class redchip(chip):
    def __init__(self):
        self.value = 5
        bitmap = wx.Bitmap("chip\\red.png")
        self.image = scale_bitmap(bitmap,self.h,self.w)

#white
class whitechip(chip):
    def __init__(self):
        self.value = 1
        bitmap = wx.Bitmap("chip\\white.png")
        self.image = scale_bitmap(bitmap,self.h,self.w)

#black
class blackchip(chip):
    def __init__(self):
        self.value = 100
        bitmap = wx.Bitmap("chip\\black.png")
        self.image = scale_bitmap(bitmap,self.h,self.w)

#maroon
class maroonchip(chip):
    def __init__(self):
        self.value = 1000  
        bitmap = wx.Bitmap("chip\\maroon.png")
        self.image = scale_bitmap(bitmap,self.h,self.w)      

#yellow
class yellowchip(chip):
    def __init__(self):
        self.value = 20
        bitmap = wx.Bitmap("chip\\yellow.png")
        self.image = scale_bitmap(bitmap,self.h,self.w)

#orange
class orangechip(chip):
    def __init__(self):
        self.value = 10
        bitmap = wx.Bitmap("chip\\orange.png")
        self.image = scale_bitmap(bitmap,self.h,self.w)
#green
class greenchip(chip):
    def __init__(self):
        self.value = 25
        bitmap = wx.Bitmap("chip\\green.png")
        self.image = scale_bitmap(bitmap,self.h,self.w)
#purple
class purplechip(chip):
    def __init__(self):
        self.value = 500
        bitmap = wx.Bitmap("chip\\purple.png")
        self.image = scale_bitmap(bitmap,self.h,self.w)

class BetArea(wx.Panel):
    w = 300
    h = 100
    def __init__(self, parent, position, player_area, timer):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, size = wx.Size( self.w, self.h ), style = wx.TAB_TRAVERSAL )
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )  
        self.Centre() 
        self.SetPosition(position)
        self.active_player_area = player_area#widget that show player's details
        self.active_player = player_area.get_player()#player
        self.timer = timer
        
        self.sc_money = wx.SpinCtrl(self, pos=(10,10),
              size=(250,50), style=wx.SP_ARROW_KEYS, min=self.Parent.minbet, max=150, initial=0)
        self.button = wx.Button(self, label = "confirm", pos = (20,70))
        self.button.Bind(wx.EVT_BUTTON, self.confirm)
        self.Show(False)

    def confirm(self,event):
        self.Show(False)
        self.active_player.moneyraise(self.sc_money.GetValue())
        self.Parent.poolArea.addToPool(self.sc_money.GetValue())
        self.Parent.minbet = self.sc_money.GetValue()
        self.active_player_area.Refresh()
        self.timer.Start(1000)
        self.Parent.fold_button.Show(False)
        self.Parent.raise_button.Show(False)
        self.Parent.call_button.Show(False)


class cardShownArea(wx.Panel):
    w = 300
    h = 100
    def __init__(self, parent, position, deck):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, size = wx.Size( self.w, self.h ), style = wx.TAB_TRAVERSAL )
        self.deck = deck
        
        self.shown_deck = []
        self.highlight = False
        self.Bind(wx.EVT_PAINT, self.OnPaint) 
        self.Centre() 
        self.SetPosition(position)
        self.Show(False)

    def drawFirstThree(self):
        for i in range(3):
            card_indx = random.randint(0, len(self.deck)-1)
            self.shown_deck.append(self.deck[card_indx])
            self.deck.remove(self.deck[card_indx])

    def drawCard(self):
        card_indx = random.randint(0, len(self.deck)-1)
        self.shown_deck.append(self.deck[card_indx])
        self.deck.remove(self.deck[card_indx])
        self.Refresh()


    def OnPaint(self, e): 
        dc = wx.PaintDC(self) 
        pen = wx.Pen(wx.Colour(0,0,0)) 
        dc.SetPen(pen) 
        
        #draw card owned to screen
        for i in range(len(self.shown_deck)):
            if not self.shown_deck[i].enlarge:
                dc.DrawBitmap(self.shown_deck[i].get_card_bitmap(),i*50,0)
            else:
                enl= scale_bitmap(self.shown_deck[i].get_card_bitmap(),224/2,312/2)
                dc.DrawBitmap(enl,i*50,0)


    def getCards(self):
        return self.shown_deck
            
        
    
  


#player
class player:
    def __init__(self, name):
        self.name = name
        self.money = 1500
        self.chip_update()

        
        self.player_hand = []
        self.folded = False
        self.action = ""
       
    
    def chip_update(self):
        money = self.money

        maroon = int(money/1000)
        money = money- maroon*1000

        purple = int(money/500)
        money = money- purple*500

        black = int(money/100)
        money = money- black*100

        green = int(money/25)
        money = money- green*25

        yellow = int(money/20)
        money = money- yellow*20

        orange = int(money/10)
        money = money- orange*10

        red = int(money/5)
        money = money- red*5
        white = money

        self.chiplist = [[whitechip() for i in range(white)], [redchip() for i in range(red)], [orangechip() for i in range(orange)],
                         [yellowchip() for i in range(yellow)],[greenchip() for i in range(green)],[blackchip() for i in range(black)],
                         [purplechip() for i in range(purple)],[maroonchip() for i in range(maroon)]]

    def money(self):
        return self.money

    def call(self,money):
        self.money = self.money - money
        self.chip_update()
        self.action = "call"

    def moneyraise(self,money):
        self.money = self.money - money
        self.chip_update()
        self.action = "raise"
     
    def small_bind(self):
        self.money = self.money - self.min_bet
    
    def fold(self):
        self.folded = True
        self.action = "fold"
        

    def cur_hand(self):
        return self.player_hand
    
    def add_chip(self, chip, amount):
        for i in range(0,amount):
            if (chip.chip_value() == 1):
               self.chiplist[0].append(chip)
            if (chip.chip_value() == 5):
               self.chiplist[1].append(chip)
            if (chip.chip_value() == 10):
               self.chiplist[2].append(chip)
            if (chip.chip_value() == 20):
               self.chiplist[3].append(chip)
            if (chip.chip_value() == 25):
               self.chiplist[4].append(chip)
            if (chip.chip_value() == 100):
               self.chiplist[5].append(chip)
            if (chip.chip_value() == 500):
               self.chiplist[6].append(chip)
            if (chip.chip_value() == 1000):
               self.chiplist[7].append(chip)
    def add_card_from(self,deck):
        card_indx = random.randint(0, len(deck)-1)
        self.player_hand.append(deck[card_indx])
        deck.remove(deck[card_indx])

class MoneyPoolArea(wx.Panel):
    w = 100
    h = 100
    def __init__(self, parent,position,money):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, size = wx.Size( int(self.w), int(self.h) ), style = wx.TAB_TRAVERSAL )
        self.money = money
        self.SetBackgroundColour( wx.Colour( 0, 255, 255 ) )  
        self.Bind(wx.EVT_PAINT, self.OnPaint) 
        self.Centre() 
        self.SetPosition(position)
        self.Show(True)
    def OnPaint(self, e): 
        dc = wx.PaintDC(self) 
        pen = wx.Pen(wx.Colour(0,0,0)) 
        dc.SetPen(pen) 
        dc.DrawText(str(self.money)+"$$",40,40)
    def addToPool(self,money):
        self.money+= money
        self.Refresh()


class PlayerArea(wx.Panel):
    w = 210
    h = 160
    def __init__(self, parent, player_,position,deck):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, size = wx.Size( self.w, self.h ), style = wx.TAB_TRAVERSAL )
        #get the deck that is in use from main
        self.deck = deck
        # add two cards into player's hand
        player_.add_card_from(self.deck)
        player_.add_card_from(self.deck)
        self.p1 = player_
        self.action = ""
        self.final_hand = ""
        if player_.name == "You":
            self.is_you = True
        else:
            self.is_you = False

        self.name_label = scale_bitmap(wx.Bitmap("ui\\name_label.png"),100,30)#name
        self.money_label = scale_bitmap(wx.Bitmap("ui\\money_label.png"),80,40)#money
        self.chat_label = scale_bitmap(wx.Bitmap("ui\\chat_label.png"),80,40)#chat
        self.back_card = scale_bitmap(wx.Bitmap("ui\\back_card.jpg"),224/4,312/4)#back

        self.SetBackgroundColour( wx.Colour( 0, 255, 255 ) )  
        self.Bind(wx.EVT_PAINT, self.OnPaint) 
        self.Centre() 
        self.SetPosition(position)
        self.Show(True)

   
    def get_player(self):
        return self.p1  

    def center(self,size,x_cor,y_cor):
        return( [x_cor+size.x/2,y_cor+size.y/2] )

    

    
       

    def OnPaint(self, e): 
        dc = wx.PaintDC(self) 
        pen = wx.Pen(wx.Colour(0,0,0)) 
        dc.SetPen(pen) 
        
        #draw card owned to screen
        if self.is_you:
            for i in range(len(self.p1.cur_hand())):
                dc.DrawBitmap(self.p1.cur_hand()[i].get_card_bitmap(),i*50,0)
            dc.DrawBitmap(self.name_label,self.w-self.name_label.GetSize().x,0)
            dc.DrawBitmap(self.money_label,self.w-self.name_label.GetSize().x+10,self.name_label.GetSize().y)
           
            dc.DrawText(self.p1.name,150,6)
            dc.DrawText(str(self.p1.money)+"$",146,41)
    
        else:
            for i in range(len(self.p1.cur_hand())):
                dc.DrawBitmap(self.back_card,int(self.w-224/4-i*50),0)
            dc.DrawBitmap(self.name_label,0,0)
            dc.DrawBitmap(self.money_label,10,self.name_label.GetSize().y)
            dc.DrawText(self.p1.name,43-len(self.p1.name),6)
            dc.DrawText(str(self.p1.money)+"$",38,41)
        
        #draw chip to screen
        for i in range(len(self.p1.chiplist)):
            if not len(self.p1.chiplist[i]):
                pass
            if i == 0:
               
                for j in range(len(self.p1.chiplist[i])):
                    dc.DrawBitmap(self.p1.chiplist[i][0].chip_image(),120+j,int(self.h/2)+30)

            if i == 1:
                for j in range(len(self.p1.chiplist[i])):
                    dc.DrawBitmap(self.p1.chiplist[i][0].chip_image(),150+j,int(self.h/2)+30)

            if i == 2:
                for j in range(len(self.p1.chiplist[i])):
                    dc.DrawBitmap(self.p1.chiplist[i][0].chip_image(),180+j,int(self.h/2)+30)
            
            if i == 3:
                for j in range(len(self.p1.chiplist[i])):
                    dc.DrawBitmap(self.p1.chiplist[i][0].chip_image(),120+j,int(self.h/2)+55)
            
            if i == 4:
                for j in range(len(self.p1.chiplist[i])):
                    dc.DrawBitmap(self.p1.chiplist[i][0].chip_image(),150+j,int(self.h/2)+55)

            if i == 5:
                for j in range(len(self.p1.chiplist[i])):
                    dc.DrawBitmap(self.p1.chiplist[i][0].chip_image(),180+j,int(self.h/2)+55)

            if i == 6:
                for j in range(len(self.p1.chiplist[i])):
                    dc.DrawBitmap(self.p1.chiplist[i][0].chip_image(),120+j,int(self.h/2)+5)

            if i == 7:
                for j in range(len(self.p1.chiplist[i])):
                    dc.DrawBitmap(self.p1.chiplist[i][0].chip_image(),j+150,int(self.h/2)+5)
        
        if self.p1.action != "":
            dc.DrawBitmap(self.chat_label,12,int(self.h/2)+10)
            dc.DrawText(self.p1.action,40,int(self.h/2)+13)
            dc.DrawText(self.final_hand,40,int(self.h/2)+50)

            
            


def hand_check(hand):
    handVal = []#list of card value in player hadn
    cardFre = []#frequency of a card in the hand calculate using count()
    same_type = True
    result = ""
    result_hand = []

    for i in range (5):
        handVal.append(hand[i].get_value())
        if (i>0 and hand[i].get_type()!=hand[i-1].get_type()):
            same_type = False
    
    for i in range (5):
        cardFre.append(handVal.count(handVal[i]))


    if (sorted(handVal) == list(range(min(handVal), max(handVal)+1))) and same_type and handVal[0] == 10 :
        result = 10 #("Royal flush")
    elif (sorted(handVal) == list(range(min(handVal), max(handVal)+1))) and same_type :
        result = 9 #("Straight flush")

    elif (sorted(handVal) == list(range(min(handVal), max(handVal)+1))) and not same_type :
        result = 5 #("Straight")

    elif (sorted(handVal) != list(range(min(handVal), max(handVal)+1))) and same_type :
        result = 6 #("Flush")
    
    elif max(cardFre) == 4:
        result = 8 #("Four of a kind")

    elif max(cardFre) == 3 and sorted(set(cardFre))[-2] == 2:
        result = 7 #("Full house")

    elif max(cardFre) == 3 and sorted(set(cardFre))[-2] == 1:
        result = 4 #("Three of a kind")

    elif max(cardFre) == 2 and cardFre.count(2) == 4:
        result = 3 #("Two pair")
    
    elif max(cardFre) == 2 and cardFre.count(2) == 2:
        result = 2 #("Pair")

    elif max(cardFre) == 1:
        result = 1 #"High Card")

    return result
     





class Mywin(wx.Frame): 
          
    def __init__(self, parent, title): 
        super(Mywin, self).__init__(parent, title = title,size = (900,600))  
        self.InitUI() 
         
    def InitUI(self): 
        self.turn = 0
        self.count = 0
        self.minbet = 2
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )        
        self.Bind(wx.EVT_PAINT, self.OnPaint) 
        self.Centre() 
        
        self.init_player_and_deck()

        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.player_update, self.timer)
        self.timer.Start(1000)
       
        


        self.fold_button = wx.Button(self, label = "fold", pos = (280,500))
        self.fold_button.Bind(wx.EVT_BUTTON, self.onFoldButton)
        

        self.call_button = wx.Button(self, label = "call", pos = (360,500))
        self.call_button.Bind(wx.EVT_BUTTON, self.onCallButton)
       

        self.raise_button = wx.Button(self, label = "raise", pos = (440,500))
        self.raise_button.Bind(wx.EVT_BUTTON, self.onRaiseButton)
        
        self.continue_btt = wx.Button(self, label = "Continue ?", pos = (360,400))
        self.continue_btt.Bind(wx.EVT_BUTTON, self.onContinueButton)
        self.continue_btt.Show(False)
        
        self.hide_button()
        
        self.bet_area = BetArea(self, (int(self.Size.x/2-150),int(self.Size.y/2+100)), self.panel[2], self.timer) #150 is half width size of betArea
        self.cardShownPanel = cardShownArea(self,(int(self.Size.x*1/3),int(self.Size.y*1/3)) , self.new_deck.deck_of_card)
      
       


       

        self.Show(True)

    def init_player_and_deck(self):
        self.new_deck = deck()#create new deck
        random.shuffle(self.new_deck.deck_of_card)

        self.p1_panel = PlayerArea(self,player("Bob"), (200,0), self.new_deck.deck_of_card)
        self.p2_panel = PlayerArea(self,player("Alice"),(0,300),self.new_deck.deck_of_card)
        self.p3_panel = PlayerArea(self,player("You"),(600,300),self.new_deck.deck_of_card)
        self.p4_panel = PlayerArea(self,player("Your mom"),(600,0), self.new_deck.deck_of_card)

        self.panel = [self.p1_panel,self.p2_panel,self.p3_panel,self.p4_panel]
        self.initial_plr = random.randint(0,3)
        self.cur_player_num = self.initial_plr
        self.active_panel = self.panel[self.cur_player_num]
        self.active_panel.get_player().call(self.minbet)  

        self.poolArea = MoneyPoolArea(self, (int(self.Size.x/2+50),int(self.Size.y/2-300)),0)
        self.poolArea.addToPool(self.minbet)
        self.next()

        
        
    def hide_button(self):
        self.fold_button.Show(False)
        self.call_button.Show(False)
        self.raise_button.Show(False)

       
       
    def next(self): 
        self.cur_player_num = self.cur_player_num + 1
        if self.cur_player_num>3:
            self.cur_player_num = 0
        


        if (self.count == 4):
            self.turn = self.turn+1
            self.count = 0
            if self.turn == 1:
                self.cardShownPanel.Show(True)
                self.cardShownPanel.drawFirstThree()
            if self.turn >1:
                self.cardShownPanel.drawCard()
            if self.turn == 3:
                self.hand_check()
                self.timer.Stop()
                self.hide_button()


        self.count+=1
       
        
    def all_fold(self):
        count = 0
    
        for i in self.panel:
            if i.get_player().folded:
                count +=1
        if count == 3:
            for i in self.panel:
                if not i.get_player().folded:
                    self.timer.Stop()
                    i.SetBackgroundColour( wx.Colour( 0, 128, 255 ) )  
                    i.Refresh()
                    i.get_player().money+=self.poolArea.money
                    self.poolArea.money = 0
                    self.continue_btt.Show(True)
                    
        
            

        

    def player_update(self,event):
       
        self.active_panel = self.panel[self.cur_player_num]
        if (self.active_panel.get_player().folded):
            self.next()
            return
        if self.active_panel.get_player().name == "You":
            
            self.fold_button.Show(True)
            self.call_button.Show(True)
            self.raise_button.Show(True)
            print("your turn")
            self.bet_area.sc_money.SetMin(self.minbet)
            self.next()
            self.timer.Stop()  
            self.Refresh()
            return
        
       
        rand = random.randint(0, 2)
        money = random.randint(self.minbet, 150)
        print(self.active_panel.get_player().name)
        if rand == 0:
            self.active_panel.get_player().call(self.minbet)
           
            print("call")
        
        if rand == 1:
            self.active_panel.get_player().moneyraise(money)
            self.minbet = money
      
            print("raise")

        if rand == 2:
            self.active_panel.get_player().fold()
            self.all_fold()
            print("fold")

        
        if rand!= 2:
            self.poolArea.addToPool(self.minbet)

        self.active_panel.Refresh()
        self.next()

        
        
    def reset(self): 
        for i in self.panel:
            i.get_player().folded = False
            i.final_hand = ""
            i.get_player().action = ""
            if i.get_player().name == "You" :
                i.is_you = True
            else:
                i.is_you = False
            i.SetBackgroundColour(wx.Colour( 0, 255, 255 ))
            i.Refresh()
        self.timer.Start(1000) 
        self.minbet = 2
        self.turn = 0 
        self.count = 0
        self.initial_plr = random.randint(0,3)
        self.cur_player_num = self.initial_plr
        self.panel[self.cur_player_num].get_player().call(self.minbet)
        self.next()
        self.panel[self.cur_player_num].Refresh()

        self.continue_btt.Show(False)
        self.cardShownPanel.shown_deck = []
        self.cardShownPanel.Refresh()
        self.new_deck = deck()#create new deck
        random.shuffle(self.new_deck.deck_of_card)

      
       
        

        
    def onContinueButton(self, event):
        self.reset()
       
    def onCallButton(self, event):
        self.active_panel.get_player().call(self.minbet)
        self.active_panel.Refresh()
        print("call")
        self.poolArea.addToPool(self.minbet)
        self.timer.Start(1000)
        self.hide_button()


    def onFoldButton(self, event):
        self.panel[2].get_player().fold()
        self.hide_button()
        self.all_fold()
        self.active_panel.Refresh()
        self.timer.Start(1000)
        self.hide_button()

    def onRaiseButton(self, event):
        self.bet_area.Show()
        self.poolArea.addToPool(self.minbet)
    
    def hand_check(self):
        result = -1
        winner_score = -1
        
        for i in self.panel:
            i.is_you = True
            
            for subset in itertools.combinations(self.cardShownPanel.getCards()+i.get_player().player_hand, 5):
                hand_value = hand_check(subset)
                if result < hand_value :
                    result = hand_value

            if result == 10:
                i.final_hand = ("Royal flush")
            elif result == 9:
                i.final_hand = (" Straight flush")
            elif result == 8:
                i.final_hand = ("Four of a kind")
            elif result == 7:
                i.final_hand = ("Full house")
            elif result == 6:
                i.final_hand = ("Flush")
            elif result == 5:
                i.final_hand = (" Straight")
            elif result == 4:
                i.final_hand = ("Three of a kind")
            elif result == 3:
                i.final_hand = ("Two pair")
            elif result == 2:
                i.final_hand = (" Pair")
            elif result == 1:
                i.final_hand = ("High Card")
            if winner_score < result and not i.get_player().folded :
                winner_score = result
                winner = i
                
            
            i.Refresh() 
            result = -1 
           
        winner.SetBackgroundColour( wx.Colour( 0, 128, 255 ) )  
        winner.Refresh()
        winner.get_player().money+=self.poolArea.money
        self.poolArea.money = 0
        self.continue_btt.Show(True)
        
                

    # Paint to adjust position of what is printed to the screen    
    def OnPaint(self, e): 
        dc = wx.PaintDC(self) 
        pen = wx.Pen(wx.Colour(0,0,0)) 
        dc.SetPen(pen) 
        
        
         
            
                
     




ex = wx.App() 
app = Mywin(None,'Poker') 
ex.MainLoop()  
