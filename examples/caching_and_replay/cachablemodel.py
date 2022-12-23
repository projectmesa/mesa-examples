from model import Schelling
from mesa_replay import CachableModel, CacheState


class CachableSchelling(CachableModel):
    """A wrapper around the original Schelling model to make the simulation cachable and replay-able.
    Uses CachableModel from the Mesa-Replay library, which is a decorator that can be put around any regular mesa model
    to make it "cachable". From outside, a CachableSchelling instance can be treated like any regular Mesa model.
    The only difference is that the model will write the state of every simulation step to a cache file or when in
    replay mode use a given cache file to replay that cached simulation run."""

    def __init__(
        self,
        width=20,
        height=20,
        density=0.8,
        minority_pc=0.2,
        homophily=3,
        # Note that this is an additional parameter we add to our model, which decides whether to simulate or replay
        replay=False,
    ):
        actual_model = Schelling(width, height, density, minority_pc, homophily)
        cache_state = CacheState.REPLAY if replay else CacheState.RECORD
        super().__init__(
            actual_model,
            cache_file_path="my_cache_file_path.cache",
            cache_state=cache_state,
        )
