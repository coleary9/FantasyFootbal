#these functions just rank different position players based on fantasy points
import team
class ranks:
  QBs=[]
  WRs=[]
  RBs=[]

#orders players by their fantasy scores, is recursive merge sort.
def Order(playerArray):
    if (len(playerArray))<2:
        return playerArray
    middle= (len(playerArray))/2
    front=Order(playerArray[:middle])
    back=Order(playerArray[middle:])    
    result=[]
    while len(front) >0 and len(back)>0:
        if front[0].score>back[0].score:
           result.append(front.pop(0))
        else:
           result.append(back.pop(0))
    if len(back)>0:
        result.extend(Order(back))
    else:
        result.extend(Order(front))
    return result

def rankPlayers(teamGroup):
    rank=ranks()
    for teams in teamGroup:
        for player in teams.offensivePlayers:
            if player.position=="QB":
                ranks.QBs.append(player)
            if player.position=="WR":
                ranks.WRs.append(player)
            if player.position=="RB":
                ranks.RBs.append(player)
    ranks.QBs=Order(ranks.QBs)
    ranks.WRs=Order(ranks.WRs)
    ranks.RBs=Order(ranks.RBs)

    #print "QBS"
    #print ""
    for player in ranks.QBs:
        player.positionRank=ranks.QBs.index(player)+1
        #print player.toString()
    #print "WRS"
    #print ""
    for player in ranks.WRs:
        player.positionRank=ranks.WRs.index(player)+1
        #print player.toString()
    #print "RBS"
    #print ""
    for player in ranks.RBs:
        player.positionRank=ranks.RBs.index(player)+1
        #print player.toString()

def teamPointRanks(teamGroup):
    teamGroup=Order(teamGroup)
    total =0
    for team in teamGroup:
        print team.name + ": " + str(team.score)
        total+=team.score
    print "average: " + str(total/len(teamGroup))

def percentImportance(team):
    team.offensivePlayers=Order(team.offensivePlayers)
    for player in team.offensivePlayers:
        return
        print player.toString()
        #set to ratio due to need for float from int division stuff
        ratio= float(player.score)/float((team.score))
        print ratio
