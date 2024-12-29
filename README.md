# Explorers

## Installation

Run the shell script `./install.sh` to install the game. You may need to `chmod +x` the scripts `test.sh`, `compile.sh`, and `install.sh` to do so.

## Playing

To play, simply run `python3 __init__.py`.

### Basic Controls

* Use the arrow keys to move the camera.
    * You can also click on the minimap.
* Use the plus and minus keys to zoom the camera.
* Click on an astronaut to select them.
* Click on the terrain to move your selected astronauts.
* Click on objects to interact with them.

## Programming Notes

This point on details how the game's source code is structured.

### Directory Structure

There are two root-level code directories. **src** holds the source code for the game, and **test** holds the unit tests for the game's code.

Both directories are organized like so:

* **colony** contains code about managing settlements.
* **ctrl** contains code for translating keyboard/mouse signals into game controls.
* **gameobject** contains code for _objects_ that are shown in the _game_, such as player characters, structures, and vehicles.
* **gen** contains code for _gen_erating terrain and other planet characteristics.
* **gui** contains code for rendering the game's GUI, including buttons, images, and text.
* **math** contains code for everything you've learned about in your basic comp sci classes, including vectors, voronoi diagrams, line segments, etc.
* **mgmt** contains code for managing the game state and passage of time.
* **o10n** stands for optimization.
* **path** contains code for pathfinding and path running.
* **render** is the glue module between game state and the screen.
* **rendermath** is exactly what it sounds like - math for rendering, particularly isometric transformations, image scaling, and draw order.
* **utility** contains misc. stuff.
* **world** models the dynamics of the game world, such as terrain, atmosphere, and the orbital layer.

The **assets** directory holds images, sounds, and plaintext.

### Compiled Library

_Explorers_ uses a library written in C for terrain generation. If changes are made to it, you must run `./compile.sh` before playing the game again.
