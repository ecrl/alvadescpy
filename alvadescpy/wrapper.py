#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# alvadescpy/wrapper.py
# v.0.1.0
# Developed in 2019 by Travis Kessler <travis.j.kessler@gmail.com>
#
# contains `alvadesc` function, a wrapper for alvaDesc software
#

# stdlib. imports
from subprocess import check_output, PIPE, Popen
from csv import writer, QUOTE_ALL
from typing import TypeVar

# path to alvaDesc command line interface executable
ALVADESC_PATH = 'C:\\Program Files\\Alvascience\\alvaDesc\\alvaDescCLI.exe'

# custom argument variable (either str or list)
_DESC = TypeVar('_DESC', str, list)


def _sub_call(command: str) -> list:
    ''' _sub_call: calls alvaDesc via subprocess.Popen

    Args:
        command (str): command to execute

    Returns:
        list: list of lists, where each sublist is a molecule's descriptors
    '''

    try:
        p = Popen(command, stdout=PIPE, stderr=PIPE)
    except FileNotFoundError as exception:
        raise FileNotFoundError('{}\n alvaDescCLI.exe not found at {}'.format(
            exception, ALVADESC_PATH
        ))
    except Exception as exception:
        raise Exception('{}'.format(exception))
    out = p.communicate()[0].decode('utf-8').split('\r\n')[:-1]
    for idx, o in enumerate(out):
        out[idx] = o.split('\t')
    return out


def alvadesc(script: str=None, ismiles: str=None, input_file: str=None,
             inputtype: str=None, descriptors: _DESC=None, labels: bool=False,
             ecfp: bool=False, pfp: bool=False, fpsize: int=1024, fpmin: int=0,
             fpmax: int=2, count: bool=True, bits: int=2, fpoptions: str=None,
             maccsfp: bool=False, output: str=None, threads: int=None) -> list:
    ''' alvadesc: calls alvaDesc's command line interface; supports all arguments

    Args:
        script (str): path to script file containing all available options; if
            supplied, nothing else should be supplied
        ismiles (str): use a single SMILES string as input
        input_file (str): uses a set of molecules in this file as inputs
        inputtype (str): if `input_file` is supplied, this is mandatory (e.g.
            `SMILES`, `MDL`, `SYBYL`, `HYPERCHEM`)
        descriptors (str, list): `ALL` for all descriptors, or a list for
            specific descriptors
        labels (bool): if `True`, adds descriptor and molecule labels
        ecfp (bool): if `True`, calculates extended connectivity fingerprint
        pfp (bool): if `True`, calculates path fingerprint
        fpsize (int): size of hashed fingerprint (default 1024)
        fpmin (int): minimum fragment length for hashed fingerprint (default 0)
        fpmax (int): maximum fragments for hashed fingerprint (default 2)
        count (bool): if `True`, counts fragments for hashed fingerprint
            (default True)
        bits (int): bits per pattern for hashed fingerprint (default 2)
        fpoptions (str): atom types for hashed fingerprint (default Atom type,
            Aromaticity, Charge, Connectivity (total), Bond order)
        maccsfp (bool): if `True`, calculates MACCS116 fingerprint
        output (str): if not `None`, saves descriptors to this file
        threads (int): number of threads used in the calculation (default:
            equal to the maximum number of CPUs)

    Returns:
        list: if `labels` is True, returns a list of dicts, where each dict
            corresponds to a single molecule; if `labels` is False, returns a
            list of lists, where each sublist contains a molecule's descriptor
            values; if any fingerprint is calculated, no labels are included -
            returns a list of lists
    '''

    if script is not None:
        _ = _sub_call('{} --script={}'.format(ALVADESC_PATH, script))
        return

    if ismiles is not None and input_file is not None:
        raise ValueError('`ismiles` and `input_file` cannot both be supplied')

    if input_file is not None and inputtype is None:
        raise ValueError('Must supply `inputtype` if supplying `input_file`')

    command = '{}'.format(ALVADESC_PATH)

    if ismiles is not None:
        command += ' --iSMILES={}'.format(ismiles)

    if input_file is not None:
        command += ' --input={} --inputtype={}'.format(input_file, inputtype)

    if output is not None:
        command += ' --output={}'.format(output)

    if threads is not None:
        command += ' --threads={}'.format(threads)

    if ecfp is True or pfp is True or maccsfp is True:

        if sum([ecfp, pfp, maccsfp]) > 1:
            raise ValueError('Only one type of fingerprint can be calculated')

        if ecfp is True:
            command += ' --ecfp'

        if pfp is True:
            command += ' --pfp'

        if maccsfp is True:
            command += ' --maccsfp'

        command += ' --size={}'.format(fpsize)
        command += ' --min={}'.format(fpmin)
        command += ' --max={}'.format(fpmax)
        command += ' --bits={}'.format(bits)
        if count is not True:
            command += ' --count=FALSE'
        if fpoptions is not None:
            command += ' --fpoptions={}'.format(fpoptions)
        return _sub_call(command)

    if labels is True:
        command += ' --labels'

    if descriptors is not None:
        if descriptors == 'ALL':
            command += ' --descriptors=ALL'
        elif type(descriptors) is list:
            command += ' --descriptors=\"'
            for idx, desc in enumerate(descriptors):
                command += '{}'.format(desc)
                if idx != len(descriptors) - 1:
                    command += ','
            command += '\"'
        else:
            raise ValueError('Unknown `descriptors` argument: {}'.format(
                descriptors
            ))

    descriptors_raw = _sub_call(command)
    calculated_descriptors = []
    if labels is True:
        molecule = {}
        for mol in descriptors_raw[1:]:
            for idx, label in enumerate(descriptors_raw[0]):
                molecule[label] = mol[idx]
        calculated_descriptors.append(molecule)
    else:
        calculated_descriptors = [mol for mol in descriptors_raw]
    return calculated_descriptors
