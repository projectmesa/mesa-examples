# mesa-examples

This repository contains examples that work with Mesa and illustrate different features of Mesa.

To contribute to this repository, see [CONTRIBUTING.rst](https://github.com/projectmesa/mesa-examples/blob/main/CONTRIBUTING.rst).

This repo also contains a package that readily lets you import and run some of the examples:
```console
$ # This will install the "mesa_models" package
$ pip install -U -e git+https://github.com/projectmesa/mesa-examples#egg=mesa-models
```
```python
from mesa_models.boltzmann_wealth_model.model import BoltzmannWealthModel
```
You can see the available models at [setup.cfg](https://github.com/projectmesa/mesa-examples/blob/main/setup.cfg).

The package also contains experimental code, which will be in the main Mesa package once they have stabilized.
You can see an example of the `JupyterViz` function in the experimental boltzmann wealth model's [app.py](https://github.com/projectmesa/mesa-examples/blob/main/examples/boltzmann_wealth_model_experimental/app.py).
