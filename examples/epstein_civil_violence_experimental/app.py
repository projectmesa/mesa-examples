import solara
from mesa.visualization.solara_viz import SolaraViz, make_text
from model import EpsteinCivilViolence

from .agent import AgentState, Citizen, Cop


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
        "max_iters": 1000,
    },
    measures=[
        make_text(get_citizen_cop_ratio),
    ],
    name="Epstein Civil Violence Model",
    agent_portrayal=agent_portrayal,
)

@solara.component
def App():
    solara.Title("Epstein Civil Violence Model")
    solara.Markdown("# Epstein Civil Violence Model")
    solara.Markdown("This is a visualization of the Epstein Civil Violence Model.")
    
    solara.Markdown("""
    ## Color Legend
    - Blue: Quiescent Citizens
    - Red: Active Citizens
    - Gray: Arrested Citizens
    - Green: Cops
    """)
    
    page.show()

if __name__ == "__main__":
    App()
