from typing import Set, Dict, Any, Callable, Iterator
from dataclasses import dataclass
from collections import defaultdict
import copy

import graph

Action = Any
Player = Any

@dataclass
class Game: 
    """
        A Game Object should maintain its own internal state, 
        and implement the following functions as interface for
            1. query game information ( getPlayers, getAction, getProfile, getPossibleActions )
            2. query utility function ( getUtil, getUtils )
            3. modify player stategy  ( setAction, setProfile) 
        
    """
    def __init__(self) -> None:
        return

    def getPlayers(self) -> Set[Player]:
        """ return the set of all players in the game"""
        pass

    def getAction(self, player: Player) -> Action:
        """ return current action of a player"""
        pass

    def getProfile(self) -> Dict[Player, Action]:
        """ return strategy profile for current game state (action for each player) """
        pass

    def getPossibleActions(self, p : Player) -> Set[Action]:
        """ return all posible actions for a single player"""
        pass

    def getUtil(self, player: Player) -> float :
        """
         Return the utilities of a player in current strategy profile
        """
        pass

    def getUtils(self, player: Player, actions: Iterator[Action]) -> Iterator[float] :
        """ 
            Return the utilities of a player for a set possible actions
            Parameters
                player: the player whose utility to return
                actions: contains a iterator of possible actions for current player
            Return
                a list of scores corresponding to actions
        """
        pass

    def setAction(self, player: Player, action: Action) -> None:
        """ set the current strategy of a player to certain action"""
        pass

    def setProfile(self, profile: Dict[Player, Action]) -> None:
        """ set the current strategy profile to argument"""


class K_DominationGame(Game): 
    def __init__(self, graph: graph.Graph)-> None:
        """make a K-domination Game from a given Graph"""
        # whether record whether a player is in the domination set
        self.graph = graph
        self.dominators = set()
        self.player = self.graph.nodes

    def randomInit(self):
        """randomly initialize the strategies for each player"""
        pass

    def getPlayers(self) -> Set(str):
        return self.players.copy() 
    
    def getPossibleActions(self, player: str) -> Set[bool]:
        return set([True, False])

    def getAction(self, player: str) -> bool: 
        return player in self.dominators
    
    def getProfile(self):
        profile = defaultdict(lambda: False)
        for p in self.players:
            profile[p] = True
        return profile
    
    
    