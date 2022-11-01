from graph_games import Game
import random
import operator
import itertools
from typing import List, Any, Optional

Player = Any



def bestResponseSingleStep(g: Game, population: List[Player]) -> Optional[Player]: 
    """
    solve for NE using best response path for single step
    Input: 
        - g: an instance of Game in graph_game
        - population: a list containing all players in Game g, the algorithm will check possible update using best response in the given order
    Return: 
        None or player:
            - if the return value is None, means g is already in Nash Equilibrium
            - if the return value is a player, means we updated the player in last step
    """
    for p in population: 
        current_util = g.getUtil(p)
        possible_acts = list(g.getPossibleActions(p))
        possible_utils = g.getUtils(p, possible_acts)
        # the first occorrance of the best responce 
        best_act_index, best_util = max(enumerate(possible_utils), key=operator.itemgetter(1))

        if current_util == best_util: 
            continue
        else:
            best_act = possible_acts[best_act_index]
            g.setAction(p, best_act)
            return p
    return None

def bestResponseSolver(g: Game ) -> int:
    """
    Trace along best-response path toward a Nash-Equilibrium
    Input:
        A instance of Game defined in graph_games 
    Return:  
        number of iterations during the solving, each iteration we overwrite the action of a player with his best response. 
    """
    population = list(g.getPlayers())
    for total_iters in itertools.count(start=1, step=1): 
        # get random order of the population
        random.shuffle(population)
        if bestResponseSingleStep(g, population) == None: 
            return total_iters
        

if __name__ == '__main__' :
    import graph
    from graph_games import K_DominationGame, AsymmetricIDSGame
    for game in ["K_DominationGame", "AsymmectricIDSGame"]: 
        print("-"*30)
        print(f'Game = {game}')
        print(f'{"rewiring_prob":15}, {"move_counts per node":15}, {"cardinality":15}')
        for rewire_prob_times_10 in range(0, 10, 2):
            rewiring_prob = rewire_prob_times_10 / 10
            move_counts = []
            cardinalities = []
            for i in range(100):
                g = graph.randomWSGraph(n=30, k=4, link_rewiring_prob=rewiring_prob)
                if game == "K_DominationGame":
                    gg = K_DominationGame(2, g) # run with k = 2
                else: 
                    gg = AsymmetricIDSGame(g)
                
                move_count = gg.solve(bestResponseSolver)
                cardinality = gg.dominationSetCardinality()
                move_counts.append(move_count)
                cardinalities.append(cardinality)

                if game == "K_DominationGame":
                    assert gg.checkDomination()
                else:
                    assert gg.checkDomination()
                    assert gg.checkIndependence() 
            print(f'{rewiring_prob:15.2f}, {sum(move_counts)/100 / 30:15.2f}, {sum(cardinalities)/100:15.2f}')
                    


