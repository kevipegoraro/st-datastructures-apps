import bisect
import streamlit as st


def search_in_ordered_list(data_list: list[tuple[str, int]], search_key: str) -> tuple[str, int] | None:
    """Find an item by key in a sorted list of (key, value) tuples."""
    idx = bisect.bisect_left(data_list, (search_key, -float("inf")))
    if idx != len(data_list) and data_list[idx][0] == search_key:
        return data_list[idx]
    return None


def render() -> None:
    """Render the ordered-list demo."""
    st.title("Ordered List Demo")
    st.markdown(
        "This page demonstrates operations on a Python list kept in sorted order. "
        "It simulates part of the search behavior of a binary search tree."
    )

    if "my_ordered_list" not in st.session_state:
        st.session_state.my_ordered_list = [
            ("apple", 10),
            ("banana", 5),
            ("carrot", 12),
        ]
        st.session_state.my_ordered_list.sort(key=lambda item: item[0])

    st.subheader("Current ordered list")
    st.write(st.session_state.my_ordered_list)

    st.subheader("Insert an item")
    key_to_insert_tree = st.text_input(
        "Key to insert",
        key="tree_key_insert",
    )
    value_to_insert_tree_str = st.text_input(
        "Numeric value to insert",
        key="tree_value_insert",
    )

    if st.button("Insert item", key="btn_tree_insert"):
        if not key_to_insert_tree.strip():
            st.error("The key cannot be empty.")
        else:
            try:
                value_to_insert_tree = int(value_to_insert_tree_str)
                new_item = (key_to_insert_tree, value_to_insert_tree)

                found_index = next(
                    (
                        index
                        for index, (key, _value) in enumerate(st.session_state.my_ordered_list)
                        if key == key_to_insert_tree
                    ),
                    -1,
                )

                if found_index != -1:
                    st.session_state.my_ordered_list[found_index] = new_item
                    st.success(f"Item with key '{key_to_insert_tree}' was updated.")
                else:
                    bisect.insort_left(st.session_state.my_ordered_list, new_item)
                    st.success(f"Item '{key_to_insert_tree}: {value_to_insert_tree}' was inserted.")
            except ValueError:
                st.error(f"'{value_to_insert_tree_str}' is not a valid integer.")

    st.markdown(
        """
        **Insertion complexity**

        Find the correct position with binary search: **O(log n)**.
        Insert into the Python list: **O(n)** because elements must shift.
        Total: **O(n)**.
        """
    )

    st.subheader("Search for an item")
    key_to_query_tree = st.text_input(
        "Key to search",
        key="tree_key_query",
    )

    if st.button("Search item", key="btn_tree_query"):
        if not key_to_query_tree.strip():
            st.warning("Enter a key before searching.")
        else:
            result = search_in_ordered_list(st.session_state.my_ordered_list, key_to_query_tree)
            if result:
                st.info(f"Item found: {result[0]}: {result[1]}")
            else:
                st.warning(f"Key '{key_to_query_tree}' was not found.")

    st.markdown(
        """
        **Search complexity**

        Binary search in a sorted list: **O(log n)**.
        """
    )

    st.subheader("Edit an item")
    key_to_edit_tree = st.text_input(
        "Key of the item to edit",
        key="tree_key_edit",
    )
    new_value_tree_str = st.text_input(
        "New numeric value",
        key="tree_value_edit",
    )

    if st.button("Edit item", key="btn_tree_edit"):
        if not key_to_edit_tree.strip():
            st.error("The key cannot be empty.")
        else:
            try:
                new_value_tree = int(new_value_tree_str)
                for index, (key, _value) in enumerate(st.session_state.my_ordered_list):
                    if key == key_to_edit_tree:
                        st.session_state.my_ordered_list[index] = (key_to_edit_tree, new_value_tree)
                        st.success(f"Item with key '{key_to_edit_tree}' was changed to '{new_value_tree}'.")
                        break
                else:
                    st.warning(f"Key '{key_to_edit_tree}' was not found.")
            except ValueError:
                st.error(f"'{new_value_tree_str}' is not a valid integer.")

    st.markdown(
        """
        **Edit complexity**

        Find the key with binary search: **O(log n)**.
        Change only the value after the position is known: **O(1)**.
        If the key changes and order must be preserved, the operation becomes **O(n)**.
        """
    )
