"""
Pytest functions for testing potentials and eigenvalues of
application examples. Calculations of reference potential for both potential
square wells and for the harmonic oscillator are based on known analytic
solution. Calculations of reference eigenvalues for infinite square well and
the harmonic oscillator are based on known analytic solution. Other reference
files were numerically calculated.
"""
import numpy as np
import pytest
import modules

EXAMPLES = ['infinite_potential_well', 'finite_potential_well',
            'double_linear', 'harmonic_potential_well', 'double_cubic_spline',
            'asym_potential_well']

_TOLERANCE = 1e-15


@pytest.mark.parametrize("example", EXAMPLES)
def test_potential(example):
    """
    Tests if computet potentials match the reference potentials. It is required
    that input file schrodinger.inp is in same directory as the reference file
    (Here: application_examples).
    """
    path = "./application_examples/{}/".format(example)
    ref_potential = np.loadtxt(path + "potential.ref")
    parameter = modules.in_and_out.read_inp(path)
    intfunc = modules.interpolator.interpolator(parameter['x_decl'],
                                                parameter['y_decl'],
                                                parameter['interpol_method'])
    x_points = np.linspace(parameter['xMin'],
                           parameter['xMax'],
                           parameter['nPoint'])
    comp_potential = [intfunc(ii) for ii in x_points]
    assert np.all(ref_potential - comp_potential < _TOLERANCE)


@pytest.mark.parametrize("example", EXAMPLES)
def test_energy(example):
    """
    Tests if computed energies match the reference energy eigenvalues. It is
    required that input file schrodinger.inp is in same directory as the
    reference file (Here: application_examples).
    """
    path = "./application_examples/{}/".format(example)
    ref_energy = np.loadtxt(path + "energy.ref")
    parameter = modules.in_and_out.read_inp(path)
    intfunc = modules.interpolator.interpolator(parameter['x_decl'],
                                                parameter['y_decl'],
                                                parameter['interpol_method'])
    comp_energy = modules.solver.solv(parameter['xMin'],
                                      parameter['xMax'],
                                      parameter['nPoint'],
                                      parameter['mass'],
                                      intfunc,
                                      parameter['first'],
                                      parameter['last'])[0]
    np.allclose(ref_energy, comp_energy)
