import math
from collections import defaultdict
from enum import Enum
from functools import lru_cache
from typing import List, Optional, Tuple

import numpy as np
from mesa import Model
from mesa.agent import AgentSet
from mesa.experimental.cell_space import Cell, CellAgent, FixedAgent

# Constants for probability values
FEMALE_PROBABILITY = 0.5
DOG_OWNER_PROBABILITY = 0.2
SINGLE_HOUSEHOLD_PROBABILITY = 0.2
MIN_AGE = 18
MAX_AGE = 87
MIN_FRIENDS = 3
MAX_FRIENDS = 5
WORKING_PROBABILITY = 0.95
RETIREMENT_AGE = 69


class ActivityType(Enum):
    WORK = "work"
    GROCERY = "grocery"
    NON_FOOD_SHOPPING = "shopping"
    SOCIAL = "social"
    LEISURE = "leisure"


class Workplace:
    """Generic workplace base class."""

    def __init__(self, store_type: str):
        self.store_type = store_type


class GroceryStore(Workplace, FixedAgent):
    def __init__(self, model: Model, cell=None):
        Workplace.__init__(self, store_type="Grocery Store")
        FixedAgent.__init__(self, model)
        self.cell = cell


class NonFoodShop(Workplace, FixedAgent):
    def __init__(self, model: Model, cell=None):
        Workplace.__init__(self, store_type="Non-Food Shop")
        FixedAgent.__init__(self, model)
        self.cell = cell


class SocialPlace(Workplace, FixedAgent):
    def __init__(self, model: Model, cell=None):
        Workplace.__init__(self, store_type="Social Place")
        FixedAgent.__init__(self, model)
        self.cell = cell


class Other(Workplace, FixedAgent):
    def __init__(self, model: Model, cell=None):
        Workplace.__init__(self, store_type="Other")
        FixedAgent.__init__(self, model)
        self.cell = cell


