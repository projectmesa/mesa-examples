Ant System for the Traveling Salesman Problem
========================

This is an implementation of the Ant System (AS) algorithm for solving the Traveling Salesman Problem (TSP).  This example uses Mesa's Network Grid to model a TSP by representing cities as nodes and the possible paths between them as edges.  Ants are then modeled as Mesa Agents that generate solutions by traversing the network using a "swarm intelligence" algorithm.

When an ant is choosing its next city, it consider both a pheromone trail laid down by previous ants and a greedy heuristic based on city proximity.  Pheromone evaporates over time and the strength of new pheromone trail laid by an ant is proportional to the quality of its TSP solution.  This produces an emergent solution as the pheromone trail is continually updated and guides ants to high quality solutions as they are discovered.

As this model runs, more pheromone will be laid on better solutions, and less traveled paths will have their pheromone evaporate.  Ants will therefore reinforce good paths and abandon bad ones.  Since decisions are ultimately samples from a weighted probability distribution, ants will sometimes explore unlikely paths, which might lead to new strong solutions that will be reflected in the updated pheromone levels.

Here, we plot the best solution per iteration, the best solution so far in all iterations, and a graph representation where the edge width is proportional to the pheromone quantity.  You will quickly see most of the edges in the fully connected graph disappear and a subset of the paths emerge as reasonable candidates in the final TSP solution.

## How to run
To launch the interactive visualization, run `solara run app.py` in this directory.  Tune the $\alpha$ and $\beta$ parameters to modify how much the pheromone and city proximity influence the ants' decisions, respectively.  See the Algorithm details section for more.

Alternatively, to run for a fixed number of iterations, run `python run_tsp.py` from this directory (and update that file with the parameters you want).

## Algorithm details
Each agent/ant is initialized to a random city and constructs a solution by choosing a sequence of cities until all are visited, but none are visited more than once.  Ants then deposit a "pheromone" signal on each path in their solution that is proportional to 1/d, where d is the final distance of the solution.  This means shorter paths are given more pheromone.

When an ant is on city $i$ and deciding which city to choose next, it samples randomly using the following probabilities of transition from city $i$ to $j$:

$$
p_{ij}^k =  \frac{\tau_{ij}^\alpha \eta_{ij}^\beta}{\sum_{l \in J_i^k} \tau_{il}^\alpha \eta_{il}^\beta}
$$

where:
- $\tau_{ij}$ is the amount of path pheromone
- $\eta_{ij}$ the a greedy heuristic of desireability
  - In this case, $\eta_{ij} = 1/d_{ij}$, where $d_{ij}$ is the distance between
    cities
- $\alpha$ is a hyperparameter setting the importance of the pheromone
- $\beta$ a hyperparameter for setting the importance of the greedy heuristic
- And the denominator sum is over $J_i^k$, which is the set of cities not yet
  visited by ant $k$.

In other words, $\alpha$ and $\beta$ are tuned to set the relative importance of the phermone trail left by prior ants, and the greedy heuristic of 1-over-distance.

## Data collection
The following data is collected and can be used for further analysis:
- Agent-level (individual ants, reset after each iteration)
  - `tsp_distance`: TSP solution distance
  - `tsp_solution`: TSP solution path
- Model-level (collection of ants over many iterations)
  - `num_steps`: number of algorithm iterations, where one step means each ant generates a full TSP solution and the pheromone trail is updated
  - `best_distance`: the distance of the best path found in all iterations
    - This is the best solution yet and can only stay flat or improve over time
  - `best_distance_iter`: the distance of the best path of all ants in a single iteration
    - This changes over time as the ant colony explores different solutions and can be used to understand the explore/exploit trade-off.  E.g., if the colony quickly finds a good solution, but then this value trends upward and stays high, then this suggests the ants are stuck re-inforcing a suboptimal solution.
  - `best_path`: the best path found in all iterations

## References
- Original paper:  Dorigo, M., Maniezzo, V., & Colorni, A. (1996). Ant system: optimization by a
colony of cooperating agents. IEEE transactions on systems, man, and cybernetics,
part b (cybernetics), 26(1), 29-41.
- Video series of this code being implemented:  https://www.youtube.com/playlist?list=PLSgGvve8UweGk2TLSO-q5OSH59Q00ZxCQ