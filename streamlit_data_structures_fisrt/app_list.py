import streamlit as st


def render() -> None:
    """Render the list demo."""
    st.title("List Demo")
    st.markdown("This page demonstrates operations on a standard Python list.")

    if "my_list" not in st.session_state:
        st.session_state.my_list = ["item A", "item B", "item C"]

    st.subheader("Current list")
    st.write(st.session_state.my_list)

    st.subheader("Add an item")
    item_to_add_list = st.text_input(
        "Item to add to the end of the list",
        key="list_add_item",
    )

    if st.button("Add item", key="btn_list_add"):
        if not item_to_add_list.strip():
            st.error("The item cannot be empty.")
        else:
            st.session_state.my_list.append(item_to_add_list)
            st.success(f"Item '{item_to_add_list}' was added.")

    st.markdown(
        """
        **Insertion complexity**

        Append at the end: **O(1)** amortized.
        Worst case append: **O(n)** when the list must resize internally.
        Insert at the beginning or middle: **O(n)** because elements must shift.
        """
    )

    st.subheader("Search for an item")
    item_to_query_list = st.text_input(
        "Item to search in the list",
        key="list_query_item",
    )

    if st.button("Search item", key="btn_list_query"):
        if not item_to_query_list.strip():
            st.warning("Enter an item before searching.")
        elif item_to_query_list in st.session_state.my_list:
            st.info(f"Item '{item_to_query_list}' was found in the list.")
        else:
            st.warning(f"Item '{item_to_query_list}' was not found in the list.")

    st.markdown(
        """
        **Search complexity**

        Search by value in an unsorted list: **O(n)**.
        """
    )

    st.subheader("Edit an item")
    index_to_edit_str = st.text_input(
        "Index of the item to edit, starting at 0",
        key="list_edit_index_str",
    )
    new_value_for_edit = st.text_input(
        "New text value",
        key="list_edit_value",
    )

    if st.button("Edit item", key="btn_list_edit"):
        if not new_value_for_edit.strip():
            st.error("The new value cannot be empty.")
        else:
            try:
                index_to_edit = int(index_to_edit_str)
                if 0 <= index_to_edit < len(st.session_state.my_list):
                    st.session_state.my_list[index_to_edit] = new_value_for_edit
                    st.success(f"Item at index {index_to_edit} was changed to '{new_value_for_edit}'.")
                else:
                    max_index = len(st.session_state.my_list) - 1
                    st.error(f"Invalid index. Enter a number from 0 to {max_index}.")
            except ValueError:
                st.error(f"'{index_to_edit_str}' is not a valid integer.")

    st.markdown(
        """
        **Edit complexity**

        Edit by known index: **O(1)**.
        Find by value and then edit: **O(n)** because the search comes first.
        """
    )
