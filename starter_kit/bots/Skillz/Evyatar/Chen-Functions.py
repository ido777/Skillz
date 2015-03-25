def best_to_conquer(game):
    nearst_island(game,islands,pirate)




def safe_distance(game,location):
    if(type(location) is game.pirate):
        location=pirate.location
    on_island={"enemies:":0,"allies:":0}
    count=0
    num=3
    nlocation=location[1]-1
    for i in xrange((location[0] -4),(location[0]+5)):
        
        for j in xrange(nlocation,(location[1]-1)+num):
            if(game.get_pirate_on(i,j)== game.ENEMY):
                on_island["enemies:"]+=1
            if(game.get_pirate_on(i,j)== game.ME):
                on_island["allies:"]+=1
        
        if(num==6 and count==0):
            count+=1
        elif (num==6 and count==1):
            count+=1
        elif (num==6 and count==2):
            count+=1
            nlocation+=1
            num-=1
        elif(num<6 and count==0):
            nlocation-=1
            num+=1
        elif(count==3):
            nlocation+=1
            num-=1
    return on_island
def near_pirates(game,location):
    if(type(location) is game.pirate):
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

def safe_direction(game,pirate,location):
    directions= game.get_directions(pirate,location)
    for direction in directions:
        if(direction == 'n'):
            if(safe_distance(game,(pirate.location[0]-1,pirate.location[1]))["enemies:"]==0):
                return 'n'
        elif(direction == 'e'):
            if(safe_distance(game,(pirate.location[0],pirate.location[1]+1))["enemies:"]==0):
                return 'e'
        elif(direction == 's'):
            if(safe_distance(game,(pirate.location[0]+1,pirate.location[1]))["enemies:"]==0):
                return 's'
        elif(direction == 'w'):
            if(safe_distance(game,(pirate.location[0],pirate.location[1]-1))["enemies:"]==0):
                return 'w'
    return '-'

def nearst_pirate(game,pirates,island):
    if(len(pirates) != 0):
        
        distances=[]
        for pirate in pirates:
            distances.append(game.distance(pirate.location, island.location))
        for Pirate in pirates:
            if(min(distances) == game.distance(pirate.location, island.location)):
                return Pirate

def nearst_island(game,islands,pirate):
    if(len(islands) != 0):
        
        distances=[]
        for island in islands:
            distances.append(game.distance(island.location, pirate.location))
        for island in islands:
            if(min(distances) == game.distance(island.location, pirate.location)):
                return island






















