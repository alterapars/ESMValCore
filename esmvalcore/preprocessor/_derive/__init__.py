"""Automatically derive variables."""

import importlib
import logging
from copy import deepcopy
from pathlib import Path

import iris

logger = logging.getLogger(__name__)


def _get_all_derived_variables():
    """Get all possible derived variables.

    Returns
    -------
    dict
        All derived variables with `cmor_name` (keys) and the associated
        python classes (values).

    """
    derivers = {}
    for path in Path(__file__).parent.glob('[a-z]*.py'):
        cmor_name = path.stem
        module = importlib.import_module(
            f'esmvalcore.preprocessor._derive.{cmor_name}')
        derivers[cmor_name] = getattr(module, 'DerivedVariable')
    return derivers


ALL_DERIVED_VARIABLES = _get_all_derived_variables()

__all__ = list(ALL_DERIVED_VARIABLES)


def get_required(cmor_name, project):
    """Return all required variables for derivation.

    Get all information (at least `var_name`) required for derivation.

    Parameters
    ----------
    cmor_name : str
        name of the variable to derive.
    project : str
        `project` of the variable to derive.

    Returns
    -------
    list
        List of dictionaries (including at least the key `cmor_name`).

    """
    if cmor_name not in ALL_DERIVED_VARIABLES:
        raise NotImplementedError(
            f"Cannot derive variable '{cmor_name}', no derivation script "
            f"available")
    DerivedVariable = ALL_DERIVED_VARIABLES[cmor_name]  # noqa: N806
    variables = deepcopy(DerivedVariable().required(project))
    return variables


def derive(cubes, cmor_name, short_name, long_name, units, standard_name=None):
    """Derive variable.

    Parameters
    ----------
    cubes: iris.cube.CubeList
        Includes all the needed variables for derivation defined in
        :func:`get_required`.
    cmor_name: str
        cmor_name
    long_name: str
        long_name
    units: str
        units
    standard_name: str, optional
        standard_name

    Returns
    -------
    iris.cube.Cube
        The new derived variable.

    """
    if short_name == cubes[0].var_name:
        return cubes[0]

    cubes = iris.cube.CubeList(cubes)

    # Derive variable
    DerivedVariable = ALL_DERIVED_VARIABLES[cmor_name.lower()]  # noqa: N806
    try:
        cube = DerivedVariable().calculate(cubes)
    except Exception as exc:
        msg = (f"Derivation of variable '{cmor_name}' failed. If you used "
               f"the option '--skip-nonexistent' for running your recipe, "
               f"this might be caused by missing input data for derivation "
               f"('{cmor_name}' needs the variables "
               f"{DerivedVariable().required}).")
        raise ValueError(msg) from exc

    # Set standard attributes
    cube.var_name = short_name
    cube.standard_name = standard_name if standard_name else None
    cube.long_name = long_name
    cube.units = units
    for temp in cubes:
        if 'source_file' in temp.attributes:
            cube.attributes['source_file'] = temp.attributes['source_file']

    return cube
