# Embedded file name: D:\Users\Akiva\Competition\cyber-pirates\admin-tools\simulator\bots\python\Demo2.py
""" Demo 3 sends a single pirate at a time to conquer the closest island """
cur_pirate = None

def do_turn(game):
    global cur_pirate
    if len(game.not_my_islands()) == 0:
        return
    elif len(game.my_pirates()) == 0:
        return
    else:
        if cur_pirate is None or game.get_my_pirate(cur_pirate).is_lost:
            cur_pirate = game.my_pirates()[0].id
        pirate = game.get_my_pirate(cur_pirate)
        island = None
        min_dist = 9999
        for i in game.not_my_islands():
            d = game.distance(i, pirate)
            if d < min_dist:
                min_dist = d
                island = i

        directions = game.get_directions(pirate, island)
        game.set_sail(pirate, directions[0])
        return