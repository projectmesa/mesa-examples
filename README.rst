mesa-examples
------------------------
This repository contains examples that work with Mesa and illustrate different features of Mesa. 

To contribute to this repository, see `CONTRIBUTING.rst`_

.. _`CONTRIBUTING.rst` : https://github.com/projectmesa/mesa-examples/blob/main/CONTRIBUTING.rst

Running mesa-examples in Docker
------------------------

You can run mesa-examples in a Docker container to streamline running example models.

First `install Docker Compose <https://docs.docker.com/compose/install/>`_ and then, in the folder containing the mesa-examples Git repository, you run:

.. code-block:: bash

    $ docker compose up
    # If you want to make it run in the background, you instead run
    $ docker compose up -d

This runs the wolf-sheep predation model by default. If you wish to run another example, simply update the MODEL_DIR variable both in the Dockerfile and docker-compose.yml files.
