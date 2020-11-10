import unittest
import sys

if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = './tests'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    results = runner.run(suite)
    sys.exit(int(not results.wasSuccessful()))
