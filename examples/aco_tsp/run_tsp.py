from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as nx

from aco_tsp.model import AcoTspModel, TSPGraph # create_graph


def run_episode(model, model_params):
    for _ in range(model_params["tsp_graph"].num_cities):
        model.step()

    
def main():
    # tsp_graph = TSPGraph.from_random(num_cities=20, seed=1)
    tsp_graph = TSPGraph.from_tsp_file("aco_tsp/data/kroA100.tsp")
    model_params = {
        "num_agents": tsp_graph.num_cities, "tsp_graph": tsp_graph,
    }
    number_of_episodes = 500

    results = defaultdict(list)

    best_path = None
    best_distance = float("inf")
    for e in range(number_of_episodes):
        model = AcoTspModel(**model_params)
        run_episode(model, model_params)
        results["best_distance"].append(model.best_distance)
        results["best_path"].append(model.best_path)
        print(f"Episode={e+1}; Min. distance={model.best_distance}; pheromone_1_8={tsp_graph.g[17][15]['pheromone']}")
        if model.best_distance < best_distance:
            best_distance = model.best_distance
            best_path = model.best_path
            print(f"New best distance:  distance={best_distance}")
        
        tsp_graph.update_pheromone(model=model)

    print(f"Best distance: {best_distance}")
    print(f"Best path: {best_path}")
    fig, ax = plt.subplots()
    ax.plot(results["best_distance"])
    ax.set(xlabel="Episode", ylabel="Best distance", title="Best distance per episode")
    plt.show()



if __name__ == "__main__":
    main()