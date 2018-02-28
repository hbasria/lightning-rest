import unittest


class DumyRequest():
    args = {}
    pass


class TestLightningRest(unittest.TestCase):
    def setUp(self):
        self.request = DumyRequest()

