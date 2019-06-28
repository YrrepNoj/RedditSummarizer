import unittest

from src.smmry_wrapper import build_url


# from src import smmry_wrapper
# from . import smmry_wrapper
# import ../src/smmry_wrapper

class TestSmmryWrapper(unittest.TestCase):

    def test_get_reddit_client(self):
        url = build_url("api_Key", "www.reddit.com/thisIsASuperCoolPost")
        self.assertIsNotNone(url)
