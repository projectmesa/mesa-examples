import importlib
import os

import pytest
from mesa import Model


def get_models(directory):
    models = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == "model.py":
                module_name = os.path.relpath(os.path.join(root, file[:-3])).replace(
                    os.sep, "."
                )

                module = importlib.import_module(module_name)
                for item in dir(module):
                    obj = getattr(module, item)
                    if (
                        isinstance(obj, type)
                        and issubclass(obj, Model)
                        and obj is not Model
                    ):
                        models.append(obj)

    return models


@pytest.mark.parametrize("model_class", get_models("examples"))
def test_model_steps(model_class):
    model = model_class()  # Assume no arguments are needed
    for _ in range(10):
        model.step()


def get_batch_scripts():
    return [
        'examples.bank_reserves.batch_run',
        'examples.sugarscape_g1mt.run'
    ]


@pytest.mark.parametrize("script_module", get_batch_scripts())
def test_batch_run(script_module):
    module = importlib.import_module(script_module)
    module.main()  # Call the main function
