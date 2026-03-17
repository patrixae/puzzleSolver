# Lösung

![Python: 3.12](https://img.shields.io/badge/python-3.12-yellow)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Typing: mypy](https://img.shields.io/badge/typing-mypy-yellowgreen)](https://github.com/python/mypy)
[![Linter: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

## Install dependencies

With `make prepare`, the necessary pip dependencies are installed.

## Install dev dependencies

With `make prepare-dev`, the necessary pip dependencies for development are installed.

Additionally following (non python) packages are needed for `pygraphviz (package name is for debian systems):

- `gcc`
- `libc-dev`
- `graphviz`
- `graphviz-dev`
- `python3.12-dev`

## Formatter

We use the [`black`](https://github.com/psf/black) formatter.

Installation:

```bash
pip install black
```

Run:

```bash
make format
```

## Typing check

We use [`mypy`](https://github.com/python/mypy) for checking typing.

Installation:

```bash
pip install mypy
```

Run:

```bash
make typing
```

## Linting

We user [`pylint`](https://github.com/pylint-dev/pylint) for linting.

Installation:

```bash
pip install pylint
```

Run:

```bash
make linting
```

## Checking everything

All static checks can be run at once with:

```bash
make check
```

## Tests

All tests in the `./test` folder can be run with:

```bash
make test
```

## Rosbag

In order to use the rosbag container you need:

- image: gitlab.lrz.de:5005/robotikss25/loesung/rosbag
- volume: folder where the ros bags will be saved (rosbag/bags)
- command: record | play
- arguments: bag-name topics | bag-name

Rosbag container could be run with:

```bash
docker run -it -v ./rosbag/bags:/ros2/bags gitlab.lrz.de:5005/robotikss25/loesung/rosbag record bag-name /test/topic1 /test/topic2
docker run -it -v ./rosbag/bags:/ros2/bags gitlab.lrz.de:5005/robotikss25/loesung/rosbag play bag-name
```


## Solver Debug Visualization

The solver currently offers two types of visualization.

### Command Line Visualization of the Puzzle Context

This prints the current piece ids stored in the puzzle context to the CLI.

Activate with:

```sh
export SOLVER_VISUALIZE="ON"
```

### Graphical Representation including Images

This visualizes the Puzzle Context including the images of the placed puzzle pieces using matplotlib.

Activate with:

```sh
export SOLVER_VISUALIZE_GUI="ON"
```
