import streamlit as st

# -----------------------------------------------------------------------------
# Parser Logic
# -----------------------------------------------------------------------------
#
# This file demonstrates how to convert a mathematical expression into a binary
# tree using a recursive descent parser.
#
# The program supports:
# - Integer numbers
# - Addition: +
# - Multiplication: *
# - Parentheses: ( )
#
# Example expression:
#     10+(5+5+5)*(5+4+1)
#
# The expression is converted into an Abstract Syntax Tree, also called an AST.
#
# An AST is a tree representation of code or expressions.
# Each operator becomes a parent node.
# Each number becomes a leaf node.
#
# Example:
#     2 + 3 * 4
#
# Because multiplication has higher precedence than addition, the tree becomes:
#
#     +
#    / \
#   2   *
#      / \
#     3   4
#
# The parser in this file respects that rule.
# Multiplication is parsed before addition.
# Parentheses can override the default precedence.
# -----------------------------------------------------------------------------


class Node:
    """
    Represent one node in a binary tree.

    A binary tree node can have:
    - One value
    - One left child
    - One right child

    In this parser, a node can represent either:
    - A number, such as 10
    - An operator, such as "+" or "*"

    Example number node:
        Node(10)

    Example operator node:
        Node("+", Node(5), Node(3))

    That operator node represents:
        5 + 3

    Attributes:
        value:
            The value stored inside the node.

            It can be:
            - int: for numbers
            - str: for operators like "+" or "*"

        left:
            The left child of the node.

            For a number node, this is usually None.
            For an operator node, this is the left side of the operation.

        right:
            The right child of the node.

            For a number node, this is usually None.
            For an operator node, this is the right side of the operation.

    Big O:
        Creating one node is O(1).

        Explanation:
            The constructor only stores three values:
            - value
            - left
            - right

            It does not loop through a list or traverse a tree.
            Because of that, the time complexity is constant.

        Space complexity:
            O(1) per node.

            Each node stores a fixed amount of data.
            However, a full tree with n nodes uses O(n) total space.
    """

    def __init__(self, value, left=None, right=None):
        """
        Initialize a new tree node.

        Args:
            value:
                The value stored inside the node.

                Examples:
                    10
                    "+"
                    "*"

            left:
                Optional left child node.

            right:
                Optional right child node.

        Returns:
            None

        Big O:
            Time complexity: O(1)
            Space complexity: O(1)
        """

        self.value = value
        self.left = left
        self.right = right


