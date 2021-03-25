#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# alvadescpy/functions.py
# v.0.1.1
# Developed in 2019 by Travis Kessler <travis.j.kessler@gmail.com>
#
# contains functions for common alvaDesc tasks
#

# stdlib. imports
from typing import TypeVar

# alvadescpy imports
from alvadescpy import alvadesc

# custom argument and return variables
_DESC = TypeVar('_DESC', str, list)
_RET_VAL = TypeVar('_RET_VAL', dict, list)


def smiles_to_descriptors(smiles: str, descriptors: _DESC='ALL',
                          labels: bool=True) -> _RET_VAL:
    ''' smiles_to_descriptors: returns molecular descriptors for a given
    molecule (represented by its SMILES string)

    Args:
        smiles (str): SMILES string for a given molecule
        descriptors (str, list): `ALL` for all descriptors, or list containing
            individual descriptors (str's)
        labels (bool): if `True`, labels are included in return value (dict);
            if `False`, no labels are included in return value (list)

    Returns:
        list, dict: returns a list of descriptor values if `labels` is False,
            else a dict
    '''

    return alvadesc(ismiles=smiles, descriptors=descriptors, labels=labels)[0]
