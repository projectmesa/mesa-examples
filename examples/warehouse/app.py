import matplotlib.pyplot as plt
import pandas as pd
import solara
from mesa.visualization import SolaraViz
from mesa.visualization.utils import update_counter
from warehouse.agents import InventoryAgent
from warehouse.model import WarehouseModel, WarehouseScenario

model_params = {
    "rng": {
        "type": "InputText",
        "value": 42,
        "label": "Random seed",
    },
    "rows": {
        "type": "SliderInt",
        "value": 8,
        "label": "Rows:",
        "min": 6,
        "max": 20,
        "step": 1,
    },
    "cols": {
        "type": "SliderInt",
        "value": 8,
        "label": "Cols:",
        "min": 6,
        "max": 20,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 2,
        "label": "Height:",
        "min": 2,
        "max": 5,
        "step": 1,
    },
}


def prepare_agent_data(model, agent_type, agent_label):
    """Prepare data for agents of a specific type.

    Args:
        model: The WarehouseModel instance.
        agent_type: The type of agent (e.g., "InventoryAgent", "RobotAgent").
        agent_label: The label for the agent type.

    Returns:
        A list of dictionaries containing agent coordinates and type.
    """
    return [
        {
            "x": agent.cell.coordinate[0],
            "y": agent.cell.coordinate[1],
            "z": agent.cell.coordinate[2],
            "type": agent_label,
        }
        for agent in model.agents_by_type[agent_type]
    ]


def prepare_robot_data(model):
    """Collect robot positions from the explicit robot list."""
    return [
        {
            "x": agent.cell.coordinate[0],
            "y": agent.cell.coordinate[1],
            "z": agent.cell.coordinate[2],
            "type": "Robot",
        }
        for agent in model.robots
    ]


@solara.component
def plot_warehouse(model):
    """Visualize the warehouse model in a 3D scatter plot.

    Args:
        model: The WarehouseModel instance.
    """
    update_counter.get()

    # Prepare data for inventory and robot agents
    inventory_data = prepare_agent_data(model, InventoryAgent, "Inventory")
    robot_data = prepare_robot_data(model)

    # Combine data into a single DataFrame
    data = pd.DataFrame(inventory_data + robot_data)

    # Create Matplotlib 3D scatter plot
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")

    # Highlight loading dock cells (from scenario-driven coords)
    for i, dock in enumerate(model.loading_docks):
        ax.scatter(
            dock[0],
            dock[1],
            dock[2],
            c="yellow",
            label="Loading Dock"
            if i == 0
            else None,  # Add label only to the first dock
            s=300,
            marker="o",
        )

    # Plot inventory agents
    if not data.empty:
        inventory = data[data["type"] == "Inventory"]
        if not inventory.empty:
            ax.scatter(
                inventory["x"],
                inventory["y"],
                inventory["z"],
                c="blue",
                label="Inventory",
                s=100,
                marker="s",
            )

        # Plot robot agents
        robots = data[data["type"] == "Robot"]
        if not robots.empty:
            ax.scatter(
                robots["x"], robots["y"], robots["z"], c="red", label="Robot", s=200
            )

    # Set labels, title, and legend
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Warehouse Visualization")
    ax.legend()

    # Configure plot appearance - from WarehouseScenario
    ax.grid(False)
    ax.set_xlim(0, model.scenario.rows)
    ax.set_ylim(0, model.scenario.cols)
    ax.set_zlim(0, model.scenario.height + 1)
    ax.axis("off")

    # Render the plot in Solara
    solara.FigureMatplotlib(fig)


@solara.component
def show_memberships(model):
    """Shallow backend showcase: triplet count and per-robot relations."""
    update_counter.get()
    # Backend-authoritative count (MembershipBackend.as_triplets)
    triplet_count = len(model.membership_backend.as_triplets())
    solara.Text(f"Membership triplets (backend): {triplet_count}")

    # Facade view for the first robot (if any)
    robots = model.robots
    if robots:
        robot = robots[0]
        view = model.meta_agents.query_memberships(robot)
        # Show relations present on this robot
        relations = sorted({edge.relation for edge in view.memberships})
        solara.Text(
            f"Robot {robot.unique_id} relations: {', '.join(map(str, relations))}"
        )
        # Also demonstrate members_of with relation filter
        router = next(
            iter(model.meta_agents.members_of(robot, relation="router")), None
        )
        sensor = next(
            iter(model.meta_agents.members_of(robot, relation="sensor")), None
        )
        worker = next(
            iter(model.meta_agents.members_of(robot, relation="worker")), None
        )
        solara.Text(
            f"Members: router={getattr(router, 'unique_id', None)} "
            f"sensor={getattr(sensor, 'unique_id', None)} "
            f"worker={getattr(worker, 'unique_id', None)}"
        )


# Create initial model instance
model = WarehouseModel(scenario=WarehouseScenario(rows=8, cols=8, height=2, rng=42))

# Create the SolaraViz page
page = SolaraViz(
    model,
    components=[plot_warehouse, show_memberships],
    model_params=model_params,
    name="Pseudo-Warehouse Model",
)

page  # noqa
