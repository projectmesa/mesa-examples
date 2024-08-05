import networkx as nx

from aco_tsp.model import AcoTspModel, create_graph


def run_iteration(model, model_params):
    for _ in range(model_params["num_cities"]):
        model.step()

def update_pheromone(
        graph: nx.Graph, 
        model: AcoTspModel, 
        q: float = 100, 
        ro: float=0.5
    ):
    # tau_ij(t+1) = (1-ro)*tau_ij(t) + delta_tau_ij(t)
    # delta_tau_ij(t) = sum_k^M {Q/L^k} * I[i,j \in T^k]
    delta_tau_ij = dict()
    for k, agent in enumerate(model.schedule.agents):
        delta_tau_ij[k] = agent.calculate_pheromone_delta(q)

    for i, j in graph.edges():
        # Evaporate
        tau_ij =  (1-ro)*graph[i][j]['pheromone']
        # Add ant's contribution
        for k, delta_tau_ij_k in delta_tau_ij.items():
            tau_ij += delta_tau_ij_k.get((i,j), 0.)

        graph[i][j]['pheromone'] = tau_ij

    return graph

    
def main():
    num_cities = 20
    graph, node_positions = create_graph(num_cities, seed=1)
    model_params = {
        "num_agents": 20, "num_cities": num_cities, 
        "g": graph, "pos": node_positions
    }
    number_of_episodes = 1_000

    best_path = None
    best_distance = float("inf")
    for e in range(number_of_episodes):
        model = AcoTspModel(**model_params)
        # model.reset_randomizer(seed=e)
        run_iteration(model, model_params)
        print(f"Episode={e+1}; Min. distance={model.best_distance}; pheromone_0_8={graph[0][8]['pheromone']}")
        if model.best_distance < best_distance:
            best_distance = model.best_distance
            best_path = model.best_path
            print(f"New best distance:  distance={best_distance}")
        
        graph = update_pheromone(graph=graph, model=model)

    print(f"Best path: {best_path}")


if __name__ == "__main__":
    main()