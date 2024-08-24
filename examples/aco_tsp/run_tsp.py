from collections import defaultdict

import matplotlib.pyplot as plt
from aco_tsp.model import AcoTspModel, TSPGraph


def main():
    # tsp_graph = TSPGraph.from_random(num_cities=20, seed=1)
    tsp_graph = TSPGraph.from_tsp_file("aco_tsp/data/kroA100.tsp")
    model_params = {
        "num_agents": tsp_graph.num_cities,
        "tsp_graph": tsp_graph,
    }
    number_of_episodes = 50

    results = defaultdict(list)

    best_path = None
    best_distance = float("inf")

    model = AcoTspModel(**model_params)

    for e in range(number_of_episodes):
        # model = AcoTspModel(**model_params)
        model.step()
        results["best_distance"].append(model.best_distance)
        results["best_path"].append(model.best_path)
        print(
            f"Episode={e + 1}; Min. distance={model.best_distance:.2f}; pheromone_1_8={model.grid.G[17][15]['pheromone']:.4f}"
        )
        if model.best_distance < best_distance:
            best_distance = model.best_distance
            best_path = model.best_path
            print(f"New best distance:  distance={best_distance:.2f}")

    print(f"Best distance: {best_distance:.2f}")
    print(f"Best path: {best_path}")
    # print(model.datacollector.get_model_vars_dataframe())

    _, ax = plt.subplots()
    ax.plot(results["best_distance"])
    ax.set(xlabel="Episode", ylabel="Best distance", title="Best distance per episode")
    plt.show()


if __name__ == "__main__":
    main()
