![](./docs/Images/homepage.png)

# QuakeLabeler

QuakeLabeler is a Python package to create and manage your seismic training data, processes, and visualization in a single place — so you can focus on building the next big thing.

## Introduction
SeisLabelCreator (SLC) is a package containing Python tools for labelling earthquake data (for machine learning applications). Current functionalities include retrieving waveforms from data centers, customizing seismic samples, auto-preparing datasets for training, testing and validation, preprocessing and augmenting techniques, and visualizing data distribution. The code helps all levels of AI developers and researchers for querying and building their own earthquake datasets and can be used through an interactive command-line interface with little knowledge of Python.

Installation, Usage, API documentation and scripts are described at
*TBD*.

Author: [`Hao Mai`](https://www.uogeophysics.com/authors/mai/)(Developer and Maintainer)
 & [`Pascal Audet`](https://www.uogeophysics.com/authors/admin/) (Developer and Maintainer)

## Installation

### Conda environment

We recommend creating a custom
[conda environment](https://conda.io/docs/user-guide/tasks/manage-environments.html)
where `seiscreator` can be installed along with its dependencies.

- Create a environment called `slc` and install `obspy`:

```bash
conda create -n slc python=3.8 obspy -c conda-forge
```

- Activate the newly created environment:

```bash
conda activate slc
```

### Installing from source

Download or clone the repository:
```bash
git clone https://github.com/maihao14/SeisLabelCreator.git
cd SeisLabelCreator
```

```bash
pip install .
```

If you work in development mode, use the `-e` argument as `pip install -e .`

## Running the scripts

Create a work folder where you will run the scripts that accompany `SeisLabelCreator`. For example

```bash
mkdir ~/WorkFolder
cd WorkFolder
```

Run the main script `SeisCreator` with default arguments

```bash
SeisCreator
```
