# mesa-examples

This repository contains examples that work with Mesa and illustrate different features of Mesa.

This is the [`mesa-2.x`](https://github.com/projectmesa/mesa-examples/tree/mesa-2.x) legacy branch, with examples that work with Mesa 2.x releases and Mesa-Geo 0.8.x releases.

To contribute to this repository, see [CONTRIBUTING.rst](https://github.com/projectmesa/mesa-examples/blob/main/CONTRIBUTING.rst).

This repo contains a package that readily lets you import and run some of the examples. For Mesa 2.x examples, install:
```console
$ # This will install the "mesa_models" package
$ pip install -U -e git+https://github.com/projectmesa/mesa-examples@mesa-2.x#egg=mesa-models
```
```python
from mesa_models.boltzmann_wealth_model.model import BoltzmannWealthModel
```
You can see the available models at [setup.cfg](https://github.com/projectmesa/mesa-examples/blob/main/setup.cfg).
