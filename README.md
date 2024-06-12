## Grasshopper - ROS Communication

This repository contains examples for bridging data between Grasshopper and ROS.

- using compass fab
  - turtlesim
      - twist publisher
      - pose subcriber
   - pose and pose array publisher
   - pointcloud subscriber (and joint state subscriber)
- YAML file writer: writes list of poses to a yaml file that can be parsed in ROS


### COMPAS FAB installation

Pre-requisites:
- Python 3.8 or similar (and pip)
- Rhino 7.0
- [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/es/visual-cpp-build-tools/): Make sure to include the **"Desktop development with C++"** workload. After installing the build tools, **restart your computer** to ensure that the changes take effect.

See COMPAS FAB installation instructions [here](https://gramaziokohler.github.io/compas_fab/latest/getting_started.html). In summary:

```bash
pip install compas_fab
```
```bash
python -m compas_rhino.install
```
If you are working with point clouds, I highly recommend you to install **Volvox** and **Tarsier** grasshopper plug-ins.

### Rosbridge installation and usage

Installation:

```bash
sudo apt install ros-noetic-rosbridge-suite
```
Usage:

```bash
roslaunch rosbridge_server rosbridge_websocket.launch
```
If you are following the steps in [software_II_project](https://github.com/ainhoaarnaiz/software_II_project.git), rosbridge suite is already included in the docker container.
