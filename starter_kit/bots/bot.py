import math

def near_pirates(game,location):
    on_island={"enemies:":0,"allies:":0}
    count=0
    num=4
    nlocation=location[1]-1
    for i in xrange((location[0] -3),(location[0]+4)):
        for j in xrange(nlocation,(location[1]-1)+num):
            if(game.get_pirate_on((i,j)) is not None):
                if(game.get_pirate_on((i,j)).owner == game.ENEMY):
                    on_island["enemies:"]+=1
                if(game.get_pirate_on((i,j)).owner == game.ME):
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
def closest_locations(loc, locationsList):
    locations = []
    for location in locationsList:
        locations.append([location, distance(loc, location)])
    return [item[0] for item in sorted(locations, key = lambda item: item[1])]

def closest_islands(loc, islandsList):
    islands = []
    for island in islandsList:
        islands.append([island, distance(loc, island.location)])
    return [item[0] for item in sorted(islands, key = lambda item: item[1])]

def closest_pirates(loc, group):
    pirates = []
    for pirate in group:
        pirates.append([pirate, distance(loc, pirate.location)])
    return [item[0] for item in sorted(pirates, key = lambda item: item[1])]

def closest_pirate(loc, group):
    return closest_pirates(loc, group)[0]

def find_target_islands():
    toConquer = int(len(game.islands()) / 2) + 1
    return closest_islands(game.my_pirates()[0].initial_loc, game.islands())[:toConquer]

def find_order(pirates, islands):
    order = [0 for i in xrange(len(islands))]
    index = 0
    for pirate in pirates:
        order[index] += 1
        index += 1
        if index >= len(order):
            index = 0
    return order

def assign_target(pirates):
    for pirate in pirates:
        pirate.target = None
        pirate.mode = ATTACKING
        pirate.lastDirection = '-'
        pirate.isArranged = False
        pirate.prevTarget = None

def update_pirates_list(pirates):
    lst = []
    for pirate in pirates:
        p = game.get_my_pirate(pirate.id)
        
        if is_pirate(pirate.target):
            if pirate.target in game.all_my_pirates():
                p.target = game.get_my_pirate(pirate.target.id)
            else:
                p.target = game.get_enemy_pirate(pirate.target.id)
        elif is_group(pirate.target):
            p.target = []
            for item in pirate.target:
                if item in game.all_my_pirates():
                    p.target.append(game.get_my_pirate(item.id))
                else:
                    p.target.append(game.get_enemy_pirate(item.id))
        else:
            p.target = pirate.target

        if is_pirate(pirate.prevTarget):
            p.prevTarget = game.get_my_pirate(pirate.prevTarget.id)
        elif is_group(pirate.prevTarget):
            p.prevTarget = []
            for item in pirate.prevTarget:
                if item in game.all_my_pirates():
                    p.prevTarget.append(game.get_my_pirate(item.id))
                else:
                    p.prevTarget.append(game.get_enemy_pirate(item.id))
        else:
            p.prevTarget = pirate.prevTarget
            
        p.mode = pirate.mode
        p.lastDirection = pirate.lastDirection
        p.isArranged = pirate.isArranged
        lst.append(p)
    return lst

def find_groups(p):
    pirates = list(p)
    groups = []

    def recursive(pirates, group, currentPirate):
        group.append(currentPirate)
        pirates.remove(currentPirate)
        for pirate in pirates:
            if game.in_range(currentPirate, pirate) and not pirate in group:
                recursive(pirates, group, pirate)

    while len(pirates) > 0:
        groups.append([])
        recursive(pirates, groups[-1], pirates[0])

    return groups

def group_location(group):
    x = 0
    y = 0
    for pirate in group:
        x += pirate.location[0]
        y += pirate.location[1]
    return (int(x / len(group)), int(y / len(group)))

def closest_group(loc, groupsList):
    groups = []
    for group in groupsList:
        groups.append([group, distance(loc, group)])
    return [item[0] for item in sorted(groups, key = lambda item: item[1])][0]

def biggest_groups(groupsList):
    groups = []
    for group in groupsList:
        groups.append([group, len(group)])
        
    groups = [item[0] for item in sorted(groups, key = lambda item: item[1])][::-1]
    
    for group in groups:
        if len(group) != len(groups[0]):
            groups.remove(group)
            
    return groups

def is_pirate(o):
    return o.__class__.__name__ is game.my_pirates()[0].__class__.__name__

def is_island(o):
    return o.__class__.__name__ is game.islands()[0].__class__.__name__

def is_group(o):
    return type(o) is list

def is_location(o):
    return type(o) is tuple

def distance(loc1, loc2):
    if is_pirate(loc1) or is_island(loc1):
        loc1 = loc1.location
    if is_pirate(loc2) or is_island(loc2):
        loc2 = loc2.location

    if is_group(loc1):
        loc1 = group_location(loc1)
    if is_group(loc2):
        loc2 = group_location(loc2)
        
    return math.sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)

