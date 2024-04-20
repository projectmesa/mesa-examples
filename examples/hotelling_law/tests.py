from .hotelling_law.model import HotellingModel
from scipy.stats import linregress


def check_slope(data, increasing=True):
    """Checks the slope of a dataset to determine
            if it's increasing or decreasing."""
    slope = get_slope(data)
    return (slope > 0) if increasing else (slope < 0)


def get_slope(data):
    slope, _, _, _, _ = linregress(range(len(data)), data)
    print(slope)
    return slope


def test_decreasing_price_variance():
    """Test to ensure the price variance decreases over time,
    in line with Hotelling's law."""
    model = HotellingModel(
        N_stores=5,
        width=20,
        height=20,
        mode="default",
        consumer_preferences="default",
        environment_type="grid",
        mobility_rate=80,
    )
    model.run_model(step_count=50)

    df_model = model.datacollector.get_model_vars_dataframe()

    assert check_slope(
        df_model["Price Variance"], increasing=False
    ), "The price variance should decrease over time."


def test_constant_price_variance():
    """Test to ensure the price variance constant over time,
    with Rules location_only without changing price"""
    model = HotellingModel(
        N_stores=5,
        width=20,
        height=20,
        mode="location_only",
        consumer_preferences="default",
        environment_type="grid",
        mobility_rate=80,
    )
    model.run_model(step_count=50)

    df_model = model.datacollector.get_model_vars_dataframe()

    assert get_slope(
        df_model["Price Variance"]
    ) == 0, "The price variance constant over time."
