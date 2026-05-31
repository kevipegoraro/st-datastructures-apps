#decorrator explanation:
from dataclasses import dataclass


@dataclass
class TestResult:
    name: str
    passed: bool
    expected_value: object
    actual_value: object
    expected_error: object
    actual_error: object

#é iaugal a
class TestResult:
    def __init__(
        self,
        name,
        passed,
        expected_value,
        actual_value,
        expected_error,
        actual_error,
    ):
        self.name = name
        self.passed = passed
        self.expected_value = expected_value
        self.actual_value = actual_value
        self.expected_error = expected_error
        self.actual_error = actual_error