```python
"""
Counting primes up to N.

This program reads one integer N from standard input and prints how many prime
numbers are less than or equal to N.

A prime number is a whole number greater than 1 that has exactly two positive
divisors: 1 and itself.

The program uses the Sieve of Eratosthenes, which is an efficient method for
finding all prime numbers up to a given limit.
"""


def count_primes_up_to(n):
    '''
    Count how many prime numbers are less than or equal to n.

    Parameters:
        n (int): The maximum number to check for primes.

    Returns:
        int: The number of prime numbers from 2 through n, inclusive.

    Strategy:
        - If n is less than 2, there are no prime numbers.
        - Create a list where each index represents whether that number is prime.
        - Mark 0 and 1 as not prime.
        - Starting from 2, mark multiples of each prime as not prime.
        - Count how many values remain marked as prime.
    '''

    # Numbers less than 2 cannot be prime, so the answer is immediately 0.
    if n < 2:
        return 0

    # Create a boolean list where index i represents whether i is prime.
    # At first, assume every number from 0 to n is prime.
    is_prime = [True] * (n + 1)

    # 0 is not prime because prime numbers must be greater than 1.
    is_prime[0] = False

    # 1 is not prime because it has only one positive divisor.
    is_prime[1] = False

    # We only need to check possible factors up to the square root of n.
    # If a number has a factor larger than its square root, it must also have
    # a matching factor smaller than its square root.
    limit = int(n ** 0.5)

    # Test every number from 2 up to the square root of n.
    for number in range(2, limit + 1):

        # If the current number is still marked prime, then its multiples
        # should be marked as not prime.
        if is_prime[number]:

            # Start marking from number * number because smaller multiples
            # have already been marked by smaller prime factors.
            start = number * number

            # Mark every multiple of number as not prime.
            for multiple in range(start, n + 1, number):
                is_prime[multiple] = False

    # Count all values that are still marked as prime.
    return sum(is_prime)


def read_input():
    '''
    Read the input value N from standard input.

    Parameters:
        None

    Returns:
        int: The integer N entered by the user or provided through input.

    Notes:
        - The program expects one integer.
        - Extra whitespace or newlines are allowed.
    '''

    # Read text from the user or input stream.
    raw_input_value = input().strip()

    # Convert the input text into an integer.
    return int(raw_input_value)


def main():
    '''
    Run the prime-counting program.

    Parameters:
        None

    Returns:
        None

    Steps:
        - Read N from input.
        - Count all prime numbers less than or equal to N.
        - Print the result.
    '''

    # Read the maximum number N.
    n = read_input()

    # Count how many prime numbers are less than or equal to N.
    answer = count_primes_up_to(n)

    # Print the final count.
    print(answer)


# This condition makes sure main() runs only when this file is executed directly.
# It prevents main() from running automatically if this file is imported.
if __name__ == "__main__":
    main()
```