class Parser:
    """
    Parse a mathematical expression and convert it into a binary tree.

    This class uses a recursive descent parser.

    A recursive descent parser is a parser built from several functions.
    Each function is responsible for one level of grammar.

    In this parser, the grammar is:

        expression -> term + term + term ...
        term       -> factor * factor * factor ...
        factor     -> number | parenthesized expression

    Meaning:
        - parse_expr handles addition
        - parse_term handles multiplication
        - parse_factor handles numbers and parentheses

    Why this structure matters:
        Multiplication has higher precedence than addition.

        Example:
            2 + 3 * 4

        Correct result:
            14

        Not:
            20

        The parser gets this right because parse_expr calls parse_term first.
        That means multiplication is grouped before addition.

    Attributes:
        tokens:
            A list of tokens created from the input expression.

            Example:
                "10+(5*2)"

            Becomes:
                [10, "+", "(", 5, "*", 2, ")"]

        pos:
            The current position inside the token list.

            This works like a cursor.
            It tells the parser which token it is currently reading.

    Big O:
        Tokenizing the expression is O(n), where n is the number of characters
        in the input expression.

        Parsing the token list is O(t), where t is the number of tokens.

        Since the number of tokens is proportional to the size of the input,
        the overall complexity is usually written as O(n).

        Space complexity is O(n), because the parser stores:
        - The token list
        - The generated binary tree
    """

    def __init__(self, expression):
        """
        Initialize the parser with a mathematical expression.

        Args:
            expression:
                A string containing the mathematical expression.

                Example:
                    "10+(5+5)*2"

        The constructor immediately tokenizes the expression.

        Big O:
            Time complexity: O(n)

            Explanation:
                The tokenizer scans the expression from left to right once.

            Space complexity: O(n)

            Explanation:
                The tokens are stored in a list.
        """

        self.tokens = self.tokenize(expression)
        self.pos = 0

    def tokenize(self, expr):
        """
        Convert the raw expression string into a list of tokens.

        A token is a meaningful piece of the expression.

        Example:
            Input:
                "10+(5*2)"

            Output:
                [10, "+", "(", 5, "*", 2, ")"]

        This method recognizes:
            - Whole integers
            - Addition operator: +
            - Multiplication operator: *
            - Opening parenthesis: (
            - Closing parenthesis: )

        This method does not accept:
            - Letters
            - Decimal numbers
            - Negative numbers
            - Division
            - Subtraction
            - Invalid symbols

        If an invalid character is found, the method raises a ValueError.

        Args:
            expr:
                The expression string without spaces.

        Returns:
            A list of tokens.

        Raises:
            ValueError:
                If the expression contains an unexpected character.

        Big O:
            Time complexity: O(n)

            Explanation:
                The method reads each character in the expression once.
                When it finds a multi-digit number, it continues reading until
                the full number is complete.

            Space complexity: O(n)

            Explanation:
                The method creates a list of tokens.
                In the worst case, every character becomes one token.
        """

        tokens = []
        i = 0

        # Scan the expression one character at a time.
        while i < len(expr):

            # If the current character is a digit, read the full number.
            #
            # Example:
            #   "123+5"
            #
            # We do not want to tokenize it as:
            #   [1, 2, 3, "+", 5]
            #
            # We want:
            #   [123, "+", 5]
            if expr[i].isdigit():
                num = ""

                while i < len(expr) and expr[i].isdigit():
                    num += expr[i]
                    i += 1

                tokens.append(int(num))

                # Continue because i is already pointing to the next character.
                # Without continue, the loop would increment i again and skip one
                # character.
                continue

            # Operators and parentheses are single-character tokens.
            elif expr[i] in "+*()":
                tokens.append(expr[i])

            # Any other character is invalid for this simple parser.
            else:
                raise ValueError(f"Unexpected token: {expr[i]}")

            i += 1

        return tokens

    def peek(self):
        """
        Return the current token without moving the parser forward.

        This method is useful when the parser needs to check what comes next
        before deciding what to do.

        Example:
            If the current token is "+", parse_expr knows it should consume
            the operator and parse another term.

        Returns:
            The current token if one exists.
            None if the parser has reached the end of the token list.

        Big O:
            Time complexity: O(1)

            Explanation:
                Accessing a list by index is constant time.

            Space complexity: O(1)

            Explanation:
                No new list or tree is created.
        """

        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        """
        Return the current token and move the parser to the next token.

        This method advances the parser cursor.

        Example:
            Before:
                tokens = [10, "+", 5]
                pos = 0

            consume() returns:
                10

            After:
                pos = 1

        Returns:
            The token that was consumed.

        Big O:
            Time complexity: O(1)

            Explanation:
                The method reads one token and increments one integer.

            Space complexity: O(1)
        """

        tok = self.peek()
        self.pos += 1
        return tok

    def parse_expr(self):
        """
        Parse an expression.

        In this parser, an expression is one or more terms joined by addition.

        Grammar:
            expression -> term + term + term ...

        Example:
            2 + 3 + 4

        The parser creates a left-associative tree.

        Example tree:
            +
           / \
          +   4
         / \
        2   3

        This means:
            (2 + 3) + 4

        Args:
            None

        Returns:
            A Node representing the root of the parsed expression.

        Big O:
            Time complexity: O(n)

            Explanation:
                Across the full parsing process, every token is consumed at
                most once. This function may loop over addition operators, but
                it does not reprocess tokens that were already consumed.

            Space complexity: O(n)

            Explanation:
                The parser builds tree nodes for numbers and operators.
                For n tokens, the resulting tree can contain O(n) nodes.
        """

        # First parse the left side as a term.
        # A term handles multiplication before addition.
        node = self.parse_term()

        # Continue while the next token is addition.
        while self.peek() == "+":
            op = self.consume()
            right = self.parse_term()

            # Create a new operator node.
            #
            # The previous tree becomes the left child.
            # The newly parsed term becomes the right child.
            node = Node(op, node, right)

        return node

    def parse_term(self):
        """
        Parse a term.

        In this parser, a term is one or more factors joined by multiplication.

        Grammar:
            term -> factor * factor * factor ...

        Example:
            3 * 4 * 5

        The parser creates a left-associative tree.

        Example tree:
            *
           / \
          *   5
         / \
        3   4

        This means:
            (3 * 4) * 5

        Why parse_term exists:
            Multiplication has higher precedence than addition.

            Because parse_expr depends on parse_term, all multiplication
            operations are grouped before addition operations.

        Returns:
            A Node representing the root of the parsed term.

        Big O:
            Time complexity: O(n)

            Explanation:
                Across the full parse, each token is consumed once.

            Space complexity: O(n)

            Explanation:
                New nodes are created for multiplication operators and factors.
        """

        # First parse the left side as a factor.
        # A factor can be a number or a parenthesized expression.
        node = self.parse_factor()

        # Continue while the next token is multiplication.
        while self.peek() == "*":
            op = self.consume()
            right = self.parse_factor()

            # Create a new operator node for multiplication.
            node = Node(op, node, right)

        return node

    def parse_factor(self):
        """
        Parse a factor.

        A factor is the smallest unit in this grammar.

        A factor can be:
            - An integer
            - A full expression inside parentheses

        Grammar:
            factor -> number
            factor -> "(" expression ")"

        Examples:
            10
            (2 + 3)
            (4 * (5 + 6))

        Parentheses are important because they allow the user to override
        normal operator precedence.

        Example:
            2 + 3 * 4 = 14

            But:
            (2 + 3) * 4 = 20

        Returns:
            A Node representing the parsed factor.

        Raises:
            ValueError:
                If the parser finds an unexpected token.
                If a closing parenthesis is missing.

        Big O:
            Time complexity: O(n) in the overall parser.

            Explanation:
                This method may call parse_expr recursively when it finds an
                opening parenthesis.

                Even with recursion, each token is still consumed once across
                the whole parse.

            Space complexity: O(d)

            Explanation:
                d is the maximum depth of nested parentheses.

                Example:
                    (((1+2)))

                Deeply nested expressions create deeper recursive calls.
                The final tree still uses O(n) space.
        """

        tok = self.peek()

        # Case 1:
        # The factor is a number.
        if isinstance(tok, int):
            self.consume()
            return Node(tok)

        # Case 2:
        # The factor is a full expression inside parentheses.
        elif tok == "(":
            self.consume()

            # Recursively parse the expression inside the parentheses.
            node = self.parse_expr()

            # After parsing the inner expression, the next token must be ")".
            if self.peek() != ")":
                raise ValueError("Missing closing parenthesis")

            self.consume()
            return node

        # Case 3:
        # Anything else is invalid in this grammar.
        raise ValueError(f"Unexpected token: {tok}")


