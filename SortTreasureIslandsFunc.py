def Treasure_Islands(game):

    #this function return a list with the islands that have treasures. The list sorted by the value of the treasure islands
    #if both treasure islands have the same value the sorting will be by the capture turns.

    treasure_islands = []
    island_values = (1, 2, 4, 8, 16)
    islands_value = island_values[-1]
    for island in game.islands():
        if island.value != islands_value:
            for i in xrange(len(treasure_islands) + 1):
                if i == len(treasure_islands):
                    treasure_islands.append(island)
                    break
                if treasure_islands[i].value() < island.value():
                    treasure_islands.insert(i ,island)
                    break
                elif treasure_islands[i].value() == island.value():
                    if treasure_islands[i].capture_turns() > island.capture_turns(): #the parameter of capturing can be changed
                        treasure_islands.insert(i ,island)
                        break
    return treasure_islands

def treasure_islands():
    #get all the islands with value more than one
    islands = [island for island in g.islands() if (island.values>1)]
    #sort by the value
    return islands.sort(key = lambda island:island.value)[::-1] #reverse
