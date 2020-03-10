import unittest

from base_test import BaseTest


class ManufacturingTests(BaseTest):
    """Test manufacture views"""
    def test_home(self):
        res = self.client().get(
            '/manufac/',)
        self.assertEqual(res.status_code, 302)
