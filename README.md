# SysDynPy

**Status**: SysDynPy was developed as a college assignment and is currently not under active development. It is provided "as is" for now, but can be used as a code basis for further development if needed.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [How to get started](#how-to-get-started)
- [Module documentation](#module-documentation)

## Overview
SysDynPy - short for *System Dynamics Python* - is a collection of Python modules
to assist you with implementing and running System Dynamics models. It aims at providing a simple to use framework to do quick simulations.

It provides classes representing core System Dynamics objects, like Stocks and Flows, which can be instantiated, connected and configured to build a model. The prerequisite to using this library effectively is, that you already have a model in mind that you want to implement, maybe in form of a simulation diagram. Once the model is built it you can run a simulation and store the results to your filesystem for further use. In addition to that a basic way of visualization in form of line plots is provided to get a first impression of the results.

## Installation

The easiest way is to install the package from PyPi: TODO upload

    pip install --upgrade pip
    pip install SysDynPy

The alternative is building from source. There are multiple tools to use for this. [This tutorial](https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives) shows one possible way. You simply install the build module 

    python -m pip install --upgrade build

and run

    python -m build

from the repositories root folder. This creates the `dist` directory, which contains the file `SysDynPy-0.1.0-py3-none-any.whl`. This file can be installed from the local filesystem with pip (make sure to navigate into the `dist` folder first):

    pip install SysDynPy-0.1.0-py3-none-any.whl


## How to get started
The [examples directory](examples) provides some simple models that can serve as a starting point. We will break down the code of the Lotka-Volterra model (which is a quite common example in the System Dynamics field) step by step.
The simulation diagram for the model we are about to implement looks like this:
![simulation-diagram-lotka-volterra](examples/simulation-diagram-lotka-volterra.png "simulation-diagram-lotka-volterra"). 

#### 1. Creating the system
This step is pretty simple. We create a system so we can reference it when creating the system elements in the next step.

```python
number_of_simulation_steps = 200

# create system
lv_system = System("lotka-volterra")
```

#### 2. Creating system elements


```python
# create elements
predators = Stock("Predators", 40, lv_system)
prey = Stock("Prey", 500, lv_system)

GROWTH_RATE_PREY = Parameter("GROWTH_RATE_PREY", 0.05, lv_system)
LOSS_RATE_PREY = Parameter("LOSS_RATE_PREY", 0.001, lv_system)
GROWTH_RATE_PREDATORS = Parameter("GROWTH_RATE_PREDATORS", 0.0002, lv_system)
ENERGY_LOSS_RATE_PREDATORS = Parameter("ENERGY_LOSS_RATE_PREDATORS", 0.1, lv_system)

increase_in_prey = Flow("increase_in_prey", lv_system)
decrease_in_prey = Flow("decrease_in_prey", lv_system)
increase_in_predators = Flow("increase_in_predators", lv_system)
energy_loss = Flow("energy_loss", lv_system)

encounters = DynamicVariable("encounters", lv_system)
```

#### 3. Connecting system elements
Most system elements have a property named `input_elements` where we can store a list of all system elements that serve as an input for the calculation of that element. Like this, we create one-directional associations which are represented by arrows in the simulation diagram above.

```python
# link elements
predators.input_elements.extend([increase_in_predators, energy_loss])

increase_in_predators.input_elements.extend([GROWTH_RATE_PREDATORS, encounters])
energy_loss.input_elements.extend([ENERGY_LOSS_RATE_PREDATORS, predators])

encounters.input_elements.extend([prey, predators])

prey.input_elements.extend([increase_in_prey, decrease_in_prey])

increase_in_prey.input_elements.extend([prey, GROWTH_RATE_PREY])

decrease_in_prey.input_elements.extend([encounters, LOSS_RATE_PREY])
```

#### 4. Defining calculation rules for each system element
Once we know the inputs of an element, we can define the calculation rule. This step is done after connecting the elements on purpose. That way the calculation rules can be validated as they are defined.
Each calculation rule must use all input elements and can only use basic arithmetic operations (addition, subtraction, multiplication and division).

```python
# set calculation rules
predators.calc_rule = "increase_in_predators - energy_loss"
increase_in_predators.calc_rule = "encounters * GROWTH_RATE_PREDATORS"
energy_loss.calc_rule = "ENERGY_LOSS_RATE_PREDATORS * Predators"

encounters.calc_rule = "Prey * Predators"

prey.calc_rule = "increase_in_prey - decrease_in_prey"
increase_in_prey.calc_rule = "GROWTH_RATE_PREY * Prey"
decrease_in_prey.calc_rule = "LOSS_RATE_PREY * encounters"
```

#### 5. Run the simulation
Now we are ready to run a simulation. This is done with a simulator. Multiple simulators can be used for different configurations (e.g. number of simulation steps), but for now we just use one.
Once the simulation is done `get_simulation_results()` can be used to return them as a dictionary.

```python
# run simulation
s1 = Simulator(number_of_simulation_steps, "weeks")
s1.run_simulation(lv_system)
# get_simulation_results() returns a dict
# Key = Name of the system element, Value = List of numerical values
sim_results = s1.get_simulation_results()
# pprint.pprint(sim_results) # print formatted results to console
```

#### 6. Save the results
At this point you are free to use the results however you like. As simulations can take some time saving the results for later use seems useful. With `csv` and `json` two very common formats are supported.
`export_graph` provides a way to visualize the results. It is meant to give a first impression on how the result looks like and has limited customization options. If you need more control on how the graph looks like libraries like [Matplotlib](https://matplotlib.org/) are designed for that and provide many options. Alternatively you can import the `json` or `csv` file to other software and do the styling there.

```python
# export results to various formats
# make sure the subfolder "results" exists or change the relative path
Exporter.export_data(results=sim_results, file_format="csv", \
    system_elements=["Predators", "Prey"], rel_path="./results/lotka-volterra-results.csv")

Exporter.export_data(results=sim_results, file_format="json", \
    system_elements=["Predators", "Prey"], rel_path=".\\results\\lotka-volterra-results.json")

Exporter.export_graph(results=sim_results, file_format="jpg", \
    system_elements=["Predators", "Prey"], rel_path="results/lotka-volterra-results", \
    title="Lotka-Volterra simulation", label_x="t[weeks]", label_y="Number of Animals",
    range_x=[0,number_of_simulation_steps], range_y=[0,600], colors=["red", "blue"],
    line_width=2, legend_pos="upper right")

Exporter.export_graph(results=sim_results, file_format="png", \
    system_elements=["Prey", "Predators"], rel_path="results\\lotka-volterra-results", \
    title="Lotka-Volterra simulation", label_x="t[weeks]", label_y="Number of Animals",
    range_x=[0,number_of_simulation_steps], range_y=[0,600], colors=["green", "orange"],
    line_width=2, legend_pos="upper left")
```

## Module documentation

A detailed documentation of the module API can be found [here](https://t16h05008.github.io/SysDynPy/).