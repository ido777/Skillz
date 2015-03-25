def near_pirates(game,location):
    if(type(location) is game.pirate):
        location=pirate.location
    if(type(location) is game.island):
        location=pirate.location
    on_island={"enemies:":0,"allies:":0}
    count=0
    num=4
    nlocation=location[1]-1
    for i in xrange((location[0] -3),(location[0]+4)):
        
        for j in xrange(nlocation,(loction[1]-1)+num):
            if(get_pirate_on(i,j)== ENEMY):
                on_island["enemies:"]+=1
            if(get_pirate_on(i,j)== ME):
                on_island["allies:"]+=1
        
        if(num==4 and count==0):
            count+=1
        elif (num==4 and count==1):
            count+=1
        elif (num==4 and count==2):
            count+=1
            nlocation+=1
            num-=1
        elif(num<4 and count==0):
            nlocation-=1
            num+=1
        elif(count==3):
            nlocation+=1
            num-=1
    return on_island

def nearst_island(game,islands,pirate):
    if(len(islands) != 0):
        distances=[]
        for island in islands:
            distances.append(game.distance(island.location, pirate.location))
        for island in islands:
            if(min(distances) == game.distance(island.location, pirate.location)):
                yield island

def treasure_islands(game):
    islands= [island for island in game.islands() if (island.value>1)]
    if(len(islands)>0):
        return island.sort(key= lambda island:island.value)[::-1]
    else:
        islands

def best_to_conquer(game,pirate):
#returns the best island to sail to
    treasure_islands=[]
    treasuers=[]
    islands =nears_islands(game,game.islands(),pirate)
    if(islands.owner != game.ME):
#if the islands owner isn't me - NETURAL or ENEMY
        for island in islands:
            if(len(treasure_islands(game)>0)):
#if the list of treasure islands isn't empty
                for tresure in treasure_islands(game):
                    if (island.value==tresure.value):
#if the currently checked island value matches the value
#of the currently checked treasure island - if the island is a treasure island
                        treasure_islands.append(island)
        for island in treasure_islands:
            if(island.max(key= lambda island:island.value) == island.value):
#if the currently checked island is the treasure island with the highest value
                return island
                        
        for island in islands:
            if(near_pirates(game,island.location)["enemies:"]==1):
#if there is an enemy on the island and you can take him alone
                for pirate in game.enemy_pirates():
                    if(pirate.location == island.location):
#if the enemy's pirate is standing on the island
                        return island
    
        for island in islands:
            if(near_pirates(game,island.location)["enemies:"]==0):
#if there are no enemies on the island
                return island
        
    
    else:
        for island in islands:
            if(len(treasure_islands(game)>0)):
#if the treasure list isn't empty
                for tresure in treasure_islands(game):
                    if (island.value==tresure.value):
#if the island is a treasure island
                        treasuers.append(tresure)
        for island in treasuers:
            if(near_pirates(game,island.location)["enemies:"]==1):
#if there is an enemy on the island and you can take him alone
                for pirate in game.enemy_pirates():
                    if(pirate.location == island.location):
#if an enemy is standing on the island
                        return island
        




