import re

class play():

    def __init__(self, gameID, qtr, minute, sec, offense, defense, down, togo,
                 yardLine, playString, offscore, defscore, season):

        self.gameID = gameID
        self.qtr = qtr
        self.minute = minute
        self.sec = sec
        self.offense = offense
        self.defense = defense
        self.down = down
        self.togo = togo
        self.yardsGot = 0
        self.yardLine = yardLine
        self.playString = playString
        self.offscore = offscore
        self.defscore = defscore
        self.season = season
        self.conversion = False
        self.fumble = False
        self.interception = False
        self.Penalty = False
        self.incomplete = False
        self.touchdown = False
        self.playType = "none"
        self.firstTouch = "noone"
        self.secondTouch = "noone"
        self.tacklers = []
        self.safety=False
        #self.analysis()

#analysis will eventually be dleeted, it's used to know roughly how many plays are of each
#type, deleteing the relevant line will show if your new define call captures all the
#running plays you want

    def analysis(self):
        if not -1 == self.playString.find("PENALTY"):
            self.Penalty = True
            if not -1 == self.playString.find("No Play"):
                self.playType = "no play"
        elif not -1 == self.playString.find("for"):
            self.playType = "run"
         # this play is usless 2 minute warning stuff
        elif self.playString == " ":
            self.playType = "skip"
        elif not -1 == self.playString.find("FUMBLE"):
            self.playType = "snapfumble"
        # same
        if not -1 == self.playString.find("FUMBLE"):
            self.fumble = True


#this defines the play
    def definePlay(self):
        tempPlay = []
        tempPlay = self.playString.split()

        #deals with extraneous information
        for x in range(len(tempPlay) - 1):

            if x >= len(tempPlay) - 1:
                break
            if tempPlay[x] == "(shotgun)":
                tempPlay.remove(tempPlay[x])
            if "(punt" in tempPlay[x] or "(field" in tempPlay[x] or \
               "(pass" in tempPlay[x] or "(run" in tempPlay[x] or \
               "(kick" in tempPlay[x]: 
                #one day this will cause a problem ,its for "punt formation being included
                tempPlay.remove(tempPlay[x])
                tempPlay.remove(tempPlay[x])
            if "formation" in tempPlay[x]:
                tempPlay.remove(tempPlay[x]) 


#fixes spaces after intial problem
            if "." == tempPlay[x][-1] and len(tempPlay) > x and len(tempPlay[x]) == 2 and re.match("[A-Za-z]",tempPlay[x]):
                tempPlay[x] += tempPlay[x+1]
                tempPlay.remove(tempPlay[x+1])

