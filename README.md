![Dragonfly](https://www.ladybug.tools/assets/img/dragonfly.png)

[![Build Status](https://github.com/ladybug-tools/dragonfly-doe2/workflows/CI/badge.svg)](https://github.com/ladybug-tools/dragonfly-doe2/actions)
[![Coverage Status](https://coveralls.io/repos/github/ladybug-tools/dragonfly-doe2/badge.svg?branch=master)](https://coveralls.io/github/ladybug-tools/dragonfly-doe2)

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

# dragonfly-doe2

Dragonfly extension for energy modeling with the DOE-2 engine.

[DOE-2](https://www.doe2.com/) is a widely used and accepted freeware building energy analysis program that can predict the energy use and cost for all types of buildings.

## Installation

`pip install -U dragonfly-doe2`

## QuickStart

```console
import dragonfly_doe2
```

## [API Documentation](http://ladybug-tools.github.io/dragonfly-doe2/docs)

## Local Development

1. Clone this repo locally
```console
git clone git@github.com:ladybug-tools/dragonfly-doe2

# or

git clone https://github.com/ladybug-tools/dragonfly-doe2
```
2. Install dependencies:
```
cd dragonfly-doe2
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

3. Run Tests:
```console
python -m pytest tests/
```

4. Generate Documentation:
```console
sphinx-apidoc -f -e -d 4 -o ./docs ./dragonfly_doe2
sphinx-build -b html ./docs ./docs/_build/docs
```
