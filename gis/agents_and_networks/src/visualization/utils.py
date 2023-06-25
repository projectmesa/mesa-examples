import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


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
