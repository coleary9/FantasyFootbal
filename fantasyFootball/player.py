
class player():

    def __init__(self, name):
        self.name = name
        self.team= " "
        self.position=""
        self.touchdowns = 0 #doesn't include thrown
        self.thrownTouchdowns=0
        self.rushYards = 0
        self.catchYards= 0
        self.throwYards = 0
        self.plays=[]
        self.score=0
        self.positionRank=0

#these three variables count how many plays a player is each position
#assumes larger is the correct position
        self.QBCount=0
        self.WRCount=0
        self.RBCount=0

    def scoreTotal(self):
        self.score= self.touchdowns*6+self.thrownTouchdowns*4+(self.rushYards+self.catchYards)/10+self.throwYards/25
        return self.score

    def addPlay(self,play):
        self.plays.append(play)

        if self.team==" ":
            if self.name in play.firstTouch or self.name in play.secondTouch:
                 self.team=play.offense
            else:
                 self.team=play.defense
        if "run" in play.playType:
            if self.name in play.firstTouch:
               self.RBCount+=1
               self.rushYards+=play.yardsGot
        if "pass" in play.playType:
            if self.name in play.firstTouch:
               self.QBCount+=1
               self.throwYards+=play.yardsGot
               if play.touchdown:
                   self.touchdowns-=1
                   self.thrownTouchdowns+=1 
            if self.name in play.secondTouch:
               self.WRCount+=1
               self.catchYards+=play.yardsGot
        if play.touchdown:
            self.touchdowns+=1
        if self.QBCount>self.WRCount and self.QBCount>self.RBCount:
             self.position="QB"
        elif self.WRCount>self.QBCount and self.WRCount>self.RBCount:
             self.position="WR"
        else:
             self.position="RB"

    def toString(self):
        return self.name + ": " +  self.team + ": "+ self.position + ": "\
                + "points:" + str(self.score) + ": total Touchdowns:"\
                 + str(self.touchdowns+self.thrownTouchdowns)+ ": prk:" +str(self.positionRank)
