import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


def run_tests():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django.setup()

    TestRunner = get_runner(settings)

    # And then we run tests and return the results.
    test_runner = TestRunner(verbosity=2, interactive=True)
    failures = test_runner.run_tests(['tests'])
    sys.exit(failures)


if __name__ == '__main__':
    run_tests()