def evaluate(node):
    """
    Evaluate the binary expression tree and return the numeric result.

    This function uses post-order traversal.

    Post-order traversal means:
        1. Evaluate the left child
        2. Evaluate the right child
        3. Apply the operator at the current node

    Example tree:
        +
       / \
      2   *
         / \
        3   4

    Evaluation order:
        1. Read 2
        2. Evaluate 3 * 4
        3. Add 2 + 12
        4. Return 14

    Args:
        node:
            The root node of the expression tree.

    Returns:
        The calculated integer result.

    Raises:
        ValueError:
            If the function finds an unknown operator.

    Big O:
        Time complexity: O(n)

        Explanation:
            The function visits each node in the tree exactly once.

        Space complexity: O(h)

        Explanation:
            h is the height of the tree.

            This space is used by the recursive call stack.

            In a balanced tree:
                h = log n

            In a very unbalanced tree:
                h = n
    """

    # Base case:
    # If the node stores an integer, it is already a value.
    if isinstance(node.value, int):
        return node.value

    # Recursive case:
    # Evaluate the left and right subtrees before applying the operator.
    left = evaluate(node.left)
    right = evaluate(node.right)

    if node.value == "+":
        return left + right

    elif node.value == "*":
        return left * right

    raise ValueError("Unknown operator")


