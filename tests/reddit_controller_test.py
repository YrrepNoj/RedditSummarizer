import unittest

# import reddit_controller
from RedditSummarizer import reddit_controller


class TestSomething(unittest.TestCase):

    def test_get_reddit_client(self):
        self.assertIsNotNone(reddit_controller.get_reddit_client())
        self.assertEqual('foo'.upper(), 'FOO')
