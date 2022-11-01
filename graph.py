from collections import defaultdict
from typing import Set, Dict, Iterable, Tuple
import copy
import random
# undirected graph

class Graph:
    def __init__(self) -> None:
        self.edges : Dict[str, Set[str]] = defaultdict(set) # map each node index to the set of its neibours' indexes
        self.nodes : Set[str] = set()

    def node(self, node: str) -> None:
        self.nodes.add(node)

    def edge(self, node1: str, node2:str) -> None:
        self.edges[node1].add(node2)
        self.edges[node2].add(node1)

    def edgeDel(self, node1:str , node2: str) -> None:
        self.edges[node1].remove(node2)
        self.edges[node2].remove(node1)

    def nodeDel(self, node) -> None:
        if node in self.nodes:
            self.nodes.remove(node)
            for n in self.edges[node]:
                self.edges[n].remove(node)
            del self.edges[node]
    
    def addEdges(self, pairs: Iterable[Tuple[str,str]]) -> None:
        map(lambda n1, n2: self.edge(n1,n2), pairs)

    def neighbors(self, node: str) -> None:
        return self.edges[node]

    def degree(self, node: str) -> None:
        return len(self.edges[node])

    def clone(self) -> "Graph": 
        return copy.deepcopy(self)


def randomWSGraph(n=16, k=4, link_rewiring_prob=0.0):
    """randomly initialize a graph using Watts-Strogatz Model"""
    # k should be even
    assert k % 2 == 0
    ws = Graph()
    
    for i in range(n):
        ws.node(str(i))

    for i in range(n):
        for dk in range(1, k//2+1):
            j = i + dk
            if random.random() > link_rewiring_prob:
                # change j to a random node that is not already connected to i
                j = random.choice(list(n for n in ws.nodes if n not in ws.neighbors(str(i))))
            ws.edge(str(i),str(j))
    
    return ws

