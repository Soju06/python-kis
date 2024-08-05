import unittest


def test_main():
    loader = unittest.TestLoader()
    suite = loader.discover("tests/unit")

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == "__main__":
    test_main()
