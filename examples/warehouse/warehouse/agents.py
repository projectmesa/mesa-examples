"""Agents used by warehouse meta-agent example."""

from __future__ import annotations

from queue import PriorityQueue

import mesa
from mesa.discrete_space import FixedAgent


class InventoryAgent(FixedAgent):
    """Represents an inventory item in the warehouse."""

    def __init__(self, model, cell, item: str):
        super().__init__(model)
        self.cell = cell
        self.item = item
        self.quantity = 1000


class RouteAgent(mesa.Agent):
    """Handle path finding for the warehouse robots."""

    def __init__(self, model):
        super().__init__(model)

    def find_path(self, start, goal) -> list[tuple[int, int, int]] | None:
        """Find a path from ``start`` to ``goal`` using A* search."""

        def heuristic(a, b) -> int:
            dx = abs(a[0] - b[0])
            dy = abs(a[1] - b[1])
            return dx + dy

        open_set = PriorityQueue()
        open_set.put((0, start.coordinate))
        came_from = {}
        g_score = {start.coordinate: 0}

        while not open_set.empty():
            _, current = open_set.get()

            if current[:2] == goal.coordinate[:2]:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                path.insert(0, start.coordinate)
                path.pop()
                return path

            for n_cell in self.model.warehouse[current].neighborhood:
                coord = n_cell.coordinate

                # Only consider orthogonal neighbors in x/y plane.
                if abs(coord[0] - current[0]) + abs(coord[1] - current[1]) != 1:
                    continue

                tentative_g_score = g_score[current] + 1
                if not n_cell.is_empty:
                    tentative_g_score += 50

                if coord not in g_score or tentative_g_score < g_score[coord]:
                    g_score[coord] = tentative_g_score
                    f_score = tentative_g_score + heuristic(coord, goal.coordinate)
                    open_set.put((f_score, coord))
                    came_from[coord] = current

        return None


class SensorAgent(mesa.Agent):
    """Detect obstacles and move the robot along a computed path."""

    def __init__(self, model):
        super().__init__(model)

    def move(
        self, coord: tuple[int, int, int], path: list[tuple[int, int, int]]
    ) -> str:
        """Move one step along the current path."""
        # Backend-authoritative lookup: sensor -> robot via groups_of
        robot = next(iter(self.model.meta_agents.groups_of(self)), self)

        if coord not in path:
            raise ValueError("Current coordinate not in path.")

        idx = path.index(coord)
        if idx + 1 >= len(path):
            return "movement complete"

        next_cell = self.model.warehouse[path[idx + 1]]
        if next_cell.is_empty:
            robot.cell = next_cell  # type: ignore[attr-defined]
            return "moving"

        neighbors = self.model.warehouse[robot.cell.coordinate].neighborhood  # type: ignore[attr-defined]
        empty_neighbors = [n for n in neighbors if n.is_empty]
        if empty_neighbors:
            robot.cell = self.random.choice(empty_neighbors)  # type: ignore[attr-defined]

        # Recalculate via typed router member
        router = next(
            iter(self.model.meta_agents.members_of(robot, relation="router")), None
        )
        if router is None or getattr(robot, "item", None) is None:
            return "recalculating"
        new_path = router.find_path(robot.cell, robot.item.cell)  # type: ignore[attr-defined]
        robot.path = new_path  # type: ignore[attr-defined]
        return "recalculating"


class WorkerAgent(mesa.Agent):
    """Handle inventory pickup and delivery to the loading dock."""

    def __init__(self, model, ld, cs):
        super().__init__(model)
        self.loading_dock = ld
        self.charging_station = cs
        self.path: list[tuple[int, int, int]] | None = None
        self.carrying: str | None = None
        self.item: InventoryAgent | None = None

    def initiate_task(self, item: InventoryAgent):
        """Start a new inventory task."""
        robot = next(iter(self.model.meta_agents.groups_of(self)), self)
        # Typed lookup for router to build path
        router = next(
            iter(self.model.meta_agents.members_of(robot, relation="router")), None
        )
        robot.item = item  # type: ignore[attr-defined]
        if router is not None:
            robot.path = router.find_path(robot.cell, item.cell)  # type: ignore[attr-defined]
        else:
            # fallback: router capability assumed on robot via meta_methods
            robot.path = robot.find_path(robot.cell, item.cell)  # type: ignore[attr-defined]

    def continue_task(self):
        """Continue the current task if the robot has one."""
        robot = next(iter(self.model.meta_agents.groups_of(self)), self)
        if getattr(robot, "path", None) is None or getattr(robot, "item", None) is None:
            return

        sensor = next(
            iter(self.model.meta_agents.members_of(robot, relation="sensor")), None
        )
        if sensor is not None:
            status = sensor.move(robot.cell.coordinate, robot.path)  # type: ignore[arg-type]
        else:
            # fallback to robot's own move (wired via meta_methods)
            status = robot.move(robot.cell.coordinate, robot.path)  # type: ignore[attr-defined]

        if (
            status == "movement complete"
            and getattr(robot, "status", None) == "inventory"
        ):
            source_coordinate = robot.cell.coordinate  # type: ignore[attr-defined]
            target_level = robot.item.cell.coordinate[2]  # type: ignore[attr-defined]
            robot.cell = self.model.warehouse[  # type: ignore[attr-defined]
                (source_coordinate[0], source_coordinate[1], target_level)
            ]
            robot.status = "loading"  # type: ignore[attr-defined]
            robot.carrying = robot.item.item  # type: ignore[attr-defined]
            robot.item.quantity -= 1  # type: ignore[attr-defined]

            loading_coordinate = robot.cell.coordinate  # type: ignore[attr-defined]
            robot.cell = self.model.warehouse[  # type: ignore[attr-defined]
                (loading_coordinate[0], loading_coordinate[1], 0)
            ]
            # Recompute path to loading dock via router or robot
            router = next(
                iter(self.model.meta_agents.members_of(robot, relation="router")), None
            )
            if router is not None:
                robot.path = router.find_path(robot.cell, robot.loading_dock)  # type: ignore[attr-defined]
            else:
                robot.path = robot.find_path(robot.cell, robot.loading_dock)  # type: ignore[attr-defined]

        if (
            status == "movement complete"
            and getattr(robot, "status", None) == "loading"
        ):
            robot.carrying = None  # type: ignore[attr-defined]
            robot.status = "open"  # type: ignore[attr-defined]
            robot.path = None  # type: ignore[attr-defined]
            robot.item = None  # type: ignore[attr-defined]
