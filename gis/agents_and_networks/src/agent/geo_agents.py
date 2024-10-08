import mesa
import mesa_geo as mg
import pyproj
from shapely.geometry import Point


class Driveway(mg.GeoAgent):
    unique_id: int
    model: mesa.Model
    geometry: Point
    crs: pyproj.CRS

    def __init__(self, model, geometry, crs) -> None:
        super().__init__(model, geometry, crs)


class LakeAndRiver(mg.GeoAgent):
    unique_id: int
    model: mesa.Model
    geometry: Point
    crs: pyproj.CRS

    def __init__(self, model, geometry, crs) -> None:
        super().__init__(model, geometry, crs)


class Walkway(mg.GeoAgent):
    unique_id: int
    model: mesa.Model
    geometry: Point
    crs: pyproj.CRS

    def __init__(self, model, geometry, crs) -> None:
        super().__init__(model, geometry, crs)
