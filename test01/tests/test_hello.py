import os
import tempfile
import unittest
from unittest import mock

from hello import greet, save_greeting, fetch_url


class TestHello(unittest.TestCase):
    def test_greet_default(self):
        self.assertEqual(greet(), "Hello, World!")

    def test_greet_uppercase(self):
        self.assertEqual(greet("Alice", uppercase=True), "HELLO, ALICE!")

    def test_save_greeting(self):
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            path = tf.name
        try:
            save_greeting("hi", path)
            with open(path, "r", encoding="utf-8") as f:
                self.assertEqual(f.read(), "hi")
        finally:
            os.remove(path)

    @mock.patch("hello.urllib.request.urlopen")
    def test_fetch_url(self, mock_urlopen):
        class Dummy:
            def __init__(self):
                self.headers = mock.Mock(get_content_charset=mock.Mock(return_value="utf-8"))

            def read(self):
                return b"content bytes"

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        mock_urlopen.return_value = Dummy()
        self.assertEqual(fetch_url("http://example.com"), "content bytes")


if __name__ == "__main__":
    unittest.main()
