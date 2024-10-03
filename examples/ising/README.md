# Ising Model

## Summary

The Ising model (or Lenz–Ising model), named after the physicists Ernst Ising and Wilhelm Lenz, is a mathematical model of ferromagnetism in statistical mechanics. The model consists of discrete variables that represent magnetic dipole moments of atomic "spins" that can be in one of two states (+1 or −1). The spins are arranged in a graph, usually a lattice (where the local structure repeats periodically in all directions), allowing each spin to interact with its neighbors. Neighboring spins that agree have a lower energy than those that disagree; the system tends to the lowest energy but heat disturbs this tendency, thus creating the possibility of different structural phases. The model allows the identification of phase transitions as a simplified model of reality. The two-dimensional square-lattice Ising model is one of the simplest statistical models to show a phase transition.

## How to Run

To run the model interactively, run ``solara run run.py`` in this directory. e.g.

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press ``run``.

## Things to Try

What happens when the temperature slider is very high? (This is called the "paramagnetic" state.) Try this with different **Spin Up Probability** values.

What happens when the temperature slider is set very low? (This is called the "ferromagnetic" state.) Again, try this with different **Spin Up Probability** values.

Between these two very different behaviors is a transition point. On an infinite grid, the transition point can be proved to be $2 / ln (1 + sqrt 2)$, which is about 2.27. On a large enough finite toroidal grid, the transition point is near this number.

## References

(NetLogo Ising)[https://ccl.northwestern.edu/netlogo/models/Ising]

(Introduction to Monte Carlo methods for an Ising Model of a Ferromagnet)[https://arxiv.org/pdf/0803.0217]
