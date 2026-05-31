
def validate_numeric_value(
    raw_value: str,
    input_type: str,
    sign: str = "either",
) -> tuple[int | float | None, str | None]:
    """
    Validate and convert a numeric value entered by the user.

    Parameters
    ----------
    raw_value:
        The value typed by the user in the Streamlit text input.

    input_type:
        Defines how the value should be interpreted.
        Accepted values:
        - "int": whole number only
        - "float": decimal number allowed
        - "positive": number must be greater than or equal to zero
        - "percentage": decimal percentage, usually between 0 and 1

    sign:
        Defines the allowed sign of the number.
        Accepted values:
        - "either": positive, negative, or zero
        - "positive": value must be greater than or equal to zero
        - "negative": value must be less than or equal to zero

    Returns
    -------
    tuple[int | float | None, str | None]
        First item:
            The converted value if valid, otherwise None.

        Second item:
            The error message if invalid, otherwise None.

    Why this function does not use while True
    -----------------------------------------
    In terminal programs, we often use loops to keep asking for input.
    In Streamlit, the app reruns automatically after user interaction.
    So the correct pattern is:
    - read the current input once
    - validate it once
    - show success or error
    """

    # Remove extra spaces before validating.
    raw_value = raw_value.strip()

    # Empty values should not be converted.
    if not raw_value:
        return None, "The numeric value cannot be empty."

    # Validate supported input types early.
    # This protects the function from incorrect internal usage.
    allowed_input_types = {"int", "float", "positive", "percentage"}
    if input_type not in allowed_input_types:
        return None, f"Invalid input type: {input_type}"

    # Validate supported sign rules early.
    allowed_signs = {"either", "positive", "negative"}
    if sign not in allowed_signs:
        return None, f"Invalid sign rule: {sign}"

    try:
        # For int, we validate more strictly.
        # int("10") is valid, but int("10.5") would fail.
        if input_type == "int":
            converted_value = int(raw_value)
        else:
            converted_value = float(raw_value)

    except ValueError:
        return None, f"'{raw_value}' is not a valid {input_type} value."

    except OverflowError:
        return None, "The number is too large."

    # Apply generic sign validation.
    if sign == "positive" and converted_value < 0:
        return None, "The value must be greater than or equal to 0."

    if sign == "negative" and converted_value > 0:
        return None, "The value must be less than or equal to 0."

    # Apply specific validation for the positive type.
    if input_type == "positive" and converted_value < 0:
        return None, "The value must be positive."

    # Apply specific validation for percentage values.
    #
    # In this version, percentages are stored as decimals:
    # 0.25 means 25%
    # 1.00 means 100%
    #
    # You can allow values above 1 if you want, but for clean validation,
    # this version blocks them.
    if input_type == "percentage":
        if converted_value < 0:
            return None, "The percentage cannot be negative."

        if converted_value > 1:
            return None, "The percentage must be between 0 and 1. Example: use 0.25 for 25%."

    return converted_value, None
