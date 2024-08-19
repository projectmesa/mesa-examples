import solara
from matplotlib.figure import Figure
from mesa.experimental.devs.simulator import ABMSimulator
from mesa.visualization.solara_viz import SolaraViz, make_text
from .agent import AgentState, Citizen, Cop
from .model import EpsteinCivilViolence


def agent_portrayal(agent):
    if isinstance(agent, Citizen):
        if agent.condition == AgentState.QUIESCENT:
            color = "tab:blue"
        elif agent.condition == AgentState.ACTIVE:
            color = "tab:red"
        else:  # ARRESTED
            color = "tab:gray"
    elif isinstance(agent, Cop):
        color = "tab:green"
    else:
        color = "tab:purple"  # Fallback color

    return {
        "color": color,
        "size": 50,
    }


def get_citizen_cop_ratio(model):
    if model.schedule is None:
        return "Citizen/Cop Ratio: N/A"
    citizen_count = sum(isinstance(agent, Citizen) for agent in model.schedule.agents)
    cop_count = sum(isinstance(agent, Cop) for agent in model.schedule.agents)
    ratio = citizen_count / cop_count if cop_count > 0 else float("inf")
    return f"Citizen/Cop Ratio: {ratio:.2f}"


def make_histogram(model):
    fig = Figure()
    ax = fig.subplots()
    hardship_vals = [
        agent.hardship for agent in model.schedule.agents if isinstance(agent, Citizen)
    ]
    if hardship_vals:  # Ensure there are hardship values to plot
        ax.hist(hardship_vals, bins=10)
    else:
        ax.text(
            0.5,
            0.5,
            "No data to display",
            horizontalalignment="center",
            verticalalignment="center",
        )
    return solara.FigureMatplotlib(fig)


def get_gini(model):
    gini_value = model.datacollector.get_model_vars_dataframe()["Gini"].iloc[-1]
    return f"Gini Coefficient: {gini_value:.2f}"  # Ensure the return value is a string


model_params = {
    "N": {
        "type": "SliderInt",
        "value": 50,
        "label": "Number of agents:",
        "min": 10,
        "max": 100,
        "step": 1,
    },
    "width": 10,
    "height": 10,
    "max_iters": {
        "type": "SliderInt",
        "value": 100,
        "label": "Number of steps:",
        "min": 10,
        "max": 1000,
        "step": 10,
    },
}

# Define the SolaraViz visualization
page = SolaraViz(
    model_class=EpsteinCivilViolence,
    model_params={
        "width": 40,
        "height": 40,
        "citizen_density": 0.7,
        "cop_density": 0.074,
        "citizen_vision": 7,
        "cop_vision": 7,
        "legitimacy": 0.8,
        "max_jail_term": 1000,
        "active_threshold": 0.1,
        "arrest_prob_constant": 2.3,
        "movement": True,
        "max_iters": 100,
    },
    measures=[
        make_text(get_citizen_cop_ratio),
        make_histogram,
        make_text(get_gini),
    ],
    name="Epstein Civil Violence Model",
    agent_portrayal=agent_portrayal,
)


@solara.component
def App():
    solara.Title("Epstein Civil Violence Model")
    solara.Markdown("# Epstein Civil Violence Model")
    solara.Markdown("This is a visualization of the Epstein Civil Violence Model.")

    # Add color legend
    solara.Markdown("""
    ## Color Legend
    - Blue: Quiescent Citizens
    - Red: Active Citizens
    - Gray: Arrested Citizens
    - Green: Cops
    """)

    page.show()


if __name__ == "__main__":
    model = EpsteinCivilViolence(seed=15)
    simulator = ABMSimulator()
    simulator.setup(model)
    simulator.run_for(time_delta=100)
    App()
