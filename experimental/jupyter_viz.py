import threading

import solara
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator


# Avoid interactive backend
plt.switch_backend("agg")


class JupyterContainer:
    def __init__(self, model_class, model_params, measures=None, name="Mesa Model", agent_portrayal=None):
        self.model_class = model_class
        self.split_model_params(model_params)
        self.measures = measures
        self.name = name
        self.agent_portrayal = agent_portrayal
        self.thread = None

    def split_model_params(self, model_params):
        self.model_params_input = {}
        self.model_params_fixed = {}
        for k, v in model_params.items():
            if self.check_param_is_fixed(v):
                self.model_params_fixed[k] = v
            else:
                self.model_params_input[k] = v

    def check_param_is_fixed(self, param):
        if not isinstance(param, dict):
            return True
        if "type" not in param:
            return True

    def do_step(self):
        self.model.step()
        self.set_df(self.model.datacollector.get_model_vars_dataframe())

    def do_play(self):
        self.model.running = True
        while self.model.running:
            self.do_step()

    def threaded_do_play(self):
        if self.thread is not None and self.thread.is_alive():
            return
        self.thread = threading.Thread(target=self.do_play)
        self.thread.start()

    def do_pause(self):
        if (self.thread is None) or (not self.thread.is_alive()):
            return
        self.model.running = False
        self.thread.join()

    def portray(self, g):
        x = []
        y = []
        s = []
        for i in range(g.width):
            for j in range(g.height):
                for agent in g._grid[i][j]:
                    _s = self.agent_portrayal(agent)
                    x.append(i)
                    y.append(j)
                    s.append(_s)
        return {"x": x, "y": y, "s": s}


@solara.component
def MesaComponent(viz):
    solara.Markdown(viz.name)

    # 1. User inputs
    user_inputs = {}
    for k, v in viz.model_params_input.items():
        if v["type"] == "SliderInt":
            user_input = solara.use_reactive(v["value"])
            user_inputs[k] = user_input.value
            solara.SliderInt(
                v.get("label", "label"),
                value=user_input,
                min=v.get("min", 0),
                max=v.get("max", 10),
                step=v.get("step", 1),
            )

    # 2. Model
    def make_model():
        return viz.model_class(**user_inputs, **viz.model_params_fixed)

    viz.model = solara.use_memo(make_model, dependencies=list(user_inputs.values()))
    viz.df, viz.set_df = solara.use_state(
        viz.model.datacollector.get_model_vars_dataframe()
    )

    # 3. Buttons
    with solara.Row():
        solara.Button(label="Step", color="primary", on_click=viz.do_step)
        solara.Button(label="▶", color="primary", on_click=viz.threaded_do_play)
        solara.Button(label="⏸︎", color="primary", on_click=viz.do_pause)
        # solara.Button(label="Reset", color="primary", on_click=do_reset)

    # 3. Space
    space_fig = Figure()
    space_ax = space_fig.subplots()
    space_ax.scatter(**viz.portray(viz.model.grid))
    space_ax.set_axis_off()
    solara.FigureMatplotlib(space_fig, dependencies=[viz.model, viz.df])

    # 4. Plots
    for i, measure in enumerate(viz.measures):
        fig = Figure()
        ax = fig.subplots()
        ax.plot(viz.df.loc[:, measure])
        ax.set_ylabel(measure)
        # Set integer x axis
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        solara.FigureMatplotlib(fig, dependencies=[viz.model, viz.df])


def JupyterViz(model_class, model_params, measures=None, name="Mesa Model", agent_portrayal=None):
    return MesaComponent(JupyterContainer(model_class, model_params, measures, name, agent_portrayal))
