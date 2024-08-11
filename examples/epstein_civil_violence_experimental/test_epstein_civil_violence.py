import unittest
from model import EpsteinCivilViolence


class TestEpsteinCivilViolence(unittest.TestCase):
    def setUp(self):
        self.model = EpsteinCivilViolence(seed=15)

    def test_initialization(self):
        self.assertEqual(self.model.width, 40)
        self.assertEqual(self.model.height, 40)
        self.assertEqual(self.model.citizen_density, 0.7)
        self.assertEqual(self.model.cop_density, 0.074)

    def test_step(self):
        self.model.step()
        # Add assertions to test the behavior of the model after a step


if __name__ == "__main__":
    unittest.main()
