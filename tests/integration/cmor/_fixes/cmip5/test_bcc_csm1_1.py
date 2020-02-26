"""Test Access1-0 fixes."""
import unittest

from esmvalcore.cmor._fixes.cmip5.bcc_csm1_1 import Tos
from esmvalcore.cmor.fix import Fix


class TestTos(unittest.TestCase):
    """Test tos fixes."""
    def test_get(self):
        """Test fix get"""
        self.assertListEqual(
            Fix.get_fixes('CMIP5', 'BCC-CSM1-1', 'Amon', 'tos'), [Tos(None)])