def get_tree_string(node, prefix="", is_left=True) -> str:
    """
    Recursively build a formatted ASCII string representing the tree.

    This function converts the binary tree into a readable text format.

    Example output:
        └── +
            ├── 10
            └── *
                ├── +
                │   ├── 5
                │   └── 5
                └── 2

    Args:
        node:
            The current tree node being printed.

        prefix:
            The indentation and vertical guide lines used before the current
            node.

            This value changes during recursion.

        is_left:
            Boolean that controls which connector should be used.

            If True:
                The node is shown with "├──"

            If False:
                The node is shown with "└──"

    Returns:
        A string containing the full ASCII tree.

    Big O:
        Time complexity: O(n)

        Explanation:
            Each node is visited once.

            However, because strings are immutable in Python, repeated string
            concatenation can become less efficient for very large trees.

            For small educational examples, this is fine.

            For a production version with large trees, a better approach would
            be to append lines to a list and use "\\n".join(lines).

        Space complexity: O(n)

        Explanation:
            The final tree string contains one line for each node.
            The recursive call stack also uses O(h), where h is tree height.
    """

    if node is None:
        return ""

    # Select the connector depending on whether this node is considered
    # a left-side or right-side child in the displayed tree.
    connector = "├── " if is_left else "└── "

    # Add the current node value to the result string.
    result = prefix + connector + str(node.value) + "\n"

    # If the node has children, recursively format them.
    if node.left or node.right:

        # Format the left child first.
        if node.left:
            result += get_tree_string(
                node.left,
                prefix + ("│   " if is_left else "    "),
                True,
            )

        # Format the right child second.
        if node.right:
            result += get_tree_string(
                node.right,
                prefix + ("│   " if is_left else "    "),
                False,
            )

    return result


# -----------------------------------------------------------------------------
# Streamlit UI
# -----------------------------------------------------------------------------
#
# This section creates the visual interface of the demo.
#
# Streamlit reruns the script every time the user interacts with a widget.
# Because this parser does not need to store long-term app state, we can keep the
# UI simple and parse the expression only when the button is clicked.
# -----------------------------------------------------------------------------


