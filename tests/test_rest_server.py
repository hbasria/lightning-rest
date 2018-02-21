import unittest

from lightning_rest.server import LightningRest


class TestLightningRest(unittest.TestCase):
    def setUp(self):
        self.server = LightningRest('/tmp/lightning-rpc')

    def test_home(self):
        response = self.server.home(None)

        self.assertEqual(type(response), str)
