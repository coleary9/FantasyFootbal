import player

class team():
    
    def __init__(self, name):
          self.name=name
          self.offensivePlays=[]
          self.defensivePlays=[]
          self.offensivePlayers=[]
          self.score=0 #total team fantasy points

    def addPlay(self,play,onOff):
          if onOff:
             self.offensivePlays.append(play)
          else:
             self.defensivePlays.append(play)
   
   #adds players for you, adds the plays to you away from the team
    def addPlayers(self):
         for play in self.offensivePlays:
             if play.playType=="run":
                 add=True
                 for guys in self.offensivePlayers:
                     if guys.name in play.firstTouch:
                        guys.addPlay(play)
                        add=False
                        break
                 if add:
                     name=play.firstTouch
                     tempPlayer=player.player(name)
                     tempPlayer.addPlay(play)
                     self.offensivePlayers.append(tempPlayer)
#adds both the first and second touch players plays
             if play.playType=="pass":
                 add=True
                 for guys in self.offensivePlayers:
                     if guys.name in play.firstTouch:
                        guys.addPlay(play)
                        add=False
                        break
                 if add:
                     name=play.firstTouch
                     tempPlayer=player.player(name)
                     tempPlayer.addPlay(play)
                     self.offensivePlayers.append(tempPlayer)
       #recievers
                 add=True
                 for guys in self.offensivePlayers:
                     if guys.name in play.secondTouch:
                        guys.addPlay(play)
                        add=False
                        break
                 if add:
                     name=play.secondTouch
                     tempPlayer=player.player(name)
                     tempPlayer.addPlay(play)
                     self.offensivePlayers.append(tempPlayer)

    def check(self):
         for player in self.offensivePlayers:
            self.score+=player.scoreTotal()    
