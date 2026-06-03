import math
import streamlit as st


MAX_N = 99_999


def validate_n(n):
    '''
    Validate the user's input value for N.

    Parameters:
        n (int): The value entered by the user through the Streamlit interface.

    Returns:
        tuple[bool, str]: A tuple containing:
            - bool: True if the value is valid, False otherwise.
            - str: A message explaining the validation result.

    Validation Rules:
        - N must be an integer.
        - N must be positive.
        - N must be less than 100000.
    '''

    # Check that the input is an integer.
    if not isinstance(n, int):
        return False, "N must be an integer."

    # Check that N is positive.
    if n < 1:
        return False, "N must be a positive integer."

    # Check that N is less than 100000, as required by the project prompt.
    if n >= 100_000:
        return False, "N must be less than 100000."

    # If every check passes, the input is valid.
    return True, "Valid input."


@st.cache_data
def generate_primes_up_to(n):
    '''
    Generate all prime numbers less than or equal to n.

    Parameters:
        n (int): The largest number that may be included in the prime list.

    Returns:
        list[int]: A list of all prime numbers from 2 through n, inclusive.

    Algorithm:
        This function uses an optimized Sieve of Eratosthenes.

        Efficiency Details:
        - The number 2 is handled separately because it is the only even prime.
        - Only odd numbers are stored in the sieve, which saves memory.
        - Multiples begin at p * p because smaller multiples were already marked
          by smaller prime factors.
        - The sieve only loops up to sqrt(n), which avoids unnecessary work.

    Notes:
        Although this is a sieve instead of direct trial division, it uses the
        same idea as wheel optimization by immediately removing all even numbers
        from consideration.
    '''

    # If n is less than 2, there are no prime numbers.
    if n < 2:
        return []

    # Start the result list with 2 because 2 is the only even prime number.
    primes = [2]

    # If n is exactly 2, the only prime number up to n is 2.
    if n == 2:
        return primes

    # The odd-only sieve represents odd numbers starting at 3.
    # Index 0 represents 3, index 1 represents 5, index 2 represents 7, and so on.
    # The formula for the number represented by index i is: 2 * i + 3.
    sieve_size = ((n - 3) // 2) + 1

    # A bytearray is memory-efficient and fast for marking prime/composite values.
    # Value 1 means "currently believed to be prime."
    # Value 0 means "known to be composite."
    is_prime = bytearray(b"\x01") * sieve_size

    # We only need to cross out multiples for base primes up to sqrt(n).
    limit = math.isqrt(n)

    # Convert the numeric limit into the last odd-only sieve index that matters.
    max_index = (limit - 3) // 2

    # Loop through possible odd prime indexes.
    for index in range(max_index + 1):

        # Continue only if this index still represents a prime number.
        if is_prime[index]:

            # Convert the index back into its actual odd number value.
            prime = (2 * index) + 3

            # Start crossing out at prime * prime.
            # Any smaller composite multiple already has a smaller prime factor.
            start_number = prime * prime

            # Convert start_number into the corresponding odd-only sieve index.
            start_index = (start_number - 3) // 2

            # Because the sieve stores only odd numbers, adding prime * 2 in the
            # real number line is equal to adding prime in the odd-only index line.
            step = prime

            # Mark every odd multiple of this prime as composite.
            is_prime[start_index::step] = b"\x00" * (((sieve_size - 1 - start_index) // step) + 1)

    # Add every odd number that is still marked as prime to the result list.
    for index, prime_flag in enumerate(is_prime):

        # If prime_flag is 1, the represented odd number is prime.
        if prime_flag:

            # Convert the odd-only index back into the actual prime number.
            prime_number = (2 * index) + 3

            # Store the prime number in the result list.
            primes.append(prime_number)

    # Return the complete list of primes up to n.
    return primes


@st.cache_data
def count_primes_up_to(n):
    '''
    Count how many prime numbers are less than or equal to n.

    Parameters:
        n (int): The largest number to check for primes.

    Returns:
        int: The number of prime numbers from 2 through n, inclusive.

    Strategy:
        - Generate all prime numbers up to n using an optimized sieve.
        - Return the length of the generated prime list.
    '''

    # Generate all primes up to n and count them by using len().
    return len(generate_primes_up_to(n))


def format_prime_preview(primes, preview_size=25):
    '''
    Format a readable preview of the prime number list.

    Parameters:
        primes (list[int]): The list of prime numbers to preview.
        preview_size (int): The maximum number of primes to show before shortening.

    Returns:
        str: A formatted string showing either all primes or a shortened preview.

    Behavior:
        - If the list is small, every prime is shown.
        - If the list is large, only the first preview_size primes are shown.
    '''

    # If there are no primes, return a clear message.
    if not primes:
        return "No prime numbers are less than or equal to this value."

    # If the number of primes is small enough, show the entire list.
    if len(primes) <= preview_size:
        return ", ".join(str(prime) for prime in primes)

    # Otherwise, show only the beginning of the list to keep the UI clean.
    preview = ", ".join(str(prime) for prime in primes[:preview_size])

    # Add a note explaining that the list continues.
    return f"{preview}, ..."


def render_page_setup():
    '''
    Configure the Streamlit page settings.

    Parameters:
        None

    Returns:
        None

    Purpose:
        This function sets the page title, page icon, layout, and sidebar state.
    '''

    # Set page configuration before drawing the rest of the app.
    st.set_page_config(
        page_title="Prime Counter",
        page_icon="🔢",
        layout="centered",
        initial_sidebar_state="expanded",
    )


def render_header():
    '''
    Display the main title and introduction for the app.

    Parameters:
        None

    Returns:
        None

    Purpose:
        This function gives the user a clear explanation of what the app does.
    '''

    # Display the main title of the application.
    st.title("🔢 Prime Counter")

    # Explain the task in simple language.
    st.write(
        "Enter a positive integer **N** less than **100000**, "
        "and this app will count how many prime numbers are less than or equal to **N**."
    )

    # Add a short definition so users understand the mathematical meaning.
    st.info(
        "A prime number is a whole number greater than 1 that has exactly two positive divisors: "
        "1 and itself."
    )


def render_sidebar():
    '''
    Display helpful information in the sidebar.

    Parameters:
        None

    Returns:
        None

    Purpose:
        This function improves the user interface by showing rules, examples,
        and algorithm information without cluttering the main page.
    '''

    # Add a sidebar title.
    st.sidebar.title("About This App")

    # Display the input rules.
    st.sidebar.subheader("Input Rules")
    st.sidebar.write("- N must be a positive integer.")
    st.sidebar.write("- N must be less than 100000.")
    st.sidebar.write("- Valid range: 1 to 99999.")

    # Display example outputs to help users understand expected behavior.
    st.sidebar.subheader("Examples")
    st.sidebar.write("- N = 10 → 4 primes: 2, 3, 5, 7")
    st.sidebar.write("- N = 20 → 8 primes")
    st.sidebar.write("- N = 100 → 25 primes")

    # Display a short algorithm summary.
    st.sidebar.subheader("Algorithm")
    st.sidebar.write(
        "Uses an optimized Sieve of Eratosthenes that stores only odd numbers "
        "for better speed and memory usage."
    )


def render_input_section():
    '''
    Render the user input controls.

    Parameters:
        None

    Returns:
        tuple[int, bool]: A tuple containing:
            - int: The selected value of N.
            - bool: Whether the user clicked the calculation button.

    UI Details:
        - A number input is used so users cannot type invalid text.
        - Minimum and maximum values are enforced directly in the widget.
        - A button lets the user choose when to run the calculation.
    '''

    # Create a visual section heading.
    st.subheader("Enter Your Number")

    # Use Streamlit's number_input to prevent non-integer text input.
    n = st.number_input(
        label="Choose a positive integer N less than 100000:",
        min_value=1,
        max_value=MAX_N,
        value=100,
        step=1,
        help="The app will count all prime numbers from 2 through N.",
    )

    # Add a button so the action is clear to the user.
    calculate_clicked = st.button("Count Primes", type="primary")

    # Return the selected number and whether the button was clicked.
    return int(n), calculate_clicked


def render_results(n):
    '''
    Calculate and display the prime-counting results.

    Parameters:
        n (int): The validated positive integer entered by the user.

    Returns:
        None

    Output:
        - Displays the count of prime numbers up to N.
        - Displays the largest prime less than or equal to N when one exists.
        - Displays a preview of the prime list.
    '''

    # Validate the input before doing any calculation.
    is_valid, validation_message = validate_n(n)

    # If validation fails, show an error and stop this function safely.
    if not is_valid:
        st.error(validation_message)
        return

    # Generate the prime list once so both the count and preview can reuse it.
    primes = generate_primes_up_to(n)

    # Count the prime numbers by checking the list length.
    prime_count = len(primes)

    # Create a success message confirming the calculation is complete.
    st.success(f"Calculation complete for N = {n}.")

    # Show the most important result as a large Streamlit metric.
    st.metric(
        label=f"Number of primes less than or equal to {n}",
        value=prime_count,
    )

    # Use columns to show extra useful results in a neat layout.
    left_column, right_column = st.columns(2)

    # Show the smallest prime information.
    with left_column:

        # The smallest prime is always 2 if at least one prime exists.
        smallest_prime = primes[0] if primes else "None"

        # Display the smallest prime result.
        st.metric("Smallest prime found", smallest_prime)

    # Show the largest prime information.
    with right_column:

        # The largest prime is the final item in the sorted prime list.
        largest_prime = primes[-1] if primes else "None"

        # Display the largest prime result.
        st.metric("Largest prime found", largest_prime)

    # Display a preview of the prime numbers.
    st.subheader("Prime List Preview")

    # Show a readable preview of the generated primes.
    st.write(format_prime_preview(primes))

    # Put the full prime list behind an expander so the page stays clean.
    with st.expander("Show full prime list"):

        # If primes exist, display them in a scrollable text area.
        if primes:
            st.text_area(
                label="All primes up to N",
                value=", ".join(str(prime) for prime in primes),
                height=200,
            )

        # If no primes exist, display a simple message.
        else:
            st.write("There are no prime numbers up to this value.")


def render_algorithm_documentation():
    '''
    Display internal documentation about the algorithm inside the app.

    Parameters:
        None

    Returns:
        None

    Purpose:
        This function documents the strategy used by the program so users and
        evaluators can understand how the result is calculated.
    '''

    # Put documentation inside an expander to avoid overwhelming the interface.
    with st.expander("How the algorithm works"):

        # Explain the high-level method.
        st.write(
            "The app uses an optimized Sieve of Eratosthenes. "
            "The sieve marks composite numbers and leaves prime numbers unmarked."
        )

        # Explain why the algorithm is efficient.
        st.write(
            "To improve efficiency, the program stores only odd numbers after handling 2 separately. "
            "This cuts the sieve size almost in half."
        )

        # Explain why crossing out starts at p squared.
        st.write(
            "For each prime p, marking starts at p² because smaller multiples of p "
            "were already marked by smaller prime factors."
        )

        # Explain the time and space complexity in a simple way.
        st.write(
            "This method is fast for the required limit because N is less than 100000."
        )


def render_default_example():
    '''
    Display an example result before the user presses the calculation button.

    Parameters:
        None

    Returns:
        None

    Purpose:
        This function makes the interface useful immediately by showing what the
        app will do after the user clicks the button.
    '''

    # Create a small section for the default example.
    st.subheader("Example")

    # Show a simple example calculation.
    st.write("If N = 10, the prime numbers are 2, 3, 5, and 7.")

    # Show the example answer.
    st.write("Therefore, the number of primes less than or equal to 10 is **4**.")


def main():
    '''
    Run the Streamlit Prime Counter application.

    Parameters:
        None

    Returns:
        None

    Program Flow:
        - Configure the Streamlit page.
        - Render the title and sidebar.
        - Get user input.
        - Validate the input.
        - Count primes up to N.
        - Display the result in a user-friendly graphical interface.
    '''

    # Configure page settings.
    render_page_setup()

    # Display the main heading and explanation.
    render_header()

    # Display sidebar instructions and algorithm notes.
    render_sidebar()

    # Draw the input controls and get user choices.
    n, calculate_clicked = render_input_section()

    # If the user clicks the button, calculate and display the result.
    if calculate_clicked:
        render_results(n)

    # Otherwise, display a helpful example before calculation.
    else:
        render_default_example()

    # Always show algorithm documentation at the bottom.
    render_algorithm_documentation()


if __name__ == "__main__":
    main()
