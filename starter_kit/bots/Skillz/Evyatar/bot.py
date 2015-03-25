def near_islands(game,my_pirate,islands):
    nearest = 999999
    dist = 0
    closest_island=islands[0]
    
    for island in islands:
        dist = game.distance(my_pirate,island)
        if island.team_capturing == game.NEUTRAL:
            dist = dist / 2
        if dist<nearest:
            nearest = game.distance(my_pirate,island)
            closest_island=island
    return closest_island

def near_enemies(game,my_pirate,enemies):
    nearest = 999999
    dist = 0
    closest_island=enemies[0]
    
    for enemy in enemies:
        dist = game.distance(my_pirate,enemy)
        if dist<nearest:
            nearest = dist
            closest_island=enemy
    return closest_island
    
def do_turn(game):
    pirates = game.my_pirates()
    if len(pirates) == 0:
        return
    
    islands = game.not_my_islands()
    enemies = game.enemy_pirates()
    
    if len(islands) == 0:
        if len(enemies) != 0:
            i = 0
            for pirate in pirates:
                direction = game.get_directions(pirate, near_enemies(game,pirate,enemies))[0]
                game.set_sail(pirate, direction)
                i += 1
                if i >= len(enemies) or i >= 2:
                    i = 0
    else:
        i = 0
        isl = list(islands)
        for pirate in pirates:
            if not game.is_capturing(pirate):
                if len(isl) == 0:
                    isl = list(islands)
                direction = game.get_directions(pirate, near_islands(game,pirate,isl))[0]
                game.set_sail(pirate, direction)
                i += 1
                if i >= len(islands) or i >= 2:
                    i = 0
                    isl.remove(near_islands(game,pirate,isl))