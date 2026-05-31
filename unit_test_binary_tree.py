"""
unit_test_binary_tree.py

Manual unit tests for the Binary Tree mathematical expression parser.

This file is designed to be called from the Streamlit app through a
"Tests" menu option. It runs a set of fixed standard tests and generates
N random tests dynamically to ensure the parser's robustness.
"""

import random
from dataclasses import dataclass
from typing import Any
import streamlit as st

# Import the validation function to check the user input for N random tests
from tools import validate_numeric_value

# Import the parser classes and evaluation function
from app_binary_tree_parser import Parser, evaluate


@dataclass
class TestCase:
    """
    Represents one parser test case.

    Attributes
    ----------
    name: Human-readable name of the test.
    expression: The mathematical expression string to be parsed.
    expected_value: The expected integer result. Use None if expecting an error.
    expected_error: The expected error message. Use None if expecting success.
    """
    name: str
    expression: str
    expected_value: int | None
    expected_error: str | None


@dataclass
class TestResult:
    """
    Stores the result of one executed test to be rendered in Streamlit.
    """
    name: str
    expression: str
    passed: bool
    expected_value: Any
    actual_value: Any
    expected_error: Any
    actual_error: Any


def generate_random_expression(depth: int = 0) -> str:
    """
    Recursively generates a valid random mathematical expression string.
    Uses only integers, addition ('+'), and multiplication ('*').

    Args:
        depth (int): Current recursion depth to prevent infinite loops.

    Returns:
        str: A randomly generated mathematical expression.
    """
    # Limit the depth to avoid excessively long expressions
    if depth > 3 or random.random() > 0.7:
        return str(random.randint(1, 50))

    op = random.choice(['+', '*'])
    left = generate_random_expression(depth + 1)
    right = generate_random_expression(depth + 1)

    # Randomly add parentheses to test precedence parsing
    if random.random() > 0.5:
        return f"({left}{op}{right})"
    return f"{left}{op}{right}"


def run_parser_tests(num_random_tests: int) -> list[TestResult]:
    """
    Executes both the fixed standard tests and the dynamically generated random tests.

    Args:
        num_random_tests (int): The number of random tests to generate.

    Returns:
        list[TestResult]: A list containing the results of all executed tests.
    """
    # 10 Standard Fixed Tests (covering base cases, precedence, and expected errors)
    test_cases = [
        TestCase("Simple addition", "5+5", 10, None),
        TestCase("Simple multiplication", "4*3", 12, None),
        TestCase("Standard precedence", "2+3*4", 14, None),
        TestCase("Parentheses precedence", "(2+3)*4", 20, None),
        TestCase("Single number", "42", 42, None),
        TestCase("Long expression", "10+(5+5+5)*(5+4+1)", 160, None),
        TestCase("Nested parentheses", "((2+2)*(3+3))", 24, None),
        TestCase("Error: Unclosed parenthesis", "(5+5", None, "Missing closing parenthesis"),
        TestCase("Error: Unexpected token (minus)", "5-5", None, "Unexpected token: -"),
        TestCase("Error: Invalid characters", "a+b", None, "Unexpected token: a"),
    ]

    # Generate and append N random tests
    for i in range(num_random_tests):
        expr = generate_random_expression()
        try:
            # Use Python's native eval() to determine the correct expected result
            expected = eval(expr)
            test_cases.append(TestCase(f"Random Test {i+1}", expr, expected, None))
        except Exception:
            # Skip if the generated expression is somehow invalid for eval
            continue

    results: list[TestResult] = []

    # Execute all collected test cases
    for test in test_cases:
        actual_value = None
        actual_error = None

        try:
            # Attempt to parse and evaluate the expression
            parser = Parser(test.expression)
            tree = parser.parse_expr()
            actual_value = evaluate(tree)
        except Exception as e:
            # Catch any parsing or evaluation errors
            actual_error = str(e)

        # A test passes if both the value and the error match the expectations
        passed = (
            actual_value == test.expected_value
            and actual_error == test.expected_error
        )

        results.append(
            TestResult(
                name=test.name,
                expression=test.expression,
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
    Renders the test page inside the Streamlit application.
    This function should be registered in the PAGES dictionary in main.py.
    """
    st.title("Binary Tree Parser Unit Tests")

    st.markdown(
        """
        This page runs unit tests for the Binary Tree mathematical expression parser.

        It executes **10 fixed standard tests** (including error handling) and allows you 
        to generate **N random tests** to validate the robustness of the parsing logic.
        """
    )

    st.subheader("Test Configuration")

    # Input for the number of random tests to generate
    n_tests_input = st.text_input(
        "How many random tests do you want to generate?",
        value="5",
        key="input_n_random_tests"
    )

    if st.button("Run Parser Tests", key="btn_run_tree_tests"):
        # Validate the input using the imported tool
        # We expect an integer that is positive (>= 0)
        num_tests, error_msg = validate_numeric_value(
            raw_value=n_tests_input,
            input_type="int",
            sign="positive"
        )

        if error_msg:
            st.error(f"Input Error: {error_msg}")
        else:
            # Execute the tests with the validated integer
            results = run_parser_tests(num_tests)

            total_tests = len(results)
            passed_tests = sum(1 for result in results if result.passed)
            failed_tests = total_tests - passed_tests

            st.subheader("Test Summary")

            # Display metrics in columns
            col1, col2, col3 = st.columns(3)
            col1.metric("Total tests", total_tests)
            col2.metric("Passed", passed_tests)
            col3.metric("Failed", failed_tests)

            if failed_tests == 0:
                st.success("All parser tests passed successfully!")
            else:
                st.error(f"{failed_tests} parser test(s) failed.")

            st.subheader("Detailed Results")

            # Render the details for each test case
            for result in results:
                if result.passed:
                    st.success(f"PASS: {result.name} | Expression: `{result.expression}`")
                    with st.expander(f"Details: {result.name}"):
                        st.write("**Expected value:**", result.expected_value)
                        st.write("**Actual value:**", result.actual_value)
                        st.write("**Expected error:**", result.expected_error)
                        st.write("**Actual error:**", result.actual_error)
                else:
                    st.error(f"FAIL: {result.name} | Expression: `{result.expression}`")
                    with st.expander(f"Error details: {result.name}", expanded=True):
                        st.write("**Expected value:**", result.expected_value)
                        st.write("**Actual value:**", result.actual_value)
                        st.write("**Expected error:**", result.expected_error)
                        st.write("**Actual error:**", result.actual_error)