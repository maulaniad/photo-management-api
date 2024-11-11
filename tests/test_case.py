from logging import disable, CRITICAL
from rich import print
from shutil import get_terminal_size

from rest_framework.test import APITestCase as _APITestCase


disable(CRITICAL)

class APITestCase(_APITestCase):
    fixtures = []

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self):
        outcome = self._outcome  # type: ignore
        test_result = outcome.result

        errors = self._get_error_list(test_result.errors)
        failures = self._get_error_list(test_result.failures)
        width = get_terminal_size().columns

        if errors:
            status = "[red]ERROR[/red]"
            width -= 1
        elif failures:
            status =  "[orange]FAIL[/orange]"
            width -= 1
        else:
            status = "[green]PASS[/green]"

        print("=" * width)
        print(f">> {status}\t{self._testMethodName}")
        print("=" * width)

    def _get_error_list(self, error_list):
        current_test = self._testMethodName
        return [error for test, error in error_list if test._testMethodName == current_test]