def render() -> None:
    """
    Render the Binary Tree Parser demo page.

    This Streamlit page demonstrates how a mathematical expression can be parsed
    into an Abstract Syntax Tree using a binary tree.

    The page allows the user to:
        1. Type a mathematical expression
        2. Parse the expression
        3. Evaluate the final numeric result
        4. Display the tree structure in ASCII format
        5. Read the Big O complexity explanation

    Supported syntax:
        - Integers
        - Addition: +
        - Multiplication: *
        - Parentheses: ( )

    Example:
        10+(5+5+5)*(5+4+1)

    Important parser behavior:
        Multiplication has higher precedence than addition.

        Example:
            2+3*4

        The parser reads this as:
            2+(3*4)

        Result:
            14

    Big O summary:
        Tokenization:
            Time: O(n)
            Space: O(n)

        Parsing:
            Time: O(n)
            Space: O(n)

        Evaluation:
            Time: O(n)
            Space: O(h)

        ASCII tree generation:
            Time: O(n)
            Space: O(n)

        Where:
            n = number of tokens or nodes
            h = height of the tree
    """

    st.title("Binary Tree Parser Demo")

    st.markdown(
        """
        This page demonstrates a **recursive descent parser**.

        The parser converts a mathematical expression into an
        **Abstract Syntax Tree**, also called an **AST**.

        An AST is a tree that shows the structure of an expression.

        Supported operations:

        - Addition: `+`
        - Multiplication: `*`
        - Parentheses: `()`
        - Integer numbers
        """
    )

    st.subheader("Parse an expression")

    # The default expression gives the user a ready-to-test example.
    #
    # Expression:
    #     10+(5+5+5)*(5+4+1)
    #
    # The parser should:
    # - Read 10 as a number
    # - Parse the first parenthesized group: (5+5+5)
    # - Parse the second parenthesized group: (5+4+1)
    # - Multiply those two groups
    # - Add the result to 10
    expression_input = st.text_input(
        "Enter a mathematical expression",
        value="10+(5+5+5)*(5+4+1)",
        key="parser_expression_input",
    )

    if st.button("Parse and Evaluate", key="btn_parse_expr"):

        # Remove spaces before parsing.
        #
        # The tokenizer in this example does not handle whitespace directly.
        # This makes the parser logic simpler for learning purposes.
        clean_expr = expression_input.replace(" ", "")

        if not clean_expr:
            st.warning("Please enter an expression.")

        else:
            try:
                # Step 1:
                # Create the parser.
                #
                # The Parser constructor automatically tokenizes the expression.
                parser = Parser(clean_expr)

                # Step 2:
                # Parse the expression into a tree.
                #
                # tree_root is the root node of the AST.
                tree_root = parser.parse_expr()

                # Optional validation:
                # After parsing, there should be no unused tokens left.
                #
                # Example invalid input:
                #     2+3)
                #
                # The parser may parse "2+3", but ")" would remain unused.
                # This check catches that kind of invalid expression.
                if parser.peek() is not None:
                    raise ValueError(f"Unexpected token after expression: {parser.peek()}")

                # Step 3:
                # Evaluate the expression tree.
                #
                # This uses recursive post-order traversal.
                result = evaluate(tree_root)

                # Step 4:
                # Generate an ASCII version of the tree.
                tree_ascii = get_tree_string(tree_root, "", False)

                # Display the final result.
                st.success(f"Result: {result}")

                st.markdown("### Abstract Syntax Tree")
                st.markdown(
                    """
                    The tree below shows how the parser understands your expression.

                    Operators become parent nodes.
                    Numbers become leaf nodes.
                    """
                )

                # st.code preserves spacing and line breaks.
                # This is important because ASCII trees depend on formatting.
                st.code(tree_ascii, language="text")

            except Exception as e:
                st.error(f"Error parsing expression: {e}")

    st.markdown(
        """
        ---

        ### How the parser works

        **1. Tokenizer**

        The tokenizer converts the raw string into tokens.

        Example:

        ```text
        10+(5*2)
        ```

        Becomes:

        ```python
        [10, "+", "(", 5, "*", 2, ")"]
        ```

        **Big O**

        - Time complexity: **O(n)**
        - Space complexity: **O(n)**

        The tokenizer scans the expression once and stores the tokens in a list.

        ---

        **2. Parser**

        The parser reads the token list and builds a binary tree.

        It uses this order:

        ```text
        expression -> addition
        term       -> multiplication
        factor     -> number or parenthesized expression
        ```

        This structure makes multiplication happen before addition.

        **Big O**

        - Time complexity: **O(n)**
        - Space complexity: **O(n)**

        Each token is consumed once, and each number/operator can become a tree node.

        ---

        **3. Evaluator**

        The evaluator calculates the final result by walking through the tree.

        It uses post-order traversal:

        ```text
        left -> right -> root
        ```

        **Big O**

        - Time complexity: **O(n)**
        - Space complexity: **O(h)**

        Where:

        - `n` is the number of nodes
        - `h` is the height of the tree

        ---

        **4. Tree display**

        The tree display function recursively creates a readable ASCII tree.

        **Big O**

        - Time complexity: **O(n)**
        - Space complexity: **O(n)**

        The output string contains one line for each node in the tree.
        """
    )