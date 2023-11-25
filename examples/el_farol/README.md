# El Farol

This folder contains an implementation of El Farol restaurant model. Agents (restaurant customers) decide whether to go to the restaurant or not based on their memory and reward from previous trials. Implications from the model have been used to explain how individual decision-making affects overall performance and fluctuation.

The implementation is based on Fogel 1999 (in particular the calculation of the prediction), which is a refinement over Arthur 1994.

## How to Run

Launch the model: You can run the model and perform analysis in el_farol.ipynb.
You can test the model itself by running `pytest tests.py`.

## Files
* [el_farol.ipynb](el_farol.ipynb): Run the model and visualization in a Jupyter notebook
* [el_farol/model.py](el_farol/model.py): Core model file.
* [el_farol/agents.py](el_farol/agents.py): The agent class.
* [tests.py](tests.py): Tests to ensure the model is consistent with Arthur 1994, Fogel 1996.

## Further Reading

1. W. Brian Arthur Inductive Reasoning and Bounded Rationality (1994) https://www.jstor.org/stable/2117868
1. D.B. Fogel, K. Chellapilla, P.J. Angeline Inductive reasoning and bounded rationality reconsidered (1999)
1. NetLogo implementation of the El Farol bar problem https://ccl.northwestern.edu/netlogo/models/ElFarol
