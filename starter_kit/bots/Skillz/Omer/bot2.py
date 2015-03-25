




















import math

def closest_islands(loc, islandsList):
    islands = []
    for island in islandsList:
        islands.append([island, distance(loc, island.location)])
    return [item[0] for item in sorted(islands, key = lambda item: item[1])]

def closest_pirate(loc, group):
    pirates = []
    for pirate in group:
        pirates.append([pirate, distance(loc, pirate.location)])
    return [item[0] for item in sorted(pirates, key = lambda item: item[1])][0]

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

def assign_target(pirates, islands, order):
    count = 0
    index = 0
    for pirate in pirates:
        pirate.target = islands[index]
        pirate.mode = ATTACKING
        pirate.lastDirection = '-'
        pirate.prevTarget = None
        count += 1

        if count >= order[index]:
            count = 0
            index += 1

def update_pirates_list(pirates):
    lst = []
    for pirate in pirates:
        p = game.get_my_pirate(pirate.id)
        
        if is_pirate(pirate.target):
            p.target = game.get_my_pirate(pirate.target.id)
        else:
            p.target = pirate.target

        if is_pirate(pirate.prevTarget):
            p.prevTarget = game.get_my_pirate(pirate.prevTarget.id)
        else:
            p.prevTarget = pirate.prevTarget
            
        p.mode = pirate.mode
        p.lastDirection = pirate.lastDirection
        lst.append(p)
    return lst

def find_groups(p, radius = 5):
    pirates = list(p)
    groups = []

    while len(pirates) != 0:
        groups.append([])
        index = 1
        while index < len(pirates):
            if distance(pirates[0].location, pirates[index].location) <= radius:
                groups[-1].append(pirates[index])
                pirates.remove(pirates[index])
            else:
                index += 1
        groups[-1].append(pirates[0])
        pirates.remove(pirates[0])

    return groups

def group_location(group):
    x = 0
    y = 0
    for pirate in group:
        x += pirate.location[0]
        y += pirate.location[1]
    return (int(x / len(group)), int(y / len(group)))

def find_closest_group(loc, groupsList):
    groups = []
    for group in groupsList:
        groups.append([group, distance(loc, group)])
    return [item[0] for item in sorted(groups, key = lambda item: item[1])][0]

def is_pirate(o):
    return o.__class__.__name__ is game.my_pirates()[0].__class__.__name__

def is_island(o):
    return o.__class__.__name__ is game.islands()[0].__class__.__name__

def is_group(o):
    return type(o) is list

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

def set_sail(pirate, target):
    if is_group(target):
        target = group_location(target)
        
    directions = game.get_directions(pirate, target)
    direction = directions[0]
    
    if pirate.mode == RUNNING and len(directions) > 1 and direction == pirate.lastDirection:
        direction = directions[1]
        
    pirate.lastDirection = direction
    
    game.set_sail(pirate, direction)

def invert_y(loc):
    return (loc[0], game.rows - loc[1])

def get_running_route(pirate, closestGroup, closestEnemy):
    loc1 = invert_y(pirate.location)
    loc2 = invert_y(group_location(closestGroup))
    loc3 = invert_y(group_location(closestEnemy))

    vec1 = (loc2[0] - loc1[0], loc2[1] - loc1[1])
    vec2 = (loc1[0] - loc3[0], loc1[1] - loc3[1])
    vec3 = (vec1[0] + vec2[0], vec1[1] + vec2[1])

    if abs(vec3[0]) > abs(vec3[1]):
        return (loc1[0] + abs(vec3[0]) / vec3[0], loc1[1])
    else:
        return (loc1[0], loc1[1] + abs(vec3[1]) / vec3[1])

def running_pirates(pirates):
    runningPirates = []
    for pirate in pirates:
        if pirate.mode == RUNNING:
            runningPirates.append(pirate)
    return runningPirates

def new_target(pirate, islands):
    return closest_islands(pirate.location, [island for island in islands if island in game.not_my_islands()])[0]

lstPirates = None

