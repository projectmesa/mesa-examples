import solara
from mesa.visualization.solara_viz import SolaraViz, make_text
from mesa.experimental.devs.simulator import ABMSimulator
from .model import BankReserves
from .agents import Person, Bank


def agent_portrayal(agent):
    if isinstance(agent, Person):
        color = "tab:blue"
    elif isinstance(agent, Bank):
        color = "tab:green"
    else:
        color = "tab:purple"  # Fallback color

    return {
        "color": color,
        "size": 50,
    }


def get_rich_poor_ratio(model):
    if model.schedule is None:
        return "Rich/Poor Ratio: N/A"
    rich_count = sum(
        isinstance(agent, Person) and agent.savings > model.rich_threshold
        for agent in model.schedule.agents
    )
    poor_count = sum(
        isinstance(agent, Person) and agent.loans > 10
        for agent in model.schedule.agents
    )
    ratio = rich_count / poor_count if poor_count > 0 else float("inf")
    return f"Rich/Poor Ratio: {ratio:.2f}"


# Define the SolaraViz visualization
page = SolaraViz(
    model_class=BankReserves,
    model_params={
        "height": 20,
        "width": 20,
        "init_people": 2,
        "rich_threshold": 10,
        "reserve_percent": 50,
    },
    measures=[
        make_text(get_rich_poor_ratio),
    ],
    name="Bank Reserves Model",
    agent_portrayal=agent_portrayal,
)


@solara.component
def App():
    solara.Title("Bank Reserves Model")
    solara.Markdown("# Bank Reserves Model")
    solara.Markdown("This is a visualization of the Bank Reserves Model.")

    # Add color legend
    solara.Markdown("""
    ## Color Legend
    - Blue: Persons
    - Green: Bank
    - Purple: Other
    """)

    page.show()


if __name__ == "__main__":
    model = BankReserves(seed=15)
    simulator = ABMSimulator()
    simulator.setup(model)
    simulator.run_for(time_delta=100)
    App()
