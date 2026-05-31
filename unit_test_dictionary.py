"""
unit_test_dictionary.py

Manual unit tests for the dictionary demo validation logic.

This file is designed to be called from the Streamlit app through a
"Tests" menu option. It does not use pytest because the goal is to show
the test results directly inside the Streamlit interface.

The tests validate the behavior of the dictionary numeric validation
function used before inserting/updating dictionary values.
"""

from dataclasses import dataclass
from typing import Any

import streamlit as st # will be render with stremlit
#Streamlit is a Python framework used to build simple web apps quickly, especially for data projects, 
# dashboards, machine learning demos, and internal tools. Instead of writing HTML, CSS, JavaScript, 
# or backend routes, you write normal Python code and use commands like `st.title()`, `st.write()`, 
# `st.button()`, and `st.text_input()` to create the interface. Every time the user interacts with the page, 
# Streamlit reruns the script from top to bottom, so state that must survive between interactions is usually 
# stored in `st.session_state`. It is useful for learning because you can focus on Python logic first, 
# then display inputs, outputs, charts, tables, and test results directly in the browser.


# Import the function that the code will test.
from tools import validate_numeric_value


@dataclass
class TestCase:
    """
    Represents one validation test case.

    Attributes
    ----------
    name:
        Human-readable name of the test.

    raw_value:
        Value sent to the validation function as if it came from user input.

    input_type:
        Selected input type from the Streamlit selectbox.

    sign:
        Selected sign validation rule.

    expected_value:
        The expected converted value. Use None when expecting validation failure.

    expected_error:
        The expected error message. Use None when expecting success.
    """

    name: str
    raw_value: str
    input_type: str
    sign: str
    expected_value: int | float | None
    expected_error: str | None


@dataclass
class TestResult:
    """
    Stores the result of one executed test.

    This structure makes it easy to render results in Streamlit later.
    """

    name: str
    passed: bool
    expected_value: Any
    actual_value: Any
    expected_error: Any
    actual_error: Any


def run_validation_tests() -> list[TestResult]:
    """
    Run all validation tests for validate_numeric_value().

    Returns
    -------
    list[TestResult]
        A list containing the result of each test case.
    """

    test_cases = [
        TestCase(
            name="Valid integer",
            raw_value="10",
            input_type="int",
            sign="either",
            expected_value=10,
            expected_error=None,
        ),
        TestCase(
            name="Invalid integer with decimal",
            raw_value="10.5",
            input_type="int",
            sign="either",
            expected_value=None,
            expected_error="'10.5' is not a valid int value.",
        ),
        TestCase(
            name="Valid float",
            raw_value="10.5",
            input_type="float",
            sign="either",
            expected_value=10.5,
            expected_error=None,
        ),
        TestCase(
            name="Valid negative float when sign is either",
            raw_value="-3.75",
            input_type="float",
            sign="either",
            expected_value=-3.75,
            expected_error=None,
        ),
        TestCase(
            name="Reject negative value when sign is positive",
            raw_value="-5",
            input_type="float",
            sign="positive",
            expected_value=None,
            expected_error="The value must be greater than or equal to 0.",
        ),
        TestCase(
            name="Reject positive value when sign is negative",
            raw_value="5",
            input_type="float",
            sign="negative",
            expected_value=None,
            expected_error="The value must be less than or equal to 0.",
        ),
        TestCase(
            name="Valid positive type",
            raw_value="25",
            input_type="positive",
            sign="either",
            expected_value=25.0,
            expected_error=None,
        ),
        TestCase(
            name="Reject negative positive-type value",
            raw_value="-25",
            input_type="positive",
            sign="either",
            expected_value=None,
            expected_error="The value must be positive.",
        ),
        TestCase(
            name="Valid percentage",
            raw_value="0.25",
            input_type="percentage",
            sign="either",
            expected_value=0.25,
            expected_error=None,
        ),
        TestCase(
            name="Reject percentage above 1",
            raw_value="1.25",
            input_type="percentage",
            sign="either",
            expected_value=None,
            expected_error="The percentage must be between 0 and 1. Example: use 0.25 for 25%.",
        ),
        TestCase(
            name="Reject negative percentage",
            raw_value="-0.10",
            input_type="percentage",
            sign="either",
            expected_value=None,
            expected_error="The percentage cannot be negative.",
        ),
        TestCase(
            name="Reject empty value",
            raw_value="",
            input_type="int",
            sign="either",
            expected_value=None,
            expected_error="The numeric value cannot be empty.",
        ),
        TestCase(
            name="Reject spaces only",
            raw_value="   ",
            input_type="float",
            sign="either",
            expected_value=None,
            expected_error="The numeric value cannot be empty.",
        ),
        TestCase(
            name="Reject unsupported input type",
            raw_value="10",
            input_type="money",
            sign="either",
            expected_value=None,
            expected_error="Invalid input type: money",
        ),
        TestCase(
            name="Reject unsupported sign rule",
            raw_value="10",
            input_type="int",
            sign="zero_only",
            expected_value=None,
            expected_error="Invalid sign rule: zero_only",
        ),
    ]

    results: list[TestResult] = []

    for test in test_cases:
        actual_value, actual_error = validate_numeric_value(
            raw_value=test.raw_value,
            input_type=test.input_type,
            sign=test.sign,
        )

        passed = (
            actual_value == test.expected_value
            and actual_error == test.expected_error
        )

        results.append(
            TestResult(
                name=test.name,
                passed=passed,
                expected_value=test.expected_value,
                actual_value=actual_value,
                expected_error=test.expected_error,
                actual_error=actual_error,
            )
        )

    return results


def render() -> None:
    """
    Render the test page inside Streamlit.

    This function can be registered in main.py like any other page.
    """

    st.title("Dictionary Unit Tests")

    st.markdown(
        """
        This page runs manual unit tests for the dictionary validation logic.

        The goal is to confirm that numeric values are accepted or rejected
        correctly before they are inserted into the dictionary.
        """
    )

    if st.button("Run dictionary tests", key="btn_run_dictionary_tests"):
        results = run_validation_tests()

        total_tests = len(results)
        passed_tests = sum(1 for result in results if result.passed)
        failed_tests = total_tests - passed_tests

        st.subheader("Test Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total tests", total_tests)
        col2.metric("Passed", passed_tests)
        col3.metric("Failed", failed_tests)

        if failed_tests == 0:
            st.success("All dictionary validation tests passed.")
        else:
            st.error(f"{failed_tests} dictionary validation test(s) failed.")

        st.subheader("Detailed Results")

        for result in results:
            if result.passed:
                st.success(f"PASS: {result.name}")

                with st.expander(f"Details: {result.name}"): # tudo que estiver indentado dentro do with será renderizado dentro do st.expander.
                    st.write("Expected value:", result.expected_value)
                    st.write("Actual value:", result.actual_value)
                    st.write("Expected error:", result.expected_error)
                    st.write("Actual error:", result.actual_error)

            else:
                st.error(f"FAIL: {result.name}")

                with st.expander(f"Error details: {result.name}", expanded=True):
                    st.write("Expected value:", result.expected_value)
                    st.write("Actual value:", result.actual_value)
                    st.write("Expected error:", result.expected_error)
                    st.write("Actual error:", result.actual_error)