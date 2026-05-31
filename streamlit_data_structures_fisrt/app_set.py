import streamlit as st


def render() -> None:
    """Render the set demo."""
    st.title("Set Demo")
    st.markdown("This page demonstrates operations on a Python set.")

    if "my_set" not in st.session_state:
        st.session_state.my_set = {"grape", "pear", "apple"}

    st.subheader("Current set")
    st.write(st.session_state.my_set)

    st.subheader("Add an item")
    item_to_add = st.text_input(
        "Item to add",
        key="set_add_item",
    )

    if st.button("Add", key="btn_set_add"):
        if not item_to_add.strip():
            st.error("The item cannot be empty.")
        elif item_to_add in st.session_state.my_set:
            st.info(f"Item '{item_to_add}' already exists. Sets store unique values only.")
        else:
            st.session_state.my_set.add(item_to_add)
            st.success(f"Item '{item_to_add}' was added.")

    st.markdown(
        """
        **Insertion complexity**

        Average case: **O(1)** because a set is hash-based.
        Worst case: **O(n)** in rare collision-heavy cases.
        """
    )

    st.subheader("Search for an item")
    item_to_query = st.text_input(
        "Item to search",
        key="set_query_item",
    )

    if st.button("Search", key="btn_set_query"):
        if not item_to_query.strip():
            st.warning("Enter an item before searching.")
        elif item_to_query in st.session_state.my_set:
            st.info(f"Item '{item_to_query}' was found in the set.")
        else:
            st.warning(f"Item '{item_to_query}' was not found in the set.")

    st.markdown(
        """
        **Search complexity**

        Average case: **O(1)** because membership checks use hashing.
        Worst case: **O(n)** in rare collision-heavy cases.
        """
    )

    st.subheader("Edit an item by remove and add")
    st.write(
        "A set does not support direct in-place editing. "
        "To change a value, remove the old item and add the new item."
    )

    item_to_remove = st.text_input(
        "Item to remove",
        key="set_remove_item",
    )
    new_item_to_add = st.text_input(
        "New item to add after removing the old item",
        key="set_new_item",
    )

    if st.button("Remove and add", key="btn_set_edit"):
        if not item_to_remove.strip():
            st.error("The item to remove cannot be empty.")
        elif not new_item_to_add.strip():
            st.error("The new item cannot be empty.")
        elif item_to_remove in st.session_state.my_set:
            st.session_state.my_set.remove(item_to_remove)
            st.session_state.my_set.add(new_item_to_add)
            st.success(f"Item '{item_to_remove}' was removed and '{new_item_to_add}' was added.")
        else:
            st.warning(f"Item '{item_to_remove}' was not found.")

    st.markdown(
        """
        **Edit complexity**

        Remove plus add: **O(1)** average case for each operation.
        """
    )
