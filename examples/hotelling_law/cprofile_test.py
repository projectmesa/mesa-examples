import cProfile
import pstats

from .hotelling_law.model import HotellingModel

# Create a profiler object
profiler = cProfile.Profile()

# Start profiling
profiler.enable()

model = HotellingModel(
        N_stores=5,
        width=20,
        height=20,
        mode="default",
        consumer_preferences="default",
        environment_type="grid",
        mobility_rate=80,
    )
model.run_model(step_count=500)

df_model = model.datacollector.get_model_vars_dataframe()

# Stop profiling
profiler.disable()

# Create Stats object and sort the results by cumulative time taken
stats = pstats.Stats(profiler).sort_stats("cumulative")

# Print the stats report
stats.print_stats()

stats.dump_stats("specific_profile_results.prof")
