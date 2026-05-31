import streamlit as st


def render() -> None:
    """Render the dictionary demo."""
    st.title("Dictionary Demo")
    st.markdown("This page demonstrates operations on a Python dictionary, also known as a hash map.")

    if "my_dictionary" not in st.session_state:
        st.session_state.my_dictionary = {
            "apple": 10,
            "banana": 5,
            "orange": 8,
        }

    st.subheader("Current dictionary")
    st.write(st.session_state.my_dictionary)

    st.subheader("Insert or update an item")
    key_to_insert = st.text_input(
        "Key to insert or update",
        key="dict_key_insert",
    )
    value_to_insert_str = st.text_input(
        "Numeric value to insert or update",
        key="dict_value_insert",
    )

    if st.button("Insert or update", key="btn_dict_insert"):
        if not key_to_insert.strip():
            st.error("The key cannot be empty.")
        else:
            try:
                value_to_insert = int(value_to_insert_str)
                st.session_state.my_dictionary[key_to_insert] = value_to_insert
                st.success(f"Item '{key_to_insert}: {value_to_insert}' was inserted or updated.")
            except ValueError:
                st.error(f"'{value_to_insert_str}' is not a valid integer.")

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
        if not key_to_query.strip():
            st.warning("Enter a key before searching.")
        elif key_to_query in st.session_state.my_dictionary:
            st.info(f"Value for '{key_to_query}': {st.session_state.my_dictionary[key_to_query]}")
        else:
            st.warning(f"Key '{key_to_query}' was not found.")

    st.markdown(
        """
        **Search complexity**

        Average case: **O(1)** because dictionary lookup is hash-based.
        """
    )

    st.subheader("Edit an item")
    st.write("Editing a dictionary item is the same operation as updating an existing key.")
    st.markdown(
        """
        **Edit complexity**

        Average case: **O(1)** when the key is already known.
        """
    )
