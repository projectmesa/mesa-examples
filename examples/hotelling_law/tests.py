import pytest
from examples.hotelling_law.model import HotellingModel
from scipy.stats import linregress


def check_slope(data, increasing=True):
    """Checks the slope of a dataset to determine
    if it's increasing or decreasing."""
    slope, _, _, _, _ = linregress(range(len(data)), data)
    return (slope > 0) if increasing else (slope < 0)


def test_decreasing_price_variance():
    """Test to ensure the price variance decreases over time,
    in line with Hotelling's law."""
    model = HotellingModel(N=10, width=20, height=20, mode="default", environment_type="grid", mobility_rate=80)
    model.run_model(step_count=50)

    df_model = model.datacollector.get_model_vars_dataframe()

    assert check_slope(df_model['Price Variance'], increasing=False), "The price variance should decrease over time."