#deals with injury timeouts under 2 minutes
            if "by" in tempPlay[x] and "to" in tempPlay[x-1] and "injury" in tempPlay[x-2]:
                tempPlay.remove(tempPlay[x])
                tempPlay.remove(tempPlay[x])
                tempPlay.remove(tempPlay[x-1])
                tempPlay.remove(tempPlay[x-2])

        tempPlay = self.stripDefense(tempPlay)
        #gets any defenders as well as dealing with name problems like a randle el
        # does not deal with problems of author sometimes putting spaces after initial
        #so t.bradyc an be t.brady or t. brady causing two different plays to appear
        #right now i deal with that inside each function since the author also uses
        # periods ot signify ends of sentences
        # it relaly should be dealt with at this level, if you wanna fix that thats prb.
        # smart and time efficent



        if len(tempPlay) > 1:
            if tempPlay[1] == "kicks":
                self.isKick(tempPlay)
            elif len(tempPlay) > 2:
                if "." == tempPlay[1][-1]:  # fixes some players names
                    tempPlay[1] += tempPlay[2]
                    tempPlay.remove(tempPlay[2])
                if "pass" in tempPlay[2]:
                    self.isPass(tempPlay)
                elif "punt" in tempPlay[2]:
                    self.isPunt(tempPlay)
                elif "extra" in tempPlay[1]:
                    self.isEP(tempPlay)
                elif "sack" in tempPlay[2]:
                    self.isSack(tempPlay)
                elif "kneel" in tempPlay[2]:
                    self.isKneel(tempPlay) 
                elif "two" in  tempPlay[0]:
                    self.isConversion(tempPlay)
                elif "left" ==tempPlay[2] or "right"== tempPlay[2]:
                    self.isRun(tempPlay)
                elif len(tempPlay)>4 and"field" in tempPlay[4] and "goal" in tempPlay[5]:
                    self.isFieldGoal(tempPlay)
                elif len(tempPlay)>4 and "middle"== tempPlay[4]:
                    self.isMidRun(tempPlay)
                elif "to"==tempPlay[2]:
                    self.isUnnamedRun(tempPlay)
                #elif not "penalty" in self.playString:
                 #   print tempPlay
                if "fumble" in self.playString:
                    self.fumble=True
                if re.match("[A-Za-z]",str(self.yardsGot)):
                    print self.playString
                    print tempPlay
                    print "this is a problem play"
                else:
                    self.yardsGot = int(self.yardsGot)

    def isUnnamedRun(self,play):
         self.playType="run"
         self.firstTouch=play[1]
         if "touchdown" in self.playString:
             self.touchdown=True
         elif "50" in play[3]:
             self.yardsGot=(play[5])
         else:
             self.yardsGot=(play[6])
         if "no" == self.yardsGot:
             self.yardsGot=0

    def isMidRun(self,play):
         self.playType="run"
         self.firstTouch=play[1]
         if "ob" in play[6]:
             play.remove(play[6])
             play.remove(play[5])
         if "safety" in self.playString:
             self.yardsGot=-self.yardLine
             self.safety=True

         elif "touchdown" in self.playString:
             if re.match("[A-Za-z]",play[6]):
                  #TD's can be disputed and can screw with this        
                  self.yardsGot=int(self.yardLine)
             else:
                  self.yardsGot=play[6]
             self.touchdown=True 
         elif "50" in play[6]:
             self.yardsGot=play[8]
         else:
             self.yardsGot=play[9]
         if "no"== self.yardsGot:
             self.yardsGot=0

#['2:58', 'c.dillon', 'right', 'guard', 'tackled', 'in', 'end', 'zone', 'for', '-3', 'yards', 'safety']

    def isRun(self,play):
         self.playType="run"       
         self.firstTouch=play[1]

#sometimes helmets come off
         if "dead" in play[4] and "ball" in play[5] and "declared" in play[6] :
             play.remove(play[6])
             play.remove(play[5])
             play.remove(play[4])
               

#sometimes players go out of bounds 
         if "ob" in play[5]:
             play.remove(play[5])
             play.remove(play[4])
#or worse are tackled in the end zone!
         if "safety" in self.playString:
             self.yardsGot=-self.yardLine
             self.safety=True
