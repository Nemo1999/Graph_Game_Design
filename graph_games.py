from typing import Set, Dict, Any, Callable, Iterator
from collections import defaultdict
import itertools
import random
import graph

Action = Any
Player = Any


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

    def getPossibleActions(self, p: Player) -> Set[Action]:
        """ return all posible actions for a single player"""
        pass

    def getUtil(self, player: Player) -> float:
        """
         Return the utilities of a player in current strategy profile
        """
        pass

    def getUtils(self, player: Player, actions: Iterator[Action]) -> Iterator[float]:
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
        pass

    def solve(self, solver: Callable[["Game"], int]) -> int: 
        """solve the game using the given solver, return the iterations used"""
        return solver(self)


class K_DominationGame(Game):
    """ 
    Simulate a K-Domination Game
    """

    def __init__(self, k: int,  graph: graph.Graph, alpha=2, beta=1) -> None:
        """
        make a K-domination Game from a given Graph
        Parameter:
            k: the minimum number of dominator-neighbors required for each non-dominator node in a valid solution
            graph: an instance of Graph from graph.py
            alpha: utility gain for a player choosing "True" when a neibouring node is not yet k-dominated.
            beta: utility penalty (cost) for a player choosing "True" 
        Note: we should have alpha > beta > 0 in order to get Nash Equilibriums that correspond to K-Dominating Sets 
        """
        assert 0 < beta and beta < alpha
        # whether record whether a player is in the domination set
        self.k = k
        self.graph = graph
        self.dominators = set()
        self.players = self.graph.nodes
        self.alpha = alpha
        self.beta = beta
        # cache the number of nodes that dominate a particular node for faster computation
        # self.numDominator[p] should equal to len(set.intersection( graph.neibors, self.dominators ))
        self.numDominator: Dict[Player, int] = defaultdict(lambda: 0)

    def randomInit(self) -> None:
        """randomly initialize the strategies for each player"""
        self.dominators.clear()
        for p in self.players:
            if random.randint(0, 1) > 0:
                self.dominators.add(p)
                for n in self.graph.neighbors(p):
                    self.numDominator[n] += 1

    def getPlayers(self) -> Set[str]:
        return self.players.copy()

    def getPossibleActions(self, player: str) -> Set[bool]:
        return set([True, False])

    def getAction(self, player: str) -> bool:
        return player in self.dominators

    def getProfile(self) -> Dict[str, bool]:
        profile = defaultdict(lambda: False)
        for p in self.players:
            profile[p] = True
        return profile

    def getUtil(self, player: str) -> float:
        if player not in self.dominators:
            return 0
        elif self.graph.degree(player) < self.k:
            return self.alpha
        else:
            def g(n):
                if n not in self.dominators and self.numDominator[n] <= self.k:
                    return self.alpha
                else:
                    return 0
            return sum(g(n) for n in self.graph.neighbors(player)) - self.beta

    def getUtils(self, player: str, actions: Iterator[bool]) -> Iterator[bool]:
        original_action = player in self.dominators
        utils = []
        for a in actions:
            self.setAction(player, a)
            utils.append(self.getUtil(player))
        self.setAction(player, original_action)
        return utils

    def setAction(self, player: str, action: Action) -> None:
        if player in self.dominators:
            if action == False:
                self.dominators.remove(player)
                for n in self.graph.neighbors(player):
                    self.numDominator[n] -= 1
        else:
            if action == True:
                self.dominators.add(player)
                for n in self.graph.neighbors(player):
                    self.numDominator[n] += 1

    def setProfile(self, profile: Dict[Player, Action]) -> None:
        for p in self.players:
            self.setAction(p, profile[p])
    
    def checkDomination(self) -> bool: 
        """check whether K-Domination condition is met"""
        return all( self.numDominator[p] >= self.k for p in self.players-self.dominators)

    def dominationSetCardinality(self) -> int:
        assert self.checkDomination() ,"The game hasn't been solved yet, the current solution is not k-domination set"
        return len(self.dominators)

class asymmetricIDSGame(K_DominationGame):
    """
    Asymmectric Minimum-Dominating-Set-based Independent Dominateding Set Game
    
    we use K_DominationGame as base class and overwrite the following functions:
    - getUtil()
    - checkDomination()
    we also add a new function:
    - checkIndependence()

    """
    def __init__(self,  graph: graph.Graph, alpha=2, beta=1) -> None:
        # set k = 1
        super().__init__(1, graph, alpha, beta)
        # make sure gamma larger than maximum degree times alpha
        maxDegree = max(self.graph.degree(p) for p in self.graph.nodes)
        self.gamma = maxDegree * alpha + 1
    
    def checkDomination(self) -> bool:
        """ check whether dominaion condition is met
            it turns out that single domination is equivilent to k-domination with k = 1
        """
        return super().checkDomination()
    
    def checkIndependence(self) -> bool:
        """check that the dominaotors are independent"""
        return all(self.graph.neighbors(d).isdisjoint(self.dominators) for d in self.dominators)

    def getUtil(self, player: str) -> float:
        def g(i):
            numDominatorIncludeSelf = self.numDominator[i]
            numDominatorIncludeSelf += 1 if i in self.dominators else 0
            return self.alpha if  numDominatorIncludeSelf == 1 else 0
        
        if player in self.dominators:
            # gain for dominating neighboring nodes
            ans = sum(g(i) for i in itertools.chain(self.graph.neighbors(player),[player]))  
            # penalty for being a dominator
            ans -= self.beta 
            # panelty for violating independence, (assymetric, only cares neighbors with higher degrees) 
            ans -= sum(self.gamma for n in self.graph.neighbors(player) if n in self.dominators)
        else: 
            ans = 0
        return ans
