from typing import NewType, Set, Dict, Any, Callable
from dataclasses import dataclass
from collections import defaultdict

import graph

Action = Any
Player = Any

@dataclass
class Game: 
    players: Set[Player]
    strategySet: Dict[Player, Set(Action)]
    strategy: Dict[Player,Action]
    utility: Callable[[Player], Dict[Action, float]]
    """
    A Game should contains the following fields
    1. palyers: A set of players
    2. strategySet: A set of possible actions for each player
    2. strategy: Get current strategy for each player
    3. utility: A function that calculate the utility corresponding to all possible actions for a single player, based on current strategy
    """

class K_DominationGame: 
    def __init__(self, graph: graph.Graph)-> :
        """make a K-domination Game from a given Graph"""
        # each graph node is a player
        self.players : Set[str] = graph.nodes
        # whether record whether a player is in the domination set

        
        self.graph = graph

    def randomInitStrategies():
        """randomly initialize the strategies for each player"""
        pass
    
    def utility(player: str) -> Dict[bool, float]: 
        """utility of a single player based on current strategy"""

    def createGame(self) -> Game: 
        # All possible strategies for each players
        strategySet: Dict[str, Set[bool]] = defaultdict(lambda : set([True, False])) 
        return Game(self.palyers, strategySet,  self.strategy, )