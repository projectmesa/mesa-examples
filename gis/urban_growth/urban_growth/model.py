import mesa
import numpy as np

from .space import City


class UrbanGrowth(mesa.Model):
    def __init__(
        self,
        world_width=531,
        world_height=394,
        max_coefficient=100,
        dispersion_coefficient=20,
        spread_coefficient=27,
        breed_coefficient=5,
        rg_coefficient=10,
        slope_coefficient=50,
        critical_slope=25,
        road_influence=False,
    ):
        super().__init__()
        self.world_width = world_width
        self.world_height = world_height
        self.max_coefficient = max_coefficient
        self.dispersion_coefficient = dispersion_coefficient
        self.spread_coefficient = spread_coefficient
        self.breed_coefficient = breed_coefficient
        self.rg_coefficient = rg_coefficient
        self.slope_coefficient = slope_coefficient
        self.critical_slope = critical_slope
        self.road_influence = road_influence
        self.schedule = mesa.time.RandomActivation(self)

        self.dispersion_value = (dispersion_coefficient * 0.005) * (
            world_width**2 + world_height**2
        ) ** 0.5
        self.rg_value = (
            rg_coefficient / max_coefficient * ((world_width + world_height) / 16.0)
        )
        self.max_search = 4 * (self.rg_value * (1 + self.rg_value))

        self._load_data()
        self._check_suitability()
        self.space.check_road()
        for cell in self.space.raster_layer:
            if cell.road:
                cell.run_value = cell.road_1 / 4 * self.dispersion_coefficient
            cell.road_found = False
            cell.road_pixel = None
            cell.model = self
            self.schedule.add(cell)

        self.initialize_data_collector(
            model_reporters={"Percentage Urbanized": "pct_urbanized"}
        )

    @property
    def pct_urbanized(self) -> float:
        total_urban = sum([cell.urban for cell in self.space.raster_layer])
        return total_urban / (self.world_width * self.world_height) * 100.0

    def _load_data(self) -> None:
        self.space = City(
            width=self.world_width,
            height=self.world_height,
            crs="epsg:3857",
            total_bounds=[-901575.0, 1442925.0, -885645.0, 1454745.0],
        )
        self.space.load_datasets(
            urban_data="data/urban_santafe.asc.gz",
            slope_data="data/slope_santafe.asc.gz",
            road_data="data/road1_santafe.asc.gz",
            excluded_data="data/excluded_santafe.asc.gz",
            land_use_data="data/landuse_santafe.asc.gz",
        )

    def _check_suitability(self) -> None:
        max_slope = max([cell.slope for cell in self.space.raster_layer])

        prob_to_build = []

        i = 0
        while i <= self.critical_slope:
            i += 1
            val = (self.critical_slope - i) / self.critical_slope
            prob_to_build.append(val ** (self.slope_coefficient / 200))

        j = 1
        while j <= (max_slope - self.critical_slope):
            prob_to_build.append(0)
            j += 1

        pct_suitable = 0

        for cell in self.space.raster_layer:
            if (
                int(cell.slope) != -9999
                and np.random.uniform() >= prob_to_build[int(cell.slope)]
            ) or (cell.excluded == 0.0):
                cell.suitable = False
            else:
                cell.suitable = True
                pct_suitable += 1

        pct_suitable = pct_suitable / (self.world_width * self.world_height) * 100

    def step(self):
        self._spontaneous_growth()
        self.schedule.step()
        if self.road_influence:
            self._road_influenced_growth()
        self.datacollector.collect(self)

    def _spontaneous_growth(self) -> None:
        i = 0
        while i < self.dispersion_value:
            i += 1
            w = np.random.randint(self.world_width)
            h = np.random.randint(self.world_height)
            random_cell = self.space.raster_layer.cells[w][h]
            if (not random_cell.urban) and random_cell.suitable:
                random_cell.urban = True
                random_cell.new_urbanized = True

    def _road_influenced_growth(self) -> None:
        pass
