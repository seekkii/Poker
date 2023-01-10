from sklearn.utils import shuffle
import wx
import random

def scale_bitmap(bitmap, width, height):
    image = bitmap.ConvertToImage()
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.Bitmap(image)
    return result
#card
class card:
    def __init__(self, bitmap, type, value):
        self.image = scale_bitmap(bitmap,224/4,312/4)
        self.type = type
        self.value = value
    
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
        self.SetBackgroundColour( wx.Colour( 0, 255, 255 ) )  
        self.Centre() 
        self.SetPosition(position)
        self.active_player_area = player_area#widget that show player's details
        self.active_player = player_area.get_player()#player
        self.timer = timer
        action = "smallbind"
        
        self.sc_money = wx.SpinCtrl(self, pos=(0,0),
              size=(300,50), style=wx.SP_ARROW_KEYS, min=0, max=1500, initial=0)
        self.button = wx.Button(self, label = "confirm", pos = (20,70))
        self.button.Bind(wx.EVT_BUTTON, self.confirm)
        self.Show(False)
    
    def set_action(self,action):
        self.action = action

    def confirm(self,event):
        self.Show(False)
        if self.action == "call":
            self.active_player.call(self.sc_money.GetValue())
            print("call")
        if self.action == "raise":
            self.active_player.moneyraise(self.sc_money.GetValue())
            print("raise")
        if self.action == "fold":
            self.active_player.fold()
            print("fold")

        self.active_player_area.Refresh()
        self.timer.Start(1000)


class cardShownArea(wx.Panel):
    w = 300
    h = 100
    def __init__(self, parent, position, deck, turn):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, size = wx.Size( self.w, self.h ), style = wx.TAB_TRAVERSAL )
        self.deck = deck
        self.shown_deck = []
        self.turn = turn
        
        self.Bind(wx.EVT_PAINT, self.OnPaint) 
        self.Centre() 
        self.SetPosition(position)
        self.Show(True)

    def OnPaint(self, e): 
        dc = wx.PaintDC(self) 
        pen = wx.Pen(wx.Colour(0,0,0)) 
        dc.SetPen(pen) 
        
        #draw card owned to screen
        if self.turn == 0:
            return
        for i in range(len(self.shown_deck)):
            card_indx = random.randint(0, len(self.deck)-1)
            self.shown_deck.append(self.deck[card_indx])
            dc.DrawBitmap(self.deck[card_indx].get_card_bitmap(),i*50,0)
            self.deck.remove(self.deck[card_indx])
            
        
    
  


#player
class player:
    def __init__(self, name):
        self.name = name
        self.money = 1500
        self.chip_update()

        
        self.player_hand = []
       
    
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

    def call(self, money):
        self.money = self.money - money
        self.chip_update()
        return 

    def moneyraise(self,money):
        self.money = self.money - money
        self.chip_update()
     
    def small_bind(self,money):
        self.money = self.money - 1
    
    def fold(self):
        pass
        

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
    def __init__(self, parent, player_,position,deck):
        return

class PlayerArea(wx.Panel):
    w = 210
    h = 160
    def __init__(self, parent, player_,position,deck):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, size = wx.Size( self.w, self.h ), style = wx.TAB_TRAVERSAL )
        self.deck = deck
        player_.add_card_from(self.deck)
        player_.add_card_from(self.deck)
        self.p1 = player_
        self.name_label = scale_bitmap(wx.Bitmap("ui\\name_label.png"),100,30)#name
        self.money_label = scale_bitmap(wx.Bitmap("ui\\money_label.png"),80,40)#money


        self.Bind(wx.EVT_PAINT, self.OnPaint) 
        self.Centre() 
        self.SetPosition(position)
        self.Show(True)

   
    def get_player(self):
        return self.p1  
       

    def OnPaint(self, e): 
        dc = wx.PaintDC(self) 
        pen = wx.Pen(wx.Colour(0,0,0)) 
        dc.SetPen(pen) 
        
        #draw card owned to screen
        for i in range(len(self.p1.cur_hand())):
            dc.DrawBitmap(self.p1.cur_hand()[i].get_card_bitmap(),i*50,0)
        
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
            
            dc.DrawBitmap(self.name_label,0,int(self.h/2)+30)
            dc.DrawBitmap(self.money_label,11,int(self.h/2)+45)
         
            dc.DrawText(self.p1.name,40,70)
            
            dc.DrawText(str(self.p1.money),40,100)

    
    
        


    
    