def do_turn(g):
    global game
    game = g

    global ATTACKING, RUNNING, ASSISTING
    ATTACKING = 0
    RUNNING = 1
    ASSISTING = 2
    
    if len(game.my_pirates()) == 0:
        return

    global lstPirates
    if lstPirates == None:
        firstRun = False
        lstPirates = game.my_pirates()
        lstIslands = find_target_islands()
        lstOrder = find_order(lstPirates, lstIslands)
        assign_target(lstPirates, lstIslands, lstOrder)
    else:
        lstPirates = update_pirates_list(lstPirates)

    alivePirates = [pirate for pirate in lstPirates if not pirate.is_lost]
    groups = find_groups(alivePirates)
    enemyGroups = find_groups(game.enemy_pirates())

    for pirate in lstPirates:
        if pirate.is_lost:
            game.debug("Id " + str(pirate.id) + ": lost")
            continue

        val = None
        if pirate.mode == ATTACKING:
            val = "attacking"
        if pirate.mode == RUNNING:
            val = "running"
        if pirate.mode == ASSISTING:
            val = "assisting"
            
        game.debug("Id " + str(pirate.id) + ": " + val + ", Target: " + str(pirate.target) + ", PrevTarget: " + str(pirate.prevTarget))

        # the group of the current pirate
        group = find_closest_group(pirate, groups)

        # checks if find_closest_group will not generate an exception
        if len(groups) > 1:
            # closest friendly group
            closestGroup = find_closest_group(group, [item for item in groups if item != group])

        # checks if find_closest_group will not generate an exception
        if len(game.enemy_pirates()) > 0:
            # closest enemy group to current target
            closestEnemyByTarget = find_closest_group(pirate.target, enemyGroups)
            # closest enemy group to my group
            closestEnemyByGroup = find_closest_group(group, enemyGroups)

        # if needs to attack
        if pirate.mode == ATTACKING:
            # if has enemy and enemy group is too close
            if len(game.enemy_pirates()) > 0 and (distance(closestEnemyByTarget, pirate.target) <= 6 or distance(closestEnemyByGroup, group) <= 6):
                # if my group can win the enemy attack enemy
                if len(closestEnemyByTarget) < len(group):
                    game.debug("changed target 2")
                    pirate.target = closestEnemyByTarget
                # if my group can not win go to closest friendly group
                elif len(groups) > 1:
                    game.debug("changed target 3")
                    pirate.target = closestGroup
                    pirate.mode = RUNNING
            # if enemy is not close
            else:
                # if captured current target check if someone needs help
                if pirate.target in game.my_islands():
                    running = running_pirates(alivePirates)
                    # if someone is running
                    if len(running) > 0:
                        game.debug("changed target 4")
                        pirate.prevTarget = pirate.target
                        pirate.target = closest_pirate(pirate, running)
                        pirate.mode = ASSISTING
                    else:
                        # generate a new target
                        pass
                
                if pirate.prevTarget != None and not pirate.prevTarget in game.my_islands():
                    game.debug("changed target 5")
                    pirate.target = pirate.prevTarget

            # if killed enemy target
            if is_group(pirate.target) and (pirate.target[0] in game.enemy_lost_pirates() or distance(closestEnemyByTarget, pirate.prevTarget) <= 5):
                game.debug("changed target 6")
                # return to the original target
                pirate.target = pirate.prevTarget

        # if pirate running away
        if pirate.mode == RUNNING:
            # if target is still threatened or enemy group is too close
            if len(game.enemy_pirates()) > 0 and (distance(closestEnemyByTarget, pirate.prevTarget) <= 5 or distance(closestEnemyByGroup, group) <= 5):
                # if can win enemy group go to original target (if pirate is attacking it means that he is capturing and therefore no available)
                if len(closestEnemyByTarget) < len([item for item in group if item.mode == RUNNING or item.mode == ASSISTING]):
                    game.debug("changed target 7")
                    pirate.target = pirate.prevTarget
                    pirate.mode = ATTACKING
            # return to original target
            else:
                game.debug("changed target 8")
                pirate.target = pirate.prevTarget
                pirate.mode = ATTACKING

        # if pirate is helping other pirates
        if pirate.mode == ASSISTING:
            # if pirate needs no assist anymore return to original target
            if not (len(game.enemy_pirates()) > 0 and (distance(closestEnemyByTarget, pirate.target.prevTarget) <= 5 or distance(closestEnemyByGroup, group) <= 5)):
                game.debug("changed target 9")
                pirate.target = pirate.prevTarget
                pirate.mode = ATTACKING
        
    for pirate in lstPirates:
        if pirate.is_lost:
            continue
        set_sail(pirate, pirate.target)