def running_pirates(pirates):
    runningPirates = []
    for pirate in pirates:
        if pirate.mode == RUNNING:
            runningPirates.append(pirate)
    return runningPirates

def pirate_target_count(pirates, target):
    count = 0
    for pirate in pirates:
        if pirate.target == target:
            count += 1
    return count

def pirates_location_count(pirates, location):
    count = 0
    for pirate in pirates:
        if game.get_pirate_on(location) == pirate:
            count += 1
    return count

def new_target(pirate, preIsland = 2):
    for island in closest_islands(pirate, game.not_my_islands()):
        if pirate_target_count([item for item in lstPirates if not item.is_lost and item != pirate], island) < preIsland:
            pirate.mode = ATTACKING
            return island
        
    if is_island(pirate.target):
        return pirate.target

    return closest_islands(pirate, game.islands())[0]

def is_group_capturing(group):
    for pirate in group:
        if game.is_capturing(pirate) or game.get_pirate_on(closest_islands(pirate, game.islands())[0]) == pirate:
            return True
    return False
 
def get_direction(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

def get_running_direction(pirate, enemyGroup, location):
    gloc = group_location(enemyGroup)
    x = gloc[1] - location[1]
    y = gloc[0] - location[0]
    theta = math.atan2(y, x)

    direction = int((theta - 45.0) / 90.0)

    if direction == 0:
        return (pirate.location[0], pirate.location[1] + 1)
    if direction == 1:
        return (pirate.location[0] - 1, pirate.location[1])
    if direction == 2:
        return (pirate.location[0], pirate.location[1] - 1)
    if direction == 3:
        return (pirate.location[0] + 1, pirate.location[1])
    
def group_has_same_target(group):
    target = group[0].target
    for pirate in group:
        if pirate.target != target:
            return False
    return True

def needs_to_be_arranged(group):
    if True in [is_location(item) for item in group]:
        return True

def is_all_arranged(pirates):
    for pirate in pirates:
        if not pirate.isArranged:
            return False
    return True

def arrange_attack(pirates):
    target = new_target(pirates[0], len(pirates))
    closestPirates = closest_pirates(target, pirates)
    closestPirate = closestPirates[0]
    targetLocations = []

    for i in xrange(-1, 2):
        for j in xrange(-1, 2):
            if distance(closestPirate, target) <= distance((closestPirate.location[0] + i, closestPirate.location[1] + j), target):
                targetLocations.append((closestPirate.location[0] + i, closestPirate.location[1] + j))

    count = 0
    for pirate in pirates:
        if pirate.isArranged:
            count += 1

    if count == len(pirates):
        for pirate in pirates:
            pirate.target = new_target(pirate, count)
        return True
    
    for pirate in pirates:
        if pirate == closestPirate:
            pirate.target = pirate.location
            pirate.isArranged = True
        else:
            closestLocations = closest_locations(closestPirates, [item for item in targetLocations if item != closestPirate.location])
            pirate.isArranged = False
            for location in closestLocations:
                if pirate.location == location:
                        pirate.isArranged = True
                elif distance(location, closestPirate) < distance(pirate, closestPirate) and pirates_location_count(pirates, location) == 0:
                    pirate.target = location
                    targetLocations.remove(pirate.target)
                    break
    
    return False

def set_all_sail(groups, arrange = False):
    arrangeGroups = [item for item in groups if item[0].mode != RUNNING]
    for group in groups:
        if is_all_arranged(group) or (arrange and arrange_attack(group)):
            pirates = closest_pirates(group[0].target, group)
            if pirates[0].mode == RUNNING:
                pirates = pirates[::-1]
            target = pirates[0].target
            if is_group(target):
                target = group_location(target)
            elif is_island(target) or is_pirate(target):
                target = target.location
                
            direction = game.get_directions(pirates[0], target)[0]
            
            for pirate in pirates:
                game.set_sail(pirate, direction)
                    
        else:
            for pirate in group:
                target = pirate.target
                if is_group(target):
                    target = group_location(target)
                elif is_island(target) or is_pirate(target):
                    target = target.location
                    
                directions = game.get_directions(pirate, target)
                direction = directions[0]
                    
                pirate.lastDirection = direction

                game.set_sail(pirate, direction)

lstPirates = None
otherStrategy = None
number= 1
def do_turn(g):
    global number
   
    global game
    game = g
    if(len(g.all_my_pirates())==4 and len(g.all_enemy_pirates())==6 and number==1):
        if(len(g.enemy_pirates())+1>len(g.my_pirates())):
            for my in g.my_pirates():
                pirate= filter(lambda x: (near_pirates(g,x.location)["enemies:"]-1<len(g.my_pirates())),closest_pirates(my.location,g.enemy_pirates()))[0]
                directions= g.get_directions(my.location,pirate)
                g.set_sail(my,directions[0])

    else:
        number=2
    global ATTACKING, RUNNING, ASSISTING, AGGRESSIVE
    ATTACKING = 0
    RUNNING = 1
    ASSISTING = 2
    AGGRESSIVE = 3
    
    if len(game.my_pirates()) == 0:
        return

    global lstPirates
    global otherStrategy
    if lstPirates == None:
        firstRun = False
        lstPirates = game.my_pirates()
        assign_target(lstPirates)
        otherStrategy = len(game.enemy_islands()) > 0 or len(game.enemy_pirates()) > len(game.my_pirates())
    else:
        lstPirates = update_pirates_list(lstPirates)

    alivePirates = [item for item in lstPirates if not item.is_lost]
    groups = find_groups(alivePirates)
    enemyGroups = find_groups(game.enemy_pirates())

    for pirate in lstPirates:
        if pirate.is_lost:
            continue

        group = closest_group(pirate, groups)
        otherPirates = [item for item in alivePirates if item != pirate]

        if otherStrategy:
            if len(game.enemy_pirates()) == 0:
                pirate.target = new_target(pirate, 1)
            else:
                pirate.target = closest_islands(lstPirates[0].initial_loc, game.not_my_islands())[0]
            continue

        if is_group(pirate.target) and pirate.target[0] in game.all_enemy_pirates() and not pirate.target in enemyGroups:
            pirate.target = new_target(pirate)

        if True:
            if len(game.not_my_islands()) == 0:
                if len(game.islands()) == 1:
                    closestIslands = closest_islands(pirate, game.islands())
                else:
                    pirate.target = new_target(pirate)
                    continue
            else:
                closestIslands = closest_islands(pirate, game.not_my_islands())
                
            if len(enemyGroups) >= 1:
                enemyGroup = closest_group(pirate, biggest_groups(enemyGroups))

                if is_all_arranged(group):
                    if len(group) == len(enemyGroup):
                        if is_group_capturing(enemyGroup) and len(group) > len(enemyGroup) - 1:
                            pirate.mode = AGGRESSIVE
                            pirate.target = enemyGroup
                            game.debug("0.25")
                        else:
                            pirate.mode = RUNNING
                            gloc = group_location(enemyGroup)
                            if distance(group, enemyGroup) <= 7:
                                pirate.target = (pirate.location[0], pirate.location[1] + get_direction(pirate.location[1] - gloc[1]))
                            game.debug("0.5")
                        continue
                '''
                if is_group_capturing(group) and distance(pirate, enemyGroup) <= 7:
                    pirate.mode = RUNNING
                    gloc = group_location(enemyGroup)
                    target = (pirate.location[0] + get_direction(pirate.location[0] - gloc[0]), pirate.location[1] + get_direction(gloc[1] - pirate.location[1]))
                    game.debug("4")
                el
                '''
                if distance(pirate, closestIslands[0]) < distance(pirate, enemyGroup) and closestIslands[0] in game.not_my_islands():
                    perIsland = 2
                    if len(enemyGroups) == 1:
                        perIsland = len(game.my_pirates())
                    pirate.target = new_target(pirate, perIsland)
                    game.debug("1")
                elif len(group) > len(enemyGroup):
                    if game.is_passable(group_location(enemyGroup)):
                        pirate.mode = AGGRESSIVE
                        pirate.target = enemyGroup
                        game.debug("2")
                    else:
                        perIsland = 2
                        if len(enemyGroups) == 1:
                            perIsland = len(game.my_pirates())
                        pirate.target = new_target(pirate, perIsland)
                        game.debug("2.5")
                else:
                    if is_group_capturing(enemyGroup) and len(group) > len(enemyGroup) - 1:
                        pirate.mode = AGGRESSIVE
                        pirate.target = enemyGroup
                        game.debug("3")
                    elif distance(pirate, enemyGroup) <= 7:
                        pirate.mode = RUNNING
                        gloc = group_location(enemyGroup)
                        target = (pirate.location[0] + get_direction(pirate.location[0] - gloc[0]), pirate.location[1] + get_direction(gloc[1] - pirate.location[1]))
                        game.debug("4")
                '''
                elif pirate_target_count(otherPirates, enemyGroup) <= len(enemyGroup) + 1:
                    pirate.mode = AGGRESSIVE
                    pirate.target = enemyGroup
                '''
            else:
                pirate.target = new_target(pirate)
                game.debug("5")
        
    for pirate in lstPirates:
        if pirate.is_lost:
            continue
        
        val = None
        if pirate.mode == ATTACKING:
            val = "attacking"
        elif pirate.mode == RUNNING:
            val = "running"
        elif pirate.mode == ASSISTING:
            val = "assisting"
        elif pirate.mode == AGGRESSIVE:
            val = "aggressive"
            
        game.debug("Id " + str(pirate.id) + ": " + val + ", Target: " + str(pirate.target) + ", PrevTarget: " + str(pirate.prevTarget))
        
    set_all_sail(groups, len(groups) == len(game.not_my_islands()) == 1)









