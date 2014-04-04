import os
import player
import play
import team
import rank

teamGroup = []


def main():
    run = 0.0
    passNum = 0.0
    eP = 0
    conversions = 0
    penalties = 0
    sacks = 0
    kicks = 0
    punts = 0
    for i in range(1):
        fileName="200"+ str(i+2) +"plays"
        readFromFile(fileName)
    for team in teamGroup:
        for play in team.offensivePlays:
            play.definePlay()
            #if play.playType=="pass":
             #   print play.secondTouch
            if play.playType == "pass":
                passNum += 1
            if play.playType=="kick":
                kicks+=1
            if play.playType=="punt":
                punts+=1
            if play.playType == "extra point":
                eP += 1
            if play.playType == "run":
                run += 1
            if play.playType == "penalty":
                penalties += 1
            if play.playType == "sack":
                sacks += 1
            if play.interception:
                conversions += 1
        team.addPlayers()
        team.check()#cackulates the fantasy scores for each player

    ratio = passNum / (passNum + run)
    print ratio
    print "run: " + str(run)
    print "pass: " + str(passNum)
    print "extra points: " + str(eP)
    print "sacks: " + str(sacks)
    print "penalties: " + str(penalties)
    print "conversions: " + str(conversions)
    print "punts: " + str(punts)
    print "kicks: " + str(kicks)


    rank.rankPlayers(teamGroup)
    rank.percentImportance(teamGroup[0])
    rank.teamPointRanks(teamGroup)    

def readFromFile(readFile):
    if os.path.isfile(readFile):
        f = open(readFile, 'r')
        lines = f.readlines()
        del lines[0] #top line is header
        for line in lines:
            line=line.lower()
            while not -1 == line.find(",,"):
                line = line.replace(",,", ",0,") #gets rid of blanks
            line = line.replace(",**,", ",0,") #get rid of missings
            playerStats = line.split(',')
            numList = [1, 2, 3, 6, 7, 8, 10, 11, 12] #stats that are numbers
            for x in range(len(playerStats)):
                if x in numList:
                    #print playerStats
                    playerStats[x] = float(playerStats[x])
            #makes the numbered stats numbers
           
            #uploads a play

           #occasionaly there will be no offensive team, this adds the offensive team from the previous play, seems to be pretty accurate.
            if  "0" in playerStats[4]:
                playerStats[4]=tempPlay.offense

            tempPlay = play.play(*playerStats)
            # adds all the teams
            add = True
            for y in teamGroup:
                if y.name == tempPlay.offense:
                    y.addPlay(tempPlay, True)#adds play if team is added
                    add = False
                    break
            if add:
                tempTeam = team.team(tempPlay.offense)
                tempTeam.addPlay(tempPlay, True) #adds if team needed adding
                teamGroup.append(tempTeam) #addsteam


            #same for Defense below
            add = True
            for y in teamGroup:
                if y.name == tempPlay.defense:
                    y.addPlay(tempPlay, False)
                    add = False
                    break
            if add:
                tempTeam = team.team(tempPlay.defense)
                tempTeam.addPlay(tempPlay, False)
                teamGroup.append(tempTeam)
            # add plays in


if __name__ == "__main__":
    main()
