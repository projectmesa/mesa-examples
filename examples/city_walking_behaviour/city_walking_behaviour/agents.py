import math
from enum import Enum
from typing import Optional

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
    """Encapsulates all walking decisions for a human agent, including distance checks."""

    DAILY_PROBABILITIES = {
        ActivityType.GROCERY: 0.25,  # Every 4 days on average
        ActivityType.NON_FOOD_SHOPPING: 0.25,
        ActivityType.SOCIAL: 0.15,
        ActivityType.LEISURE: 0.20,
    }

    BASE_MAX_DISTANCES = {
        ActivityType.WORK: 2000,  # meters
        ActivityType.GROCERY: 1000,
        ActivityType.NON_FOOD_SHOPPING: 1500,
        ActivityType.SOCIAL: 2000,
        ActivityType.LEISURE: 3000,
    }

    def __init__(self, model: Model):
        self.model = model
        self.total_distance_walked = 0

    def reset_daily_distance(self):
        """Reset the total distance walked for a new day"""
        self.total_distance_walked = 0

    def add_distance(self, distance: float):
        """Add distance to total daily walking distance"""
        self.total_distance_walked += distance

    def get_max_walking_distance(self, human, activity: ActivityType) -> float:
        """Calculate person-specific maximum walking distance"""
        return self.BASE_MAX_DISTANCES[activity] * human.walking_ability

    def calculate_distance(self, cell1, cell2) -> float:
        """Calculate distance between two cells"""
        x1, y1 = cell1.coordinate
        x2, y2 = cell2.coordinate
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def decide_walk_to_work(self, human) -> bool:
        """Decide if person walks to work"""
        if not human.is_working or not human.workplace:
            return False

        distance = self.calculate_distance(human.cell, human.workplace.cell)
        max_distance = self.get_max_walking_distance(human, ActivityType.WORK)

        if distance <= max_distance:
            return self.model.random.random() <= human.walking_attitude
        return False

    def find_nearest_location(
        self, human, activity_type: ActivityType, search_workplace: bool = True
    ) -> Optional[FixedAgent]:
        """Find nearest location of given type within walking distance"""
        if activity_type == ActivityType.GROCERY:
            locations = self.model.agents_by_type[GroceryStore]
        elif activity_type == ActivityType.NON_FOOD_SHOPPING:
            locations = self.model.agents_by_type[NonFoodShop]
        elif activity_type == ActivityType.SOCIAL:
            locations = self.model.agents_by_type[SocialPlace]
        else:
            return None

        max_distance = self.get_max_walking_distance(human, activity_type)

        # Check locations near home
        nearest = min(
            locations,
            key=lambda loc: self.calculate_distance(human.cell, loc.cell),
            default=None,
        )
        if (
            nearest
            and self.calculate_distance(human.cell, nearest.cell) <= max_distance
        ):
            return nearest

        # Check locations near workplace if applicable
        if search_workplace and human.workplace:
            nearest = min(
                locations,
                key=lambda loc: self.calculate_distance(human.workplace.cell, loc.cell),
                default=None,
            )
            if (
                nearest
                and self.calculate_distance(human.workplace.cell, nearest.cell)
                <= max_distance
            ):
                return nearest

        return None

    def decide_leisure_walk(self, human) -> Optional[tuple[float, float]]:
        """Decide if person takes a leisure walk"""
        if (
            self.model.random.random()
            > self.DAILY_PROBABILITIES[ActivityType.LEISURE] * human.walking_attitude
        ):
            return None

        max_distance = self.get_max_walking_distance(human, ActivityType.LEISURE)
        min_distance = max_distance * 0.75

        # Generate random point within 75-100% of max walking distance
        random_cells = []
        all_cells = self.model.grid.all_cells.cells
        if len(all_cells) == 0:
            return None
        for cell in all_cells:
            if (
                self.calculate_distance(cell, human.cell) <= max_distance
                and self.calculate_distance(cell, human.cell) >= min_distance
            ):
                random_cells.append(cell)

        if len(random_cells) == 0:
            return None
        return self.model.random.choice(random_cells)

    def simulate_daily_walks(self, human):
        """Simulate a full day of possible walks for the agent."""
        walks = []

        # Work walk
        if self.decide_walk_to_work(human):
            distance = self.calculate_distance(human.cell, human.workplace.cell)
            self.add_distance(distance)
            walks.append((ActivityType.WORK, human.workplace))

        # Basic needs walks
        for activity in [ActivityType.GROCERY, ActivityType.NON_FOOD_SHOPPING]:
            if self.model.random.random() <= self.DAILY_PROBABILITIES[activity]:
                destination = self.find_nearest_location(human, activity)
                if destination and self.model.random.random() <= human.walking_attitude:
                    distance = self.calculate_distance(human.cell, destination.cell)
                    self.add_distance(distance)
                    walks.append((activity, destination))

        # Social visit
        if self.model.random.random() <= self.DAILY_PROBABILITIES[ActivityType.SOCIAL]:
            social_place = self.model.random.choice(
                self.model.agents_by_type[SocialPlace]
            )
            distance = self.calculate_distance(human.cell, social_place.cell)
            if (
                distance <= self.get_max_walking_distance(human, ActivityType.SOCIAL)
                and self.model.random.random() <= human.walking_attitude
            ):
                self.add_distance(distance)
                walks.append((ActivityType.SOCIAL, social_place))

        # Leisure walk
        leisure_destination = self.decide_leisure_walk(human)
        if leisure_destination:
            distance = self.calculate_distance(human.cell, leisure_destination)
            self.add_distance(distance)
            walks.append((ActivityType.LEISURE, leisure_destination))

        return walks


