#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# alvadescpy/wrapper.py
# v.0.1.2
# Developed in 2019 by Travis Kessler <travis.j.kessler@gmail.com>
#
# contains `alvadesc` function, a wrapper for alvaDesc software
#

# stdlib. imports
from subprocess import PIPE, Popen
from typing import TypeVar
import platform

# path to alvaDesc command line interface executable
CONFIG = {
    'alvadesc_path': None
}
plt = platform.system()
if plt == 'Windows':
    CONFIG['alvadesc_path'] = 'C:\\Program Files\\Alvascience\\alvaDesc\\\
alvaDescCLI.exe'
elif plt == 'Darwin':
    CONFIG['alvadesc_path'] = '/Applications/alvaDesc.app/Contents/MacOS/\
alvaDescCLI'
elif plt == 'Linux':
    CONFIG['alvadesc_path'] = '/usr/bin/alvaDescCLI'
else:
    raise RuntimeError('Unknown/unsupported operating system: {}'.format(plt))

# custom argument variable (either str or list)
str_or_list = TypeVar('str_or_list', str, list)


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
        raise FileNotFoundError('{}\n alvaDescCLI not found at {}'.format(
            exception, CONFIG['alvadesc_path']
        ))
    except Exception as exception:
        raise Exception('{}'.format(exception))
    return p.communicate()[0].decode('utf-8')


def alvadesc(script: str = None, ismiles: str = None, input_file: str = None,
             inputtype: str = None, descriptors: str_or_list = None,
             labels: bool = False, ecfp: bool = False, pfp: bool = False,
             fpsize: int = 1024, fpmin: int = 0, fpmax: int = 2,
             count: bool = True, bits: int = 2, fpoptions: str = None,
             maccsfp: bool = False, output: str = None,
             threads: int = None) -> list:
    ''' alvadesc: calls alvaDesc's command line interface; supports all
    arguments

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
        _ = _sub_call(' --script={}'.format(script))
        return

    if ismiles is not None and input_file is not None:
        raise ValueError('`ismiles` and `input_file` cannot both be supplied')

    if input_file is not None and inputtype is None:
        raise ValueError('Must supply `inputtype` if supplying `input_file`')

    command = [CONFIG['alvadesc_path']]

    if ismiles is not None:
        command.append('--iSMILES={}'.format(ismiles))

    if input_file is not None:
        command.append('--input={}'.format(input_file))
        command.append('--inputtype={}'.format(inputtype))

    if output is not None:
        command.append('--output={}'.format(output))

    if threads is not None:
        command.append('--threads={}'.format(threads))

    if ecfp is True or pfp is True or maccsfp is True:

        if sum([ecfp, pfp, maccsfp]) > 1:
            raise ValueError('Only one type of fingerprint can be calculated')

        if ecfp is True:
            command.append('--ecfp')

        if pfp is True:
            command.append('--pfp')

        if maccsfp is True:
            command.append('--maccsfp')

        command.append('--size={}'.format(fpsize))
        command.append('--min={}'.format(fpmin))
        command.append('--max={}'.format(fpmax))
        command.append('--bits={}'.format(bits))
        if count is not True:
            command.append('--count=FALSE')
        if fpoptions is not None:
            command.append('--fpoptions={}'.format(fpoptions))

    if labels is True:
        command.append('--labels')

    if descriptors is not None:
        if descriptors == 'ALL':
            command.append('--descriptors=ALL')
        elif type(descriptors) is list:
            cmd = '--descriptors='
            for idx, desc in enumerate(descriptors):
                cmd += '{}'.format(desc)
                if idx != len(descriptors) - 1:
                    cmd += ','
            # cmd += ''
            command.append(cmd)
        else:
            raise ValueError('Unknown `descriptors` argument: {}'.format(
                descriptors
            ))

    descriptors_raw = _sub_call(command).split('\n')[:-1]
    val_start_idx = 0
    if labels is True:
        desc_names = descriptors_raw[0].split('\t')
        val_start_idx = 1
    desc_vals = []
    for d in descriptors_raw[val_start_idx:]:
        _vals = d.split('\t')
        for vidx, v in enumerate(_vals):
            try:
                _vals[vidx] = float(v)
            except ValueError:
                continue
        desc_vals.append(_vals)
    if labels is False:
        return desc_vals
    desc_dicts = []
    for mol in desc_vals:
        moldict = {}
        for nidx, name in enumerate(desc_names):
            moldict[name] = mol[nidx]
        desc_dicts.append(moldict)
    return desc_dicts