class player_area_style_2(PlayerArea):
    def __init__(self, parent, player_,position,deck):
        super().__init__(parent, player_,position,deck)
        self.back_card = scale_bitmap(wx.Bitmap("ui\\back_card.jpg"),224/4,312/4)#name
        

    def OnPaint(self, e): 
        dc = wx.PaintDC(self) 
        pen = wx.Pen(wx.Colour(0,0,0)) 
        dc.SetPen(pen) 
        
        #draw card owned to screen
        for i in range(len(self.p1.cur_hand())):
            dc.DrawBitmap(self.back_card,int(self.w-224/4-i*50),0)
        
        #draw chip to screen
        for i in range(len(self.p1.chiplist)):
            if not len(self.p1.chiplist[i]):
                pass
            if i == 0:
               
                for j in range(len(self.p1.chiplist[i])):
                    dc.DrawBitmap(self.p1.chiplist[i][0].chip_image(),0+j,int(self.h/2)+30)

            if i == 1:
                for j in range(len(self.p1.chiplist[i])):
                    dc.DrawBitmap(self.p1.chiplist[i][0].chip_image(),30+j,int(self.h/2)+30)

            if i == 2:
                for j in range(len(self.p1.chiplist[i])):
                    dc.DrawBitmap(self.p1.chiplist[i][0].chip_image(),60+j,int(self.h/2)+30)
            
            if i == 3:
                for j in range(len(self.p1.chiplist[i])):
                    dc.DrawBitmap(self.p1.chiplist[i][0].chip_image(),0+j,int(self.h/2)+55)
            
            if i == 4:
                for j in range(len(self.p1.chiplist[i])):
                    dc.DrawBitmap(self.p1.chiplist[i][0].chip_image(),30+j,int(self.h/2)+55)

            if i == 5:
                for j in range(len(self.p1.chiplist[i])):
                    dc.DrawBitmap(self.p1.chiplist[i][0].chip_image(),60+j,int(self.h/2)+55)

            if i == 6:
                for j in range(len(self.p1.chiplist[i])):
                    dc.DrawBitmap(self.p1.chiplist[i][0].chip_image(),0+j,int(self.h/2)+5)

            if i == 7:
                for j in range(len(self.p1.chiplist[i])):
                    dc.DrawBitmap(self.p1.chiplist[i][0].chip_image(),30+j,int(self.h/2)+5)
            
            dc.DrawBitmap(self.name_label,100,int(self.h/2)+30)
            dc.DrawBitmap(self.money_label,89,int(self.h/2)+45)
         
            dc.DrawText(self.p1.name,40,70)
            dc.DrawText(str(self.p1.money),40,100)


def hand_check(hand):
    handVal = []#list of card value in player hadn
    cardFre = []#frequency of a card in the hand calculate using count()
    same_type = True

    for i in range (5):
        handVal.append(hand[i].get_value())
        if (i>0 and hand[i].get_type()!=hand[i-1].get_type()):
            same_type = False
    
    for i in range (5):
        cardFre.append(handVal.count(handVal[i]))


    if (sorted(handVal) == list(range(min(handVal), max(handVal)+1))) and same_type and handVal[0] == 10 :
        print("Royal flush")
    elif (sorted(handVal) == list(range(min(handVal), max(handVal)+1))) and same_type :
        print("Straight flush")

    if (sorted(handVal) == list(range(min(handVal), max(handVal)+1))) and not same_type :
        print("Straight")

    if (sorted(handVal) != list(range(min(handVal), max(handVal)+1))) and same_type :
        print("Flush")
    
    if max(cardFre) == 4:
        print("Four of a kind")

    if max(cardFre) == 3 and sorted(set(cardFre))[-2] == 2:
        print("Full house")

    if max(cardFre) == 3 and sorted(set(cardFre))[-2] == 1:
        print("Three of a kind")

    if max(cardFre) == 2 and cardFre.count(2) == 4:
          print("Two pair")
    
    if max(cardFre) == 2 and cardFre.count(2) == 2:
          print("Pair")

    if max(cardFre) == 1:
        print("High Card")

    print(handVal)
    print(cardFre)

    
     





