import random 

class Game: 
    
    def __init__(self, p): 
        self.players = []
        self.playerValues = []
        self.bidPrice = 0
        self.gameOver = False


        for x in range(p):
            #PRICE GENERATION FUNCTION -- KEY
    
            rand = 10 + random.randint(0, 40)  
            self.playerValues.append(rand)
            self.players.append(Player(rand, len(self.players)))
            print("Player", len(self.players), "value:", rand)
            

    def play(self): 
        self.bidPrice = 0
        highest_bidder = self.players[0]

        while not self.gameOver:
            winner = self.players[0]
            players_to_remove = []
            bid_increased = False

            for x in self.players: 
                if (len(self.players) == 1): 
                    winner = self.players[0].playerNumber
                    self.gameOver = True
                    break

                new_bid = x.bidCheck(self.bidPrice)
                if new_bid == self.bidPrice or not x.inGame:
                    print("Player", x.playerNumber, "is out.")
                    players_to_remove.append(x)
                elif not bid_increased:
                    # Only increase the bid once per loop iteration
                    self.bidPrice = new_bid
                    bid_increased = True



            # Remove players after the loop completes its iteration
            for p in players_to_remove:
                self.players.remove(p)

            if len(self.players) == 0:
                self.gameOver = True

        print("Winner: ", winner, "at a price of ", self.bidPrice)


            

class Player(Game): 
    def __init__(self, v, num): 
        self.playerNumber = num+1
        self.itemValue = v  
        self.bid = 0
        self.inGame = True

    def bidCheck(self, bp): 
        if bp < self.itemValue and bp + 1 < self.itemValue: 
            return bp + 1
        else: 
            self.inGame = False
            return bp  # return the same bid price if not willing to increase



def run(): 
    g = Game(2)
    g.play() 


run()