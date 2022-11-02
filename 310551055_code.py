import graph
from graph_games import K_DominationGame, AsymmetricIDSGame, MaximalMatchingGame
from graph_games import Game
from game_solver import bestResponseSolver

print("== Part 1" + "="*20)
for game in ["K_DominationGame", "AsymmectricIDSGame"]:
    print("-"*30)
    print(f'Game = {game}')
    print(f'{"rewiring_prob":15}, {"move_counts per node":15}, {"cardinality":15}')
    for rewire_prob_times_10 in range(0, 10, 2):
        rewiring_prob = rewire_prob_times_10 / 10
        move_counts = []
        cardinalities = []
        for i in range(100):
            g = graph.randomWSGraph(
                n=30, k=4, link_rewiring_prob=rewiring_prob)
            if game == "K_DominationGame":
                gg = K_DominationGame(2, g)  # run with k = 2
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
        print(
            f'{rewiring_prob:15.2f}, {sum(move_counts)/100 / 30:15.2f}, {sum(cardinalities)/100:15.2f}')
print("== Part 2" + "="*20)
for util_setting in [(False, False), (True, False), (True, True)]:
    print("-"*30)
    print(f'Game = Maximal Matching Game')
    print(
        f'Utils: deg_panelty={util_setting[0]}, robbing_reward={util_setting[1]}')
    print(
        f'{"rewiring_prob":15}, {"move_counts per node":15}, {"matching_counts":15}')
    for rewire_prob_times_10 in range(0, 10, 2):
        rewiring_prob = rewire_prob_times_10 / 10
        move_counts = []
        matching_counts = []
        for i in range(100):
            g = graph.randomWSGraph(
                n=30, k=4, link_rewiring_prob=rewiring_prob)
            gg = MaximalMatchingGame(
                g, deg_penalty=util_setting[0], robbing_reward=util_setting[1])
            gg.randomInit()
            move_count = gg.solve(bestResponseSolver)
            matching_count = gg.numMatchingPairs()
            move_counts.append(move_count)
            matching_counts.append(matching_count)
            assert gg.checkMaximalMatching()
        print(
            f'{rewiring_prob:15.2f}, {sum(move_counts)/100 / 30:15.2f}, {sum(matching_counts)/100:15.2f}')