class Human(CellAgent):
    """Represents a person with specific attributes and daily walking behavior."""

    def __init__(self, model: Model, unique_id: int = 0, cell=None, SES: int = 0):
        super().__init__(model)
        self.cell = cell
        self.unique_id = unique_id
        self.SES = SES

        # Human Attributes
        self.gender = self.model.generate_gender()
        self.age = self.model.generate_age()
        self.family_size = self.model.generate_family_size()
        self.has_dog = self.model.generate_dog_ownership()
        self.walking_ability = self.get_walking_ability()
        self.walking_attitude = self.get_walking_attitude()
        self.is_working = self._determine_working_status()
        self.workplace = self.get_workplace()
        self.friends = self.get_friends()
        self.family = self.get_family()

        self.previous_walking_density: float = 0
        self.current_walking_density: float

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
        return self.model.random.random() < WORKING_PROBABILITY

    def get_friends(self) -> AgentSet:
        friend_count = self.model.random.randint(MIN_FRIENDS, MAX_FRIENDS)
        friend_set = AgentSet.select(
            self.model.agents_by_type[Human],
            lambda x: (x.SES > self.SES - 1 and x.SES < self.SES + 1)
            and x.unique_id != self.unique_id,
            at_most=friend_count,
        )
        if len(friend_set) > 0:
            for friend in friend_set:
                friend.friends.add(self)
        return friend_set

    def get_family(self) -> AgentSet:
        if self.family_size > 1:
            family_set = AgentSet.select(
                self.model.agents_by_type[Human],
                lambda x: x.gender != self.gender
                and abs(x.age - self.age) <= 3,  # age difference no more than 3 years
                at_most=1,
            )
            if len(family_set) > 0:
                family_set[0].family = AgentSet([self], random=self.model.random)
            return family_set
        else:
            return None

    def get_workplace(self) -> Optional[Workplace | FixedAgent]:
        if not self.is_working:
            return None
        return self.model.random.choice(self.model.agents_by_type[GroceryStore])

    def get_walking_ability(
        self,
    ) -> float:  # Method from https://pmc.ncbi.nlm.nih.gov/articles/PMC3306662/
        random_component = self.model.random.random() ** 4
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
        return self.model.random.random() ** 3

    def get_feedback(self, activity: ActivityType):
        a: float = 0.001  # attitude factor

        # 1. Walking attitudes of family members and friends
        if self.family:
            self.walking_attitude = ((1 - a) * self.walking_attitude) + (
                a * self.family[0].walking_attitude
            )

        if self.friends:
            cumulative_friends_attitude: float = 0  # Initialize to 0
            for friend in self.friends:
                cumulative_friends_attitude += friend.walking_attitude
            # Average the friends' attitudes if there are any
            if len(self.friends) > 0:
                cumulative_friends_attitude /= len(self.friends)
            self.walking_attitude = ((1 - a) * self.walking_attitude) + (
                a * cumulative_friends_attitude
            )

        # 2. Person's walking experience
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

        # 3. Density of other walkers
        neighbour_cells = self.cell.get_neighborhood(radius=2)
        num_neighbours = [i for i in neighbour_cells if i.agents]
        self.current_walking_density = len(num_neighbours) / len(neighbour_cells)
        density_feedback = 0
        if self.previous_walking_density == 0:
            # If previous density was zero, treat any current density as a positive change
            density_feedback = 1 if self.current_walking_density > 0 else 0
        else:
            density_ratio = self.current_walking_density / self.previous_walking_density
            density_feedback = density_ratio - 1  # Centers the feedback around 0

        self.previous_walking_density = self.current_walking_density

        # 4. Total amount walked by the person during that day
        walking_feedback = 0
        if self.walking_behavior.total_distance_walked > 0:
            max_personal_distance = (
                self.walking_behavior.get_max_walking_distance(self, activity)
                * self.walking_ability
            )
            walking_feedback = min(
                1, max_personal_distance / self.walking_behavior.total_distance_walked
            )

        # Update walking attitude
        self.walking_attitude = (
            self.walking_attitude
            * (1 - a + (a * SE_index))
            * (1 - a + (a * density_feedback))
            * (1 - a + (a * walking_feedback))
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
                if activity in [ActivityType.GROCERY, ActivityType.NON_FOOD_SHOPPING]
            ]
        )
        self.leisure_trips = sum(
            [1 for activity, _ in daily_walks if activity == ActivityType.LEISURE]
        )

        if len(daily_walks) > 0:
            for activity, destination in daily_walks:
                self.get_feedback(activity)
                # Move agent to new cell if applicable
                if isinstance(destination, FixedAgent):
                    self.cell = destination.cell
                elif isinstance(destination, Cell):
                    self.cell = destination