#however sometimes they score
         elif "touchdown" in self.playString:
             if re.match("[A-Za-z]",play[5]):#TD's can be disputed and can screw with this
                  self.yardsGot=int(self.yardLine)
             else:
                  self.yardsGot=play[5]
             self.touchdown=True               

         elif "50" in play[5]:
             self.yardsGot=play[7]
         else:
             self.yardsGot=play[8]
         if "no" == self.yardsGot:
             self.yardsGot=0
 
    def isConversion(self,play):
         self.playType="2PT-Conversion"
         self.firstTouch=play[3]
         if "pass" in play[4]:
             self.playType+="-pass"
             self.secondTouch=play[6]
             if "incomplete" in self.secondTouch:
                 self.secondTouch="noone"
         else:
             self.playType+="-run"
         if "fails" in self.playString:
             self.incomplete=True


    def isKneel(self,play):
         self.playType="kneel"
         self.firstTouch=play[1]
         if "50" in play[4]:
             self.yardsGot=play[6]
         else:
             self.yardsGot=play[7]
         if  "dead" in play[3]:                #weird play call sometimes
             self.yardsGot=play[10]
         if "no" in self.yardsGot:
             self.yardsGot=0


    def isSack(self, play):
         self.playType="sack"
         self.firstTouch=play[1]
         if "50" in play[4]:
             self.yardsGot=play[6]
         else:
             self.yardsGot=play[7]
         if "for" in self.yardsGot:
             self.yardsGot=play[8]

    def isEP(self,play):
         self.playType="extra point"
         self.firstTouch=play[1]
         if not "good" in play[4]:
            self.incomplete=True


    def isFieldGoal(self,play):
         self.playType="field goal"
         self.firstTouch=play[1]
         self.yardsGot=play[2]
         if "no" in play[7] or "blocked" in play[7]:
            self.incomplete=True

    def isPunt(self,play):
         self.playType="punt"
         self.firstTouch=play[1]
         self.yardsGot=play[3]
         if "is" in self.yardsGot:
             self.yardsGot=0
             self.fumble=True 
                                    


    #gets info from all kicking plays, very simple since theres a format for it
    def isKick(self, play):
        self.firstTouch = play[0]
        self.playType = "kick"
        self.yardsGot = play[2]
        self.yardLine = play[7]
        if "onside" in self.yardsGot:
           self.yardsGot=play[3]
           self.yardLine = play[8]


    #gets info from passing plays, shit show.
    def isPass(self, play):

        if play[3] == "incomplete" or play[3] == "incomplete.":
            play.remove(play[3])
            self.incomplete = True
        self.firstTouch = play[1]
        self.playType = "pass"

        # quarterback done, one time terrell owen threw a pass

        if len(play) < 4 and self.incomplete:
            return

        # incompletes to no one finished

        if "spike" in play[3]:
            return
        # spikes taken care of, not incomplete cuz don't even want it to count

        if "to" == play[3]:
            #fixes players names
            self.secondTouch = play[4]
            # gets caught passes

        if len(play) < 6:
            if not "spike" in self.playString:
                self.incomplete = True
            return
        # takes care of more incompletes

        if len(play) < 9 or self.incomplete:
            self.incomplete = True  # tested, all incomplete at this point
            return
        if play[7] == "for":
            if play[8] == "no":
                return  # no gain play accounted for
            else:
                self.yardsGot = int(play[8])
                return
        # above is for 50 yard line

        if play[8] == "for":
            if play[9] == "no":
                return  # no gain play accounted for
            else:
                self.yardsGot = int(play[9])
                return
        if play[6] == "ob":
            if "50" in play[8]:
                self.yardsGot = int(play[10])
            else:
                if play[11] == "no":
                    return
                self.yardsGot = int(play[11])

            return
        if "touchdown" in play[8]:
            self.yardsGot = int(play[6])
            self.touchdown = True
            return

        if "intercepted" in play[6]:
            self.secondTouch = play[8]  # second touch given to defense
            self.interception = True
            return
        if "intercepted" in play[3]:
            self.secondTouch = play[5]  # second touch given to defense
            self.interception = True
            return

    def stripDefense(self, play):
        tempPlayer = ""
        end = 0
        beg = 0

        for x in range(len(play)):
            if x > len(play) - 1:
                break

            if play[x] == "el" or play[x] == "jr" or play[x] == "el." or play[x] == "jr.":
            # a randle el that mother fucker plsu jrs
                play[x - 1] += play[x]
                play.remove(play[x])

            if x > len(play) - 1:
                break

            if play[x] == "davis" or play[x] == "jones":
                if (play[x - 1] == "andre'" or play[x - 1] == "daryl"):
            # more name bullshit
                    play[x - 1] += play[x]
                    play.remove(play[x])

            if x > len(play) - 1:
                break

            play[x] = play[x].replace("yards)", "yards")
            play[x] = play[x].replace("(1", "1")
            play[x] = play[x].replace("(5", "5")
            # deals with weird penalties in brackets

            if ")" in play[x]:
                play[x] = play[x].replace(")", "")
                end = x
            if "(" in play[x]:
                play[x] = play[x].replace("(", "")
                beg = x
            if ":" in play[x]:
                beg = 0
                end = 0
                x += 1

        while end >= beg and not end == 0:
            tempPlayer += play[beg]
            del play[beg]
            end -= 1
        self.tacklers.append(tempPlayer)
        return play
