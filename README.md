![](./docs/Images/QuakeLabeler.png)

# QuakeLabeler
Quake Labeler was born from the need for seismologists and developers who are not AI specialists to easily, quickly, and independently build and visualize their training data set.

## Introduction
QuakeLabeler is a Python package to customize, build and manage your seismic training data, processes, and visualization in a single place — so you can focus on building the next big thing. Current functionalities include retrieving waveforms from data centers, customizing seismic samples, auto-building datasets, preprocessing and augmenting for labels, and visualizing data distribution. The code helps all levels of AI developers and seismology researchers for querying and building their own earthquake datasets and can be used through an interactive command-line interface with little knowledge of Python.

Installation, Usage, documentation and scripts are described at
 https://maihao14.github.io/QuakeLabeler/

Author: [`Hao Mai`](https://www.uogeophysics.com/authors/mai/)(Developer and Maintainer)
 & [`Pascal Audet`](https://www.uogeophysics.com/authors/admin/) (Developer and Maintainer)

## Installation

### Conda environment

We recommend creating a custom
[conda environment](https://conda.io/docs/user-guide/tasks/manage-environments.html)
where `QuakeLabeler` can be installed along with its dependencies.

- Create a environment called `ql` and install `pygmt`:

```bash
conda create -n ql python=3.8 pygmt -c conda-forge
```

- Activate the newly created environment:

```bash
conda activate ql
```

### Installing from source

Download or clone the repository:
```bash
git clone https://github.com/maihao14/QuakeLabeler.git
cd QuakeLabeler
```

```bash
pip install -e .
```

## Running the scripts

Create a work folder where you will run the scripts that accompany `QuakeLabeler`. For example:

```bash
mkdir ./WorkFolder
cd WorkFolder
```

Run `QuakeLabeler`. Input ``QuakeLabeler`` to `macOS terminal` or `Windows consoles`:

```bash
QuakeLabeler
```

Or input ``quakelabeler`` also works:

```bash
quakelabeler
```

A QuakeLabeler welcome interface will be loading:

```bash
(ql) hao@HaodeMacBook-Pro QuakeLabeler % QuakeLabeler
Welcome to QuakeLabeler----Fast AI Earthquake Dataset Deployment Tool!
QuakeLabeler provides multiple modes for different levels of Seismic AI researchers

[Beginner] mode -- well prepared case studies;
[Advanced] mode -- produce earthquake samples based on Customized parameters.
```


## Contributing
In current version, raw waveforms data from part of Chinese Earthquake stations are unavailable to access automatically (But you can still use QuakeLabeler in China). Any collaborators are welcome to help extend the data sources, develop the codes, etc.

All constructive contributions are welcome, e.g. bug reports, discussions or suggestions for new features. You can either [open an issue on GitHub](https://github.com/maihao14/QuakeLabeler/issues) or make a pull request with your proposed changes. Before making a pull request, check if there is a corresponding issue opened and reference it in the pull request. If there isn't one, it is recommended to open one with your rationale for the change. New functionality or significant changes to the code that alter its behavior should come with corresponding tests and documentation. If you are new to contributing, you can open a work-in-progress pull request and have it iteratively reviewed. Suggestions for improvements (speed, accuracy, etc.) are also welcome.