class WalkingBehaviorModel:
    """Optimized walking behavior model with spatial caching and early termination."""

    MILES_TO_METERS = 1609.34
    DAILY_PROBABILITIES = {
        ActivityType.GROCERY: 0.4,
        ActivityType.NON_FOOD_SHOPPING: 0.25,  # once every 4 days
        ActivityType.SOCIAL: 0.20,
        ActivityType.LEISURE: 0.33,
    }

    BASE_MAX_DISTANCES = {
        ActivityType.WORK: 1.125 * MILES_TO_METERS,  # meters
        ActivityType.GROCERY: 2.000 * MILES_TO_METERS,
        ActivityType.NON_FOOD_SHOPPING: 1.500 * MILES_TO_METERS,
        ActivityType.SOCIAL: 2.500 * MILES_TO_METERS,
        ActivityType.LEISURE: 5.500 * MILES_TO_METERS,
    }

    def __init__(self, model: Model):
        self.model = model
        self.total_distance_walked = 0
        # Spatial index for quick location lookup
        self._location_cache = {}
        self._distance_cache = {}
        # Maximum possible walking distance for any activity
        self._max_possible_distance = max(self.BASE_MAX_DISTANCES.values())

    def reset_daily_distance(self) -> None:
        """Reset daily walking distance."""
        self.total_distance_walked = 0

    def add_distance(self, distance: float) -> None:
        """Add to total daily walking distance."""
        self.total_distance_walked += distance

    @lru_cache(maxsize=1024)  # noqa
    def get_max_walking_distance(self, ability: float, activity: ActivityType) -> float:
        """Cached calculation of max walking distance based on ability."""
        return self.BASE_MAX_DISTANCES[activity] * ability

    @staticmethod
    @lru_cache(maxsize=4096)
    def calculate_distance(x1: int, y1: int, x2: int, y2: int) -> float:
        """Cached distance calculation between two points."""
        dx = x2 - x1
        dy = y2 - y1
        return math.sqrt(dx * dx + dy * dy)

    def get_distance(self, cell1, cell2) -> float:
        """Get distance between cells using cache."""
        key = (cell1, cell2)
        if key not in self._distance_cache:
            x1, y1 = cell1.coordinate
            x2, y2 = cell2.coordinate
            self._distance_cache[key] = self.calculate_distance(x1, y1, x2, y2)
        return self._distance_cache[key]

    def decide_walk_to_work(self, human) -> bool:
        """Optimized work walk decision."""
        if not (human.is_working and human.workplace):
            return False

        distance = self.get_distance(human.household, human.workplace.cell)
        max_distance = self.get_max_walking_distance(
            human.walking_ability, ActivityType.WORK
        )

        return (
            distance <= max_distance
            and self.model.random.random() <= human.walking_attitude
        )

    def _build_location_cache(self, activity_type: ActivityType) -> None:
        """Build spatial index for locations of given type."""
        if activity_type not in self._location_cache:
            locations = defaultdict(list)
            if activity_type == ActivityType.GROCERY:
                agents = self.model.agents_by_type[GroceryStore]
            elif activity_type == ActivityType.NON_FOOD_SHOPPING:
                agents = self.model.agents_by_type[NonFoodShop]
            elif activity_type == ActivityType.SOCIAL:
                agents = self.model.agents_by_type[SocialPlace]
            else:
                return

            # Group locations by grid sectors for faster lookup
            sector_size = int(self._max_possible_distance)
            for agent in agents:
                x, y = agent.cell.coordinate
                sector_x = x // sector_size
                sector_y = y // sector_size
                locations[(sector_x, sector_y)].append(agent)

            self._location_cache[activity_type] = locations

    def find_walkable_locations(self, human, activity_type: ActivityType) -> List:
        """Find walkable locations using spatial indexing."""
        self._build_location_cache(activity_type)
        max_distance = self.get_max_walking_distance(
            human.walking_ability, activity_type
        )

        walkable = []
        locations = self._location_cache.get(activity_type, {})

        # Helper function to check locations near a reference point
        def check_near_point(ref_point):
            x, y = ref_point.coordinate
            sector_size = int(self._max_possible_distance)
            sector_x = x // sector_size
            sector_y = y // sector_size

            # Check nearby sectors only
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    sector = (sector_x + dx, sector_y + dy)
                    for location in locations.get(sector, []):
                        if self.get_distance(ref_point, location.cell) <= max_distance:
                            walkable.append(location)
            return bool(walkable)

        # Check household first
        if check_near_point(human.household):
            return walkable

        # If no locations found and person is working, check workplace
        if human.is_working and human.workplace:
            check_near_point(human.workplace.cell)

        return walkable

    def get_leisure_cells(self, human) -> List[Cell]:
        """
        Get valid leisure walk destinations.
        """
        if not human or not human.household:
            return []

        # Calculate distances based on walking ability
        max_distance = self.get_max_walking_distance(
            human.walking_ability, ActivityType.LEISURE
        )
        # Set minimum distance to 75% of max distance
        min_distance = max_distance * 0.75

        household_x, household_y = human.household.coordinate
        valid_cells = []

        for cell in self.model.grid.all_cells.cells:
            x, y = cell.coordinate

            # Quick boundary check
            if (
                abs(x - household_x) > max_distance
                or abs(y - household_y) > max_distance
            ):
                continue

            # Calculate exact distance
            dist = self.calculate_distance(household_x, household_y, x, y)
            if min_distance <= dist <= max_distance:
                valid_cells.append(cell)

                if len(valid_cells) >= 200:
                    return valid_cells

        return valid_cells

    def decide_leisure_walk(self, human) -> Optional[Cell]:
        """
        Leisure walk decision making.
        """
        base_probability = self.DAILY_PROBABILITIES[ActivityType.LEISURE]

        # Consider additional factors that might encourage walking
        motivation_factors = 1.0
        if human.has_dog:  # Dog owners are more likely to take leisure walks
            motivation_factors += 0.3
        if not human.is_working:  # Non-working individuals have more time
            motivation_factors += 0.2

        # Final probability calculation
        probability = base_probability * human.walking_attitude * motivation_factors

        if self.model.random.random() > probability:
            return None

        valid_cells = self.get_leisure_cells(human)
        if not valid_cells:
            return None

        return self.model.random.choice(valid_cells)

    def simulate_daily_walks(self, human) -> List[Tuple]:
        """Optimized daily walk simulation."""
        walks = []
        random = self.model.random.random

        # Work walk
        if self.decide_walk_to_work(human):
            distance = self.get_distance(human.household, human.workplace.cell)
            self.add_distance(distance)
            walks.append((ActivityType.WORK, human.workplace))

        # Basic needs walks
        for activity in (ActivityType.GROCERY, ActivityType.NON_FOOD_SHOPPING):
            if random() <= self.DAILY_PROBABILITIES[activity]:
                walkable = self.find_walkable_locations(human, activity)
                if walkable and random() <= human.walking_attitude:
                    destination = self.model.random.choice(walkable)
                    distance = self.get_distance(human.household, destination.cell)
                    self.add_distance(distance)
                    walks.append((activity, destination))

        # Social visit
        if random() <= self.DAILY_PROBABILITIES[ActivityType.SOCIAL]:
            social_place = self.model.random.choice(
                self.model.agents_by_type[SocialPlace]
            )
            max_distance = self.get_max_walking_distance(
                human.walking_ability, ActivityType.SOCIAL
            )

            household_distance = self.get_distance(human.household, social_place.cell)
            workplace_distance = float("inf")
            if human.is_working and human.workplace:
                workplace_distance = self.get_distance(
                    human.workplace.cell, social_place.cell
                )

            min_distance = min(household_distance, workplace_distance)
            if min_distance <= max_distance and random() <= human.walking_attitude:
                self.add_distance(min_distance)
                walks.append((ActivityType.SOCIAL, social_place))

        # Leisure walk
        leisure_destination = self.decide_leisure_walk(human)
        if leisure_destination:
            distance = self.get_distance(human.household, leisure_destination)
            self.add_distance(distance)
            walks.append((ActivityType.LEISURE, leisure_destination))

        return walks

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the WalkingBehaviorModel.

        Returns:
            str: String showing model state including caches and distances
        """
        cache_stats = {
            "location_cache_size": sum(
                len(locations) for locations in self._location_cache.values()
            ),
            "distance_cache_size": len(self._distance_cache),
            "leisure_cache_size": len(getattr(self, "_leisure_cells_cache", {})),
        }

        return (
            f"WalkingBehaviorModel("
            f"total_distance_walked={self.total_distance_walked:.2f}, "
            f"max_possible_distance={self._max_possible_distance}, "
            f"cache_sizes={cache_stats}, "
            f"daily_probabilities={len(self.DAILY_PROBABILITIES)} activities)"
        )


class Human(CellAgent):
    """Represents a person with specific attributes and daily walking behavior."""

    def __init__(
        self,
        model: Model,
        gender: Optional[int] = None,
        family_size: Optional[int] = None,
        age: Optional[int] = None,
        SES: Optional[int] = None,
        unique_id: int = 0,
        cell=None,
        household: Cell = None,
    ):
        super().__init__(model)
        self.cell = cell
        self.unique_id = unique_id
        self.household = household

        # Human Attributes
        self.gender = gender
        self.age = age
        self.SES = SES
        self.family_size = family_size
        self.has_dog = self.model.generate_dog_ownership()
        self.walking_ability = self.get_walking_ability()
        self.walking_attitude = self.get_walking_attitude()
        self.is_working = self._determine_working_status()
        self.workplace = self.get_workplace()
        self.friends = self.get_friends()
        self.family: Human = None

        self.previous_walking_density: float = 0

        # Datacollector attributes
        self.daily_walking_trips: int = 0
        self.work_trips: int = 0
        self.basic_needs_trips: int = 0
        self.leisure_trips: int = 0

        # Initialize walking behavior
        self.walking_behavior = WalkingBehaviorModel(model)

    def _determine_working_status(self) -> bool:
        if self.age >= RETIREMENT_AGE:
            return False
        return self.random.random() < WORKING_PROBABILITY

    def get_friends(self) -> AgentSet:
        friend_count = self.random.randint(MIN_FRIENDS, MAX_FRIENDS)
        friend_set = AgentSet.select(
            self.model.agents_by_type[Human],
            lambda x: (
                x.SES > self.SES - 2 and x.SES < self.SES + 2
            )  # get friends with similar SES i.e. difference no more than 3
            and x.unique_id != self.unique_id,
            at_most=friend_count,
        )
        if len(friend_set) > 0:
            for friend in friend_set:
                friend.friends.add(self)  # add self to the friends list as well
        return friend_set

    def get_workplace(self) -> Optional[Workplace | FixedAgent]:
        if not self.is_working:
            return None

        # Get all workplaces like grocery stores, non-food shops, social places
        all_workplaces = [
            workplace
            for workplace in self.model.agents
            if not isinstance(workplace, Human)
        ]
        return self.random.choice(all_workplaces)

    def get_walking_ability(
        self,
    ) -> float:  # Method from https://pmc.ncbi.nlm.nih.gov/articles/PMC3306662/
        random_component = self.random.random() ** 4
        if self.age <= 37:
            # For ages up to 37, use the base calculation
            return random_component * (min(abs(137 - self.age), 100) / 100)
        else:
            # For ages over 37, apply linear decrease
            base_ability = random_component * (min(abs(137 - self.age), 100) / 100)
            age_factor = (self.age - 37) / 50  # Linear decrease factor
            return base_ability * (1 - age_factor)

    def get_walking_attitude(
        self,
    ) -> float:  # Method from https://pmc.ncbi.nlm.nih.gov/articles/PMC3306662/
        return self.random.random() ** 3

    def get_feedback(self):
        a: float = 0.001  # attitude factor

        # 1. Social network feedback (family and friends)
        # Store original attitude for use in calculations
        At = self.walking_attitude

        # Family feedback (Equations 1 & 2 in literature)
        if self.family:
            self.walking_attitude = (1 - a) * At + a * self.family.walking_attitude

        # Friends feedback (Equation 3 in literature)
        if self.friends:
            friends_attitude = sum(friend.walking_attitude for friend in self.friends)
            if len(self.friends) > 0:
                friends_attitude /= len(self.friends)
                self.walking_attitude = (1 - a) * At + a * friends_attitude

        # 2. Walking experience feedback (Equation 4 in literature)
        x, y = self.cell.coordinate
        SE_index = (
            (
                self.model.safety_cell_layer.data[x][y]
                + self.model.random.uniform(-0.5, 0.5)
            )
            * (
                self.model.aesthetic_cell_layer.data[x][y]
                + self.model.random.uniform(-0.5, 0.5)
            )
        ) / np.mean(
            self.model.safety_cell_layer.data * self.model.aesthetic_cell_layer.data
        )

        # 3. Density feedback
        # Compare current walking density to previous day
        neighbour_cells = self.cell.get_neighborhood(radius=1)
        current_density = sum(len(cell.agents) for cell in neighbour_cells) / len(
            neighbour_cells
        )

        Id = 0
        if self.previous_walking_density > 0:
            Id = current_density / self.previous_walking_density
        else:
            Id = 1 if current_density > 0 else 0

        self.previous_walking_density = current_density

        # 4. Walking distance feedback (Equation 5 in literature)
        It = 0
        if self.walking_behavior.total_distance_walked > 0:
            Ab_Da = sum(
                [
                    dis * self.walking_ability
                    for dis in self.walking_behavior.BASE_MAX_DISTANCES.values()
                ]
            )
            d = self.walking_behavior.total_distance_walked
            It = min(1, Ab_Da / d)

        # Final attitude update (Equation 6 in literature)
        self.walking_attitude = (
            At * (1 - a + a * SE_index) * (1 - a + a * Id) * (1 - a + a * It)
        )

    def step(self):
        """Execute one simulation step: decide on daily walks, update feedback."""
        daily_walks = self.walking_behavior.simulate_daily_walks(self)

        # Update datacollector attributes
        self.daily_walking_trips = len(daily_walks)
        self.work_trips = sum(
            [1 for activity, _ in daily_walks if activity == ActivityType.WORK]
        )
        self.basic_needs_trips = sum(
            [
                1
                for activity, _ in daily_walks
                if activity
                in [
                    ActivityType.GROCERY,
                    ActivityType.NON_FOOD_SHOPPING,
                    ActivityType.SOCIAL,
                ]
            ]
        )
        self.leisure_trips = sum(
            [1 for activity, _ in daily_walks if activity == ActivityType.LEISURE]
        )

        if len(daily_walks) > 0:
            self.get_feedback()
            for activity, destination in daily_walks:
                # Move agent to new cell if applicable
                if isinstance(destination, FixedAgent):
                    self.cell = destination.cell
                elif isinstance(destination, Cell):
                    self.cell = destination
