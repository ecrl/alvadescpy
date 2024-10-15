[![UML Energy & Combustion Research Laboratory](https://sites.uml.edu/hunter-mack/files/2021/11/ECRL_final.png)](http://faculty.uml.edu/Hunter_Mack/)

# alvaDescPy: A Python wrapper for alvaDesc software

[![GitHub version](https://badge.fury.io/gh/ecrl%2Falvadescpy.svg)](https://badge.fury.io/gh/ecrl%2Falvadescpy)
[![PyPI version](https://badge.fury.io/py/alvadescpy.svg)](https://badge.fury.io/py/alvadescpy)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/ecrl/alvadescpy/master/LICENSE.txt)

alvaDescPy provides a Python wrapper for the [alvaDesc](https://www.alvascience.com/alvadesc/) molecular descriptor calculation software. It was created to allow direct access to the alvaDesc command-line interface via Python.

Important Notice:

Please note that alvaDescPy is an independent project and was not developed by Alvascience. You can find the official alvaDesc Python interface on Alvascience website: https://www.alvascience.com/python-alvadesc/.

## Installation

Installation via pip:

```
$ pip install alvadescpy
```

Installation via cloned repository:

```
$ git clone https://github.com/ecrl/alvadescpy
$ cd alvadescpy
$ pip install .
```

There are currently no additional dependencies for alvaDescPy, however it requires a valid, licensed installation of [alvaDesc](https://www.alvascience.com/alvadesc/).

## Basic Usage

alvaDescPy assumes the location of alvaDesc's command-line interface is located at your OS's default location. If alvaDesc is located in a different location, you can change the path:

```python
from alvadescpy import CONFIG

CONFIG['alvadesc_path'] = '\\path\\to\\alvaDescCLI'
```

alvaDescPy provides direct access to all alvaDesc command line arguments via the "alvadesc" function:

```python
from alvadescpy import alvadesc

# providing an XML script file
alvadesc(script='my_script.xml')

# supplying a SMILES string returns a list of descriptors
descriptors = alvadesc(ismiles='CCC', descriptors='ALL')

# a Python dictionary is returned if labels are desired
descriptors = alvadesc(ismiles='CCC', descriptors='ALL', labels=True)

# specific descriptors can be calculated
descriptors = alvadesc(ismiles='CCC', descriptors=['MW', 'AMW'], labels=True)

# input/output files (and input type) can be specified
alvadesc(
    input_file='mols.mdl',
    inputtype='MDL',
    descriptors='ALL',
    output='descriptors.txt'
)

# various fingerprints can be calculated
ecfp = alvadesc(ismiles='CCC', ecfp=True)
pfp = alvadesc(ismiles='CCC', pfp=True)
maccsfp = alvadesc(ismiles='CCC', pfp=True)

# fingerprint hash size, min/max fragment length, bits/pattern and other
#   options can be specified
ecfp = alvadesc(
    ismiles='CCC',
    ecfp=True,
    fpsize=2048,
    fpmin=1,
    fpmax=4,
    bits=4,
    fpoptions='- Additional Options -'
)

# alvaDesc uses a number of threads equal to the maximum number of CPUs, but
#   can be changed
descriptors=alvadesc(ismiles='CCC', descriptors='ALL', threads=4)
```

alvaDescPy also provides the "smiles_to_descriptors" function:

```python
from alvadescpy import smiles_to_descriptors

# returns a list of descriptor values
descriptors = smiles_to_descriptors('CCC', descriptors='ALL')

# returns a dictionary of descriptor labels, values
descriptors = smiles_to_descriptors('CCC', descriptors='ALL', labels=True)

# returns a dictionary containing MW, AMW labels, values
descriptors = smiles_to_descriptors(
    'CCC',
    descriptors=['MW', 'AMW'],
    labels=True
)
```

## Contributing, Reporting Issues and Other Support

To contribute to alvaDescPy, make a pull request. Contributions should include tests for new features added, as well as extensive documentation.

To report problems with the software or feature requests, file an issue. When reporting problems, include information such as error messages, your OS/environment and Python version.

For additional support/questions, contact Travis Kessler (Travis_Kessler@student.uml.edu).
