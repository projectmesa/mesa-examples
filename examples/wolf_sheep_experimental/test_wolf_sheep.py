from wolf_sheep.wolf_sheep import WolfSheep


def test_wolf_sheep():
    model = WolfSheep(seed=15)
    assert model is not None
