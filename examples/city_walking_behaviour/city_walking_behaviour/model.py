import math

from agents import (
    DOG_OWNER_PROBABILITY,
    FEMALE_PROBABILITY,
    MAX_AGE,
    MIN_AGE,
    SINGLE_HOUSEHOLD_PROBABILITY,
    GroceryStore,
    Human,
    NonFoodShop,
    Other,
    SocialPlace,
)
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.experimental.cell_space import OrthogonalVonNeumannGrid
from mesa.experimental.cell_space.property_layer import PropertyLayer
from mesa.experimental.devs import ABMSimulator

SCENARIOS = {
    "random_random": "Random Land Use, Random Safety",
    "random_safe": "Random Land Use, Low Safety in Core",
    "central_random": "Centralized Land Use, Random Safety",
    "central_safe": "Centralized Land Use, Low Safety in Core",
}


class WalkingModel(Model):
    def __init__(
        self,
        height: int = 40,
        width: int = 40,
        no_of_couples: int = 2400,
        no_of_singles: int = 600,
        no_of_grocery_stores: int = 10,
        no_of_social_places: int = 75,
        no_of_non_food_shops: int = 40,
        no_of_others: int = 475,
        scenario: str = "random_random",
        seed=None,
        simulator=ABMSimulator(),
    ):
        super().__init__(seed=seed)
        self.simulator = simulator
        self.simulator.setup(self)

        # Initialize basic properties
        self.initialize_properties(
            height,
            width,
            no_of_couples,
            no_of_singles,
            no_of_grocery_stores,
            no_of_social_places,
            no_of_non_food_shops,
            no_of_others,
        )

        # Set up grid and layers
        self.setup_grid_and_layers()

        # Apply selected scenario
        self.apply_scenario(scenario)

        # Model reporters: Fixed SES references for b_SES_4, c_SES_4, d_SES_4
        model_reporters = {
            "avg_walk_ses1": lambda x: (  # average daily walking trips for SES=1
                sum(
                    agent.daily_walking_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 1
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_walk_ses2": lambda x: (  # average daily walking trips for SES=2
                sum(
                    agent.daily_walking_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 2
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_walk_ses3": lambda x: (  # average daily walking trips for SES=3
                sum(
                    agent.daily_walking_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 3
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_walk_ses4": lambda x: (  # average daily walking trips for SES=4
                sum(
                    agent.daily_walking_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 4
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_walk_ses5": lambda x: (  # average daily walking trips for SES=5
                sum(
                    agent.daily_walking_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 5
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_work_ses1": lambda x: (  # average work trips for SES=1
                sum(
                    agent.work_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 1
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_work_ses2": lambda x: (  # average work trips for SES=2
                sum(
                    agent.work_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 2
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_work_ses3": lambda x: (  # average work trips for SES=3
                sum(
                    agent.work_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 3
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_work_ses4": lambda x: (  # average work trips for SES=4
                sum(
                    agent.work_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 4
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_work_ses5": lambda x: (  # average work trips for SES=5
                sum(
                    agent.work_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 5
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_basic_ses1": lambda x: (  # average basic-needs trips for SES=1
                sum(
                    agent.basic_needs_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 1
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_basic_ses2": lambda x: (  # average basic-needs trips for SES=2
                sum(
                    agent.basic_needs_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 2
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_basic_ses3": lambda x: (  # average basic-needs trips for SES=3
                sum(
                    agent.basic_needs_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 3
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_basic_ses4": lambda x: (  # average basic-needs trips for SES=4
                sum(
                    agent.basic_needs_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 4
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_basic_ses5": lambda x: (  # average basic-needs trips for SES=5
                sum(
                    agent.basic_needs_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 5
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_leisure_ses1": lambda x: (  # average leisure trips for SES=1
                sum(
                    agent.leisure_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 1
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_leisure_ses2": lambda x: (  # average leisure trips for SES=2
                sum(
                    agent.leisure_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 2
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_leisure_ses3": lambda x: (  # average leisure trips for SES=3
                sum(
                    agent.leisure_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 3
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_leisure_ses4": lambda x: (  # average leisure trips for SES=4
                sum(
                    agent.leisure_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 4
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
            "avg_leisure_ses5": lambda x: (  # average leisure trips for SES=5
                sum(
                    agent.leisure_trips
                    for agent in x.agents_by_type[Human]
                    if agent.SES == 5
                )
                / len(x.agents_by_type[Human])
                if x.agents_by_type[Human]
                else 0
            ),
        }

        self.datacollector = DataCollector(model_reporters)
        # Add initial humans
        self.add_initial_humans()

        self.datacollector.collect(self)
        self.running = True

    def initialize_properties(
        self,
        height,
        width,
        no_of_couples,
        no_of_singles,
        no_of_grocery_stores,
        no_of_social_places,
        no_of_non_food_shops,
        no_of_others,
    ):
        """Initialize basic model properties."""
        self.height = height
        self.width = width
        self.no_of_couples = no_of_couples
        self.no_of_singles = no_of_singles
        self.no_of_grocery_stores = no_of_grocery_stores
        self.no_of_social_places = no_of_social_places
        self.no_of_non_food_shops = no_of_non_food_shops
        self.no_of_others = no_of_others
        self.no_of_humans = 2 * self.no_of_couples + self.no_of_singles
        self.unique_id = 1

    def setup_grid_and_layers(self):
        """Set up the visual grid and associated layers."""
        self.grid = OrthogonalVonNeumannGrid(
            [self.height, self.width],
            torus=True,
            capacity=math.inf,
            random=self.random,
        )
        self.safety_cell_layer = PropertyLayer(
            "safety", (self.width, self.height), dtype=float
        )
        self.aesthetic_cell_layer = PropertyLayer(
            "aesthetic", (self.width, self.height), dtype=float
        )
        self.setup_aesthetic_layer()

    def setup_aesthetic_layer(self):
        """Setup aesthetic distribution with central tendency and organic variations"""
        center_x, center_y = self.height // 2, self.width // 2
        max_distance = math.sqrt((self.height // 2) ** 2 + (self.width // 2) ** 2)

        # Create multiple aesthetic hotspots
        hotspots = [
            (center_x, center_y, 1.0),  # Main center, full weight
            (
                center_x + self.height // 4,
                center_y + self.width // 4,
                0.7,
            ),  # Secondary spots
            (center_x - self.height // 4, center_y - self.width // 4, 0.7),
            (center_x + self.height // 3, center_y - self.width // 3, 0.5),
            (center_x - self.height // 3, center_y + self.width // 3, 0.5),
        ]

        # Create base noise grid for organic variation
        noise_grid = [
            [self.random.random() * 0.3 for _ in range(self.width)]
            for _ in range(self.height)
        ]

        # Apply smoothing to noise
        smoothing_radius = 2
        smoothed_noise = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                total = 0
                count = 0
                for di in range(-smoothing_radius, smoothing_radius + 1):
                    for dj in range(-smoothing_radius, smoothing_radius + 1):
                        ni, nj = (i + di) % self.height, (j + dj) % self.width
                        total += noise_grid[ni][nj]
                        count += 1
                smoothed_noise[i][j] = total / count

        def calculate_aesthetic_value(i, j):
            # Calculate influence from all hotspots
            hotspot_influence = 0
            total_weight = 0

            for hx, hy, weight in hotspots:
                distance = math.sqrt((i - hx) ** 2 + (j - hy) ** 2)
                normalized_distance = distance / max_distance

                # Exponential decay with distance
                influence = math.exp(-2 * normalized_distance) * weight
                hotspot_influence += influence
                total_weight += weight

            # Normalize hotspot influence
            hotspot_value = hotspot_influence / total_weight

            # Combine with smoothed noise
            base_value = hotspot_value * 0.7 + smoothed_noise[i][j]

            # Add some local character
            local_variation = self.random.random() * 0.2
            if base_value > 0.7:  # High aesthetic areas get more consistent
                local_variation *= 0.5

            # Add some "character" to certain areas
            if 0.3 < base_value < 0.7:  # Mid-range areas get more variation
                local_variation *= 1.5

            final_value = base_value + local_variation

            # Ensure value stays within [0, 1]
            return max(0.1, min(1.0, final_value))

        for i in range(self.height):
            for j in range(self.width):
                self.aesthetic_cell_layer.data[i][j] = calculate_aesthetic_value(i, j)

        # Apply final smoothing pass for more natural transitions
        final_smoothing = 1
        for i in range(self.height):
            for j in range(self.width):
                total = 0
                count = 0
                for di in range(-final_smoothing, final_smoothing + 1):
                    for dj in range(-final_smoothing, final_smoothing + 1):
                        ni, nj = (i + di) % self.height, (j + dj) % self.width
                        total += self.aesthetic_cell_layer.data[ni][nj]
                        count += 1
                self.aesthetic_cell_layer.data[i][j] = total / count

    def apply_scenario(self, scenario: str):
        """Apply chosen scenario for building placement & safety setup."""
        scenario_handlers = {
            "random_random": self._apply_random_random,
            "random_safe": self._apply_random_safe,
            "central_random": self._apply_central_random,
            "central_safe": self._apply_central_safe,
        }
        if scenario not in scenario_handlers:
            raise ValueError(f"Invalid scenario: {scenario}")
        scenario_handlers[scenario]()

    def _place_buildings_random(self):
        """Place buildings randomly on the grid."""
        building_types = [
            (GroceryStore, self.no_of_grocery_stores),
            (SocialPlace, self.no_of_social_places),
            (NonFoodShop, self.no_of_non_food_shops),
            (Other, self.no_of_others),
        ]

        for building_type, count in building_types:
            for _ in range(count):
                cell = self.grid.select_random_empty_cell()
                if cell is not None:
                    building_type(self, cell)

    def _place_buildings_central(self):
        """Place buildings with stronger central tendency using exponential decay."""
        center_x, center_y = self.width // 2, self.height // 2
        max_distance = math.sqrt((self.width // 2) ** 2 + (self.height // 2) ** 2)

        # Different weights for different building types (personal preference)
        building_types = [
            (GroceryStore, self.no_of_grocery_stores, 0.7),  # Less centralized
            (SocialPlace, self.no_of_social_places, 0.85),  # More centralized
            (NonFoodShop, self.no_of_non_food_shops, 0.9),  # Highly centralized
            (Other, self.no_of_others, 0.6),  # Least centralized
        ]

        def get_placement_probability(x, y, centralization_weight):
            # Calculate distance from center
            distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            normalized_distance = distance / max_distance

            # Exponential decay function for stronger central tendency
            prob = math.exp(-centralization_weight * normalized_distance * 3)

            # Add some randomness to avoid perfect circles
            prob *= 0.8 + 0.4 * self.random.random()

            return prob

        for building_type, count, centralization_weight in building_types:
            buildings_placed = 0
            max_attempts = count * 20
            attempts = 0

            while buildings_placed < count and attempts < max_attempts:
                cell = self.grid.select_random_empty_cell()
                if cell is None:
                    break

                x, y = cell.coordinate
                if self.random.random() < get_placement_probability(
                    x, y, centralization_weight
                ):
                    building_type(self, cell)
                    buildings_placed += 1
                attempts += 1

    def _setup_random_safety(self):
        """Set up random safety values with some spatial correlation."""
        # Initialize with pure random values
        base_values = [
            [self.random.random() for _ in range(self.width)]
            for _ in range(self.height)
        ]

        # Apply smoothing to create more realistic patterns
        smoothing_radius = 2
        for i in range(self.height):
            for j in range(self.width):
                # Calculate average of neighboring cells
                total = 0
                count = 0
                for di in range(-smoothing_radius, smoothing_radius + 1):
                    for dj in range(-smoothing_radius, smoothing_radius + 1):
                        ni, nj = (i + di) % self.height, (j + dj) % self.width
                        total += base_values[ni][nj]
                        count += 1

                # Set smoothed value with some random variation
                smoothed = total / count
                variation = (self.random.random() - 0.5) * 0.2  # +/-0.1 variation
                self.safety_cell_layer.data[i][j] = max(
                    0.1, min(1.0, smoothed + variation)
                )

    def _setup_central_safety(self):
        """Set up safety values with a subtle urban-like distribution."""
        center_x, center_y = self.height // 2, self.width // 2
        max_distance = math.sqrt((self.height // 2) ** 2 + (self.width // 2) ** 2)

        # Define centers with proper formatting
        centers = [
            (center_x, center_y),  # Main center
            # Secondary Centers: Removed for model simplicity.
            # (center_x + self.height // 4, center_y + self.width // 4),  # NE
            # (center_x - self.height // 4, center_y - self.width // 4),  # SW
            # (center_x + self.height // 4, center_y - self.width // 4),  # SE
            # (center_x - self.height // 4, center_y + self.width // 4),  # NW
        ]

        def calculate_safety(i, j):
            # Calculate Manhattan distance
            distances = [max(abs(i - cx), abs(j - cy)) for cx, cy in centers]
            min_distance = min(distances) / max_distance

            # More subtle base safety calculation for center
            base_safety = 0.4 + (
                min_distance * 0.4
            )  # Reduced range and increased minimum

            # Reduced square influence for center
            square_factor = abs((i - center_x) / self.height) + abs(
                (j - center_y) / self.width
            )
            central_damping = 1 - max(0, 0.7 - min_distance)  # Reduce effect in center
            square_influence = (
                square_factor * 0.15 * central_damping
            )  # Reduced overall influence

            # Smaller local variation
            local_variation = self.random.random() * 0.03  # Reduced random variation

            # More subtle transition in center
            if min_distance < 0.3:
                safety = (
                    base_safety + (square_influence * 0.5) + (local_variation * 0.5)
                )
            else:
                safety = base_safety + square_influence + (local_variation * 0.4)

            return max(0.3, min(0.85, safety))  # Narrower range for more subtlety

        # Fill the safety layer
        for i in range(self.height):
            for j in range(self.width):
                self.safety_cell_layer.data[i][j] = calculate_safety(i, j)

    def _apply_random_random(self):
        self._place_buildings_random()
        self._setup_random_safety()

    def _apply_random_safe(self):
        self._place_buildings_random()
        self._setup_central_safety()

    def _apply_central_random(self):
        self._place_buildings_central()
        self._setup_random_safety()

    def _apply_central_safe(self):
        self._place_buildings_central()
        self._setup_central_safety()

    def add_initial_humans(self):
        """Add initial humans with distance-based cell organization. Each cell can contain up to 'n' households.
        Couples share households."""
        center_x, center_y = self.height // 2, self.width // 2
        max_distance = math.sqrt((self.height // 2) ** 2 + (self.width // 2) ** 2)
        MAX_HOUSEHOLDS_PER_CELL = 10

        # Track available cells and their SES levels along with current occupancy
        cells_by_ses = {}
        cell_occupancy = {}  # Track number of households in each cell

        for cell in self.grid.all_cells:
            x, y = cell.coordinate
            distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            normalized_distance = distance / max_distance

            # Assign SES based on normalized distance from center
            if normalized_distance < 0.2:
                ses_level = 1
            elif normalized_distance < 0.4:
                ses_level = 2
            elif normalized_distance < 0.6:
                ses_level = 3
            elif normalized_distance < 0.8:
                ses_level = 4
            else:
                ses_level = 5

            if ses_level not in cells_by_ses:
                cells_by_ses[ses_level] = []
            cells_by_ses[ses_level].append(cell)
            cell_occupancy[cell] = 0  # Initialize occupancy counter

        def find_available_cell(ses):
            """Helper function to find a cell that hasn't reached maximum capacity"""
            # Try in preferred SES zone first
            available_cells = [
                cell
                for cell in cells_by_ses.get(ses, [])
                if cell_occupancy[cell] < MAX_HOUSEHOLDS_PER_CELL
            ]

            if available_cells:
                return self.random.choice(available_cells)

            # Look in adjacent SES zones (alternate between higher and lower)
            for offset in range(1, 5):
                # Try higher SES
                if ses + offset <= 5:
                    available_cells = [
                        cell
                        for cell in cells_by_ses.get(ses + offset, [])
                        if cell_occupancy[cell] < MAX_HOUSEHOLDS_PER_CELL
                    ]
                    if available_cells:
                        return self.random.choice(available_cells)

                # Try lower SES
                if ses - offset >= 1:
                    available_cells = [
                        cell
                        for cell in cells_by_ses.get(ses - offset, [])
                        if cell_occupancy[cell] < MAX_HOUSEHOLDS_PER_CELL
                    ]
                    if available_cells:
                        return self.random.choice(available_cells)

            return None

        # Place couples first (they share the same household)
        for _ in range(self.no_of_couples):
            ses = self.generate_ses()
            cell = find_available_cell(ses)

            if cell:
                # Create both members of the couple in the same household
                household = cell  # Using cell as household identifier
                cell_occupancy[cell] += (
                    1  # Increment occupancy (couples count as one household)
                )

                male = Human(
                    self,
                    gender="Male",
                    family_size=2,
                    age=self.generate_age(),
                    SES=ses,
                    unique_id=self.unique_id,
                    cell=cell,
                    household=cell,
                )
                self.unique_id += 1
                female = Human(
                    self,
                    gender="Female",
                    family_size=2,
                    age=self.random.randint(
                        male.age - 3, male.age + 3
                    ),  # selecting age with difference no more than 3.
                    SES=ses,
                    unique_id=self.unique_id,
                    cell=cell,
                    household=cell,
                )
                self.unique_id += 1

                # Link the couple together
                male.family = female
                female.family = male

        # Place singles (each gets their own household)
        for _ in range(self.no_of_singles):
            ses = self.generate_ses()
            cell = find_available_cell(ses)

            if cell:
                household = cell  # Using cell as household identifier
                cell_occupancy[cell] += 1  # Increment occupancy

                Human(
                    self,
                    gender=self.generate_gender(),
                    family_size=1,
                    age=self.generate_age(),
                    SES=ses,
                    unique_id=self.unique_id,
                    cell=cell,
                    household=household,
                )
                self.unique_id += 1

    def step(self):
        """Advance the model by one step."""
        self.agents_by_type[Human].shuffle_do("step")

        # Reset daily walking trips
        self.agents_by_type[Human].daily_walking_trips = 0
        self.agents_by_type[Human].work_trips = 0
        self.agents_by_type[Human].basic_needs_trips = 0
        self.agents_by_type[Human].leisure_trips = 0

        self.datacollector.collect(self)

    def generate_gender(self) -> str:
        return "Female" if self.random.random() < FEMALE_PROBABILITY else "Male"

    def generate_age(self) -> int:
        return self.random.randint(MIN_AGE, MAX_AGE)

    def generate_ses(self) -> int:
        return self.random.randint(1, 5)

    def generate_family_size(self) -> int:
        return 1 if self.random.random() < SINGLE_HOUSEHOLD_PROBABILITY else 2

    def generate_dog_ownership(self) -> bool:
        return self.random.random() < DOG_OWNER_PROBABILITY
