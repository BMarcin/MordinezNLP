import unittest
import sys

# pre initialize ENV
import stanza
stanza.download('en')

if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = './tests'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    results = runner.run(suite)
    sys.exit(int(not results.wasSuccessful()))
