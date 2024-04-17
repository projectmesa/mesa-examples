from hotelling_law.model import HotellingModel
from scipy.stats import linregress


def check_slope(data, increasing=True):
    """Checks the slope of a dataset to determine
    if it's increasing or decreasing."""
    slope, _, _, _, _ = linregress(range(len(data)), data)
    return (slope > 0) if increasing else (slope < 0)


def test_price_variance_behavior(expected_to_increase=True):
    """Test to ensure the price variance behaves as expected over time.

    Parameters:
    - expected_to_increase (bool):
    True if the price variance is expected to increase over time,
    False if it is expected to decrease.
    """
    model = HotellingModel(
        N=10,
        width=20,
        height=20,
        mode="default",
        environment_type="grid",
        mobility_rate=80,
    )
    model.run_model(step_count=50)

    df_model = model.datacollector.get_model_vars_dataframe()

    # Checking if the slope of the price variance is as expected
    if expected_to_increase:
        assert check_slope(df_model["Price Variance"],
                           increasing=True), \
            "The price variance should increase over time, but it did not."
    else:
        assert check_slope(df_model["Price Variance"],
                           increasing=False), \
            "The price variance should decrease over time, but it did not."
