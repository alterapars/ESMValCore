"""Test MPI-ESM-LR fixes."""
import unittest

from cf_units import Unit
from iris.cube import Cube

from esmvalcore.cmor._fixes.cmip5.mpi_esm_lr import Pctisccp
from esmvalcore.cmor.fix import Fix


class TestPctisccp2(unittest.TestCase):
    """Test Pctisccp2 fixes."""
    def setUp(self):
        """Prepare tests."""
        self.cube = Cube([1.0], var_name='pctisccp', units='J')
        self.fix = Pctisccp(None)

    def test_get(self):
        """Test fix get"""
        self.assertListEqual(
            Fix.get_fixes('CMIP5', 'MPI-ESM-LR', 'Amon', 'pctisccp'),
            [Pctisccp(None)])

    def test_fix_data(self):
        """Test data fix."""
        cube = self.fix.fix_data(self.cube)
        self.assertEqual(cube.data[0], 100)
        self.assertEqual(cube.units, Unit('J'))
