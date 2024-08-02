# mesa-examples

This repository contains examples that work with Mesa and illustrate different features of Mesa.

- Mesa examples that work on the Mesa main development branch are available here on the [`main`](https://github.com/projectmesa/mesa-examples) branch.
- Mesa examples that work for Mesa 2.x releases are available here on the [`mesa-2.x`](https://github.com/projectmesa/mesa-examples/tree/mesa-2.x) branch.

To contribute to this repository, see [CONTRIBUTING.rst](https://github.com/projectmesa/mesa-examples/blob/main/CONTRIBUTING.rst).

This repo also contains a package that readily lets you import and run some of the examples:
```console
$ # This will install the "mesa_models" package
$ pip install -U -e git+https://github.com/projectmesa/mesa-examples#egg=mesa-models
```
For Mesa 2.x examples, install:
```console
$ # This will install the "mesa_models" package
$ pip install -U -e git+https://github.com/projectmesa/mesa-examples@mesa-2.x#egg=mesa-models
```
```python
from mesa_models.boltzmann_wealth_model.model import BoltzmannWealthModel
```
You can see the available models at [setup.cfg](https://github.com/projectmesa/mesa-examples/blob/main/setup.cfg).
