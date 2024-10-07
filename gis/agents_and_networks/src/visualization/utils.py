import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import solara

from ..agent.building import Building
from ..agent.commuter import Commuter
from ..agent.geo_agents import Driveway, LakeAndRiver, Walkway


def make_plot_clock(model):
    return solara.Markdown(f"**Day {model.day}, {model.hour:02d}:{model.minute:02d}**")


def agent_draw(agent):
    portrayal = {}
    portrayal["color"] = "White"
    if isinstance(agent, Driveway):
        portrayal["color"] = "#D08004"
    elif isinstance(agent, Walkway):
        portrayal["color"] = "Brown"
    elif isinstance(agent, LakeAndRiver):
        portrayal["color"] = "#04D0CD"
    elif isinstance(agent, Building):
        portrayal["color"] = "Grey"
        # if agent.function is None:
        #     portrayal["color"] = "Grey"
        # elif agent.function == 1.0:
        #     portrayal["color"] = "Blue"
        # elif agent.function == 2.0:
        #     portrayal["color"] = "Green"
        # else:
        #     portrayal["color"] = "Grey"
    elif isinstance(agent, Commuter):
        if agent.status == "home":
            portrayal["color"] = "Green"
        elif agent.status == "work":
            portrayal["color"] = "Blue"
        elif agent.status == "transport":
            portrayal["color"] = "Red"
        else:
            portrayal["color"] = "Grey"
        portrayal["radius"] = "5"
        portrayal["fillOpacity"] = 1
    return portrayal


def plot_commuter_status_count(model_vars_df: pd.DataFrame) -> None:
    commuter_status_df = model_vars_df.rename(
        columns=lambda x: x.replace("status_", "")
    )
    commuter_status_df["time"] = commuter_status_df["time"] / pd.Timedelta(minutes=1)
    commuter_status_df = commuter_status_df.melt(
        id_vars=["time"],
        value_vars=["home", "traveling", "work"],
        var_name="status",
        value_name="count",
    )
    sns.relplot(
        x="time",
        y="count",
        data=commuter_status_df,
        kind="line",
        hue="status",
        aspect=1.5,
    )
    plt.gca().xaxis.set_major_formatter(
        lambda x, pos: ":".join(str(datetime.timedelta(minutes=x)).split(":")[:2])
    )
    plt.xticks(rotation=90)
    plt.title("Number of commuters by status")


def plot_num_friendships(model_vars_df: pd.DataFrame) -> None:
    friendship_df = model_vars_df.rename(columns=lambda x: x.replace("friendship_", ""))
    friendship_df["time"] = friendship_df["time"] / pd.Timedelta(minutes=1)
    friendship_df = friendship_df.melt(
        id_vars=["time"],
        value_vars=["home", "work"],
        var_name="friendship",
        value_name="count",
    )
    sns.relplot(
        x="time",
        y="count",
        data=friendship_df,
        kind="line",
        hue="friendship",
        aspect=1.5,
    )
    plt.gca().xaxis.set_major_formatter(
        lambda x, pos: ":".join(str(datetime.timedelta(minutes=x)).split(":")[:2])
    )
    plt.xticks(rotation=90)
    plt.title("Number of friendships")
