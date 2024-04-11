# Import the server object from the server module within the server package.
# This object is configured in server.py, where you set up the
# simulation model, visualization, and user controls.
from examples.hotelling_law.server import server

# This conditional checks if the script is being run directly
# (as opposed to being imported as a module).
# It's a common Python idiom for making code both importable as a module and
# executable as a script.
if __name__ == "__main__":
    # If the script is run directly, launch the Mesa server.
    # The server.launch() method starts a web server and opens a browser window
    # to display the simulation's
    # interactive visualization. Users can adjust model parameters through the
    # web interface and observe
    # the simulation in real-time.
    server.launch()
