Ant System for the Traveling Salesman Problem
========================

This is an implementation of the Ant System (AS) algorithm for solving the
Traveling Salesman Problem (TSP).  Individual ants consider both a pheromone
trail laid down by previous ants, the strength of which is proportional to the
solution quality, and a greedy heuristic when choosing its next city.  This
produces an emergent solution as the pheromone trail guides ants to high quality
solutions.

## How to run
To launch the interactive visualization, run `solara run app.py` in this
directory.

Alternatively, to run for a fixed number of iterations, run `python run_tsp.py`
from this directory (and update that file with the parameters you want).


## Algorithm details
Each agent/ant is initialized to a random city and constructs a solution by
choosing a sequence of cities until all are visited, but none are visited more
than once.  Ants then deposit a "pheromone" signal on each path in their
solution that is proportional to 1/d, where d is the final distance traveled by
the solution.  This means shorter paths are given more pheromone.

When an ant is on city $i$ and deciding which city to choose next, it samples
randomly using the following probabilities of transition from city $i$ to $j$:

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

In other words, $\alpha$ and $\beta$ are tuned to set the relative importance
of the phermone trail left by prior ants, and the greedy heuristic of
1-over-distance.


## References
- Original paper:  Dorigo, M., Maniezzo, V., & Colorni, A. (1996). Ant system: optimization by a
colony of cooperating agents. IEEE transactions on systems, man, and cybernetics,
part b (cybernetics), 26(1), 29-41.
- Video series of this code being implemented:  https://www.youtube.com/playlist?list=PLSgGvve8UweGk2TLSO-q5OSH59Q00ZxCQ

