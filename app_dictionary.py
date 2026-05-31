import streamlit as st

# Import function for validation
from tools import validate_numeric_value


def render() -> None:
    """
    Render the dictionary demo.

    This page demonstrates how a Python dictionary works using Streamlit.
    A dictionary stores data in key-value pairs.

    Example:
        {
            "apple": 10,
            "banana": 5
        }

    In this example:
    - "apple" is the key
    - 10 is the value
    """

    st.title("Dictionary Demo")

    st.markdown(
        """
        This page demonstrates operations on a Python dictionary, also known as a hash map.

        A dictionary is useful when you want to store values and access them quickly using a key.
        """
    )

    # Initialize the dictionary only once.
    #
    # Streamlit reruns this file every time the user interacts with the app.
    # Because of that, normal variables are reset on every interaction.
    #
    # st.session_state keeps data alive between reruns.
    if "my_dictionary" not in st.session_state:
        st.session_state.my_dictionary = {
            "apple": 10,
            "banana": 5,
            "orange": 8,
        }

    st.subheader("Current dictionary")
    st.write(st.session_state.my_dictionary)

    st.subheader("Insert or update an item")

    # The dictionary key is always text.
    # Example: "apple", "banana", "price", "discount"
    key_to_insert = st.text_input(
        "Key to insert or update",
        key="dict_key_insert",
    )

    # The user selects how the value should be validated before typing it.
    #
    # This is better than guessing the type because the user clearly defines
    # the expected format.
    input_type = st.selectbox(
        "Select the value type",
        options=["int", "float", "positive", "percentage"],
        key="dict_value_type",
    )

    # Optional sign validation.
    #
    # For most use cases, "either" is flexible.
    # If you want to force only positive values, select "positive".
    sign = st.selectbox(
        "Select the allowed sign",
        options=["either", "positive", "negative"],
        key="dict_value_sign",
    )

    # The value is captured as text first.
    # This allows us to validate it manually before converting it.
    value_to_insert_str = st.text_input(
        "Numeric value to insert or update",
        key="dict_value_insert",
    )

    if st.button("Insert or update", key="btn_dict_insert"):
        clean_key = key_to_insert.strip()

        if not clean_key:
            st.error("The key cannot be empty.")

        else:
            value_to_insert, error_message = validate_numeric_value(
                raw_value=value_to_insert_str,
                input_type=input_type,
                sign=sign,
            )

            if error_message:
                st.error(error_message)

            else:
                # Insert or update the dictionary.
                #
                # If the key does not exist, Python creates it.
                # If the key already exists, Python replaces its value.
                st.session_state.my_dictionary[clean_key] = value_to_insert

                st.success(
                    f"Item '{clean_key}: {value_to_insert}' was inserted or updated."
                )

    st.markdown(
        """
        **Insert/update complexity**

        Average case: **O(1)**. A dictionary uses hashing to locate the key.

        Worst case: **O(n)** in rare situations with many hash collisions.
        """
    )

    st.subheader("Search for an item")

    key_to_query = st.text_input(
        "Key to search",
        key="dict_key_query",
    )

    if st.button("Search", key="btn_dict_query"):
        clean_query_key = key_to_query.strip()

        if not clean_query_key:
            st.warning("Enter a key before searching.")

        elif clean_query_key in st.session_state.my_dictionary:
            value_found = st.session_state.my_dictionary[clean_query_key]

            st.info(f"Value for '{clean_query_key}': {value_found}")

        else:
            st.warning(f"Key '{clean_query_key}' was not found.")

    st.markdown(
        """
        **Search complexity**

        Average case: **O(1)** because dictionary lookup is hash-based.
        """
    )

    st.subheader("Edit an item")

    st.write(
        "Editing a dictionary item is the same operation as updating an existing key."
    )

    st.markdown(
        """
        **Edit complexity**

        Average case: **O(1)** when the key is already known.
        """
    )