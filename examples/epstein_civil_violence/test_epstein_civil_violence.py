import pytest
from epstein_civil_violence.epstein_civil_violence import EpsteinCivilViolence

def test_epstein_civil_violence():
    model = EpsteinCivilViolence(seed=15)
    assert model is not None