class Mywin(wx.Frame): 
          
    def __init__(self, parent, title): 
        super(Mywin, self).__init__(parent, title = title,size = (900,600))  
        self.InitUI() 
         
    def InitUI(self): 
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )        
        self.Bind(wx.EVT_PAINT, self.OnPaint) 
        self.Centre() 
        self.Bind(wx.EVT_LEFT_UP, self.onClick)
        self.init_player_and_deck()

        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.player_update, self.timer)
        self.timer.Start(1000)


        fold_button = wx.Button(self, label = "fold", pos = (20,70))
        fold_button.Bind(wx.EVT_BUTTON, self.onFoldButton)
        bet_button = wx.Button(self, label = "call", pos = (20,100))
        bet_button.Bind(wx.EVT_BUTTON, self.onCallButton)
        raise_button = wx.Button(self, label = "raise", pos = (20,130))
        raise_button.Bind(wx.EVT_BUTTON, self.onRaiseButton)

        self.bet_area = BetArea(self, (self.Size.x*1/3,self.Size.y*1/3), self.panel[3], self.timer)
        self.cardShownPanel = cardShownArea(self,(self.Size.x*1/3,self.Size.y*1/3) , self.new_deck.deck_of_card,self.cur_player_num)
        
       


       

        self.Show(True)

    def init_player_and_deck(self):
        self.new_deck = deck()#create new deck
        random.shuffle(self.new_deck.deck_of_card)

        p1_panel = PlayerArea(self,player("Bob"), (200,0), self.new_deck.deck_of_card)
        p2_panel = player_area_style_2(self,player("Alice"),(0,300),self.new_deck.deck_of_card)
        p3_panel = player_area_style_2(self,player("You"),(600,300),self.new_deck.deck_of_card)
        p4_panel = player_area_style_2(self,player("Your mom"),(600,0), self.new_deck.deck_of_card)

        self.panel = [p1_panel,p2_panel,p3_panel,p4_panel]
        self.cur_player_num = 3
        self.active_panel = self.panel[self.cur_player_num]
        
        self.action =""
        
       
       
    def next(self):
        self.cur_player_num = self.cur_player_num + 1
        if self.cur_player_num>3:
            self.cur_player_num = 0

        

    def player_update(self,event):
        print(self.cur_player_num)
        self.active_panel = self.panel[self.cur_player_num]
        if self.active_panel.get_player().name == "You":
            print("your turn")
            self.next()
            self.timer.Stop()  
            return
        
       
        rand = random.randint(0, 2)
        money = random.randint(0, 1500)
        print(self.active_panel.get_player().name)
        if rand == 0:
            self.active_panel.get_player().call(money)
            print("call")
        
        if rand == 1:
            self.active_panel.get_player().moneyraise(money)
            print("raise")

        if rand == 2:
            self.active_panel.get_player().fold()
            print("fold")

        
       
        self.active_panel.Refresh()
        self.next()

        

       
    def onCallButton(self, event):
        self.bet_area.Show()
        self.bet_area.set_action("call")

    def onFoldButton(self, event):
        self.bet_area.Show()
        self.bet_area.set_action("fold")

    def onRaiseButton(self, event):
        self.bet_area.Show()
        self.bet_area.set_action("raise")


    def onClick(self, event):
        hand=[]
        for i in range(5):
            link = "card\\" + str(i+8)+"hearts.png"
            image = wx.Bitmap(link)
            hand.append (card(image,"hearts",i+8))
        
        hand[0].set_value(3)
        hand[0].set_type("dia")
        hand[1].set_value(11)
        hand[1].set_type("clubs")
        hand[2].set_value(8)
        hand[2].set_type("spades")
        hand[3].set_value(4)
        hand[3].set_type("hearts")
        hand[4].set_value(2)
        hand[4].set_type("spades")
        
      
        hand_check(hand)
        return
                

    # Paint to adjust position of what is printed to the screen    
    def OnPaint(self, e): 
        dc = wx.PaintDC(self) 
        pen = wx.Pen(wx.Colour(0,0,0)) 
        dc.SetPen(pen) 
        
         
            
                
     




ex = wx.App() 
app = Mywin(None,'Poker') 
ex.MainLoop()  
