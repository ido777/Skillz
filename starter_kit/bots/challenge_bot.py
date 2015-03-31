
def do_turn(game):
    pirates = game.my_pirates()
    islands = game.islands()

    for pirate, island in zip(pirates, islands):
        direction = game.get_directions(pirate, island)[0]
        game.set_sail(pirate, direction)
