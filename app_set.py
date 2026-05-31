"""
app_set.py

Streamlit page that demonstrates Python set operations.

This module is intentionally documented with a module docstring because the
project documentation page reads `ast.get_docstring(tree)` and displays it as
"Module Docstring".

Purpose
-------
Teach the basic behavior of a Python set through a small interactive app.

Concepts demonstrated
---------------------
1. Creating a set
2. Displaying set values
3. Adding a unique value
4. Searching for a value
5. Editing a value by removing the old value and adding the new value
6. Comparing common set operations

Set characteristics
-------------------
- Stores unique values only
- Does not preserve guaranteed insertion order
- Is mutable
- Uses hashing internally
- Provides fast membership checks on average

Common set operations
---------------------
- add(value): add a new value
- remove(value): remove a value and raise an error if missing
- discard(value): remove a value without raising an error if missing
- value in set_name: check membership
- len(set_name): count values
- clear(): remove all values
- set_a | set_b: union
- set_a & set_b: intersection
- set_a - set_b: difference
- set_a ^ set_b: symmetric difference
- issubset(): check if one set is contained in another
- issuperset(): check if one set contains another

Complexity summary
------------------
- Add: O(1) average, O(n) worst case
- Search: O(1) average, O(n) worst case
- Remove: O(1) average, O(n) worst case
- Display all values: O(n)
- Space: O(n)

Why most operations are O(1) on average
---------------------------------------
Python sets use a hash table. Python calculates a hash for each value and uses
that hash to locate where the value should be stored. This usually avoids
scanning every item.

Why the worst case can be O(n)
------------------------------
In rare collision-heavy cases, many values may map to the same internal hash
area. Python may then need to check multiple values.
"""

from __future__ import annotations

import streamlit as st


# Common Python set syntax examples used by the documentation scanner.
#
# Create:
#     my_set = {"apple", "banana", "orange"}
#
# Add:
#     my_set.add("grape")
#
# Remove with error if missing:
#     my_set.remove("apple")
#
# Remove safely:
#     my_set.discard("apple")
#
# Search:
#     "banana" in my_set
#
# Union:
#     set_a | set_b
#
# Intersection:
#     set_a & set_b
#
# Difference:
#     set_a - set_b
#
# Symmetric difference:
#     set_a ^ set_b


def render() -> None:
    """
    Render the Set Demo page.

    This function builds a Streamlit interface for learning how Python sets work.

    User actions
    ------------
    1. View the current set stored in `st.session_state.my_set`.
    2. Add a new item to the set.
    3. Search for an existing item.
    4. Edit an item using remove plus add.
    5. Review common set operations and Big O complexity.

    Streamlit state behavior
    ------------------------
    Streamlit reruns the script after each interaction. Because of that,
    normal local variables are recreated frequently.

    This page stores the set in `st.session_state.my_set` so the values remain
    available while the user clicks buttons and types into inputs.

    Data structure used
    -------------------
    The main data structure is a Python set:

        {"grape", "pear", "apple"}

    A set is appropriate here because the demo needs duplicate prevention and
    fast membership checks.

    Complexity notes
    ----------------
    Initial creation:
        Time: O(n)
        Space: O(n)

    Add operation:
        Average time: O(1)
        Worst-case time: O(n)

    Search operation:
        Average time: O(1)
        Worst-case time: O(n)

    Remove operation:
        Average time: O(1)
        Worst-case time: O(n)

    Edit operation:
        Average time: O(1)
        Worst-case time: O(n)

    Display operation:
        Time: O(n)

    Where `n` is the number of values stored in the set.
    """

    st.title("Set Demo")

    st.markdown(
        """
        This page demonstrates operations on a Python **set**.

        A set stores **unique values only**.

        ```python
        {"grape", "pear", "apple"}
        ```

        Use a set when you want fast membership checks and duplicate prevention.
        """
    )

    # Initialize the set only once during the Streamlit session.
    if "my_set" not in st.session_state:
        st.session_state.my_set = {"grape", "pear", "apple"}

    st.subheader("Current set")
    st.write(st.session_state.my_set)

    st.info(
        "Sets are unordered. The displayed order can be different from the "
        "order used when the set was created."
    )

    st.divider()

    st.subheader("Add an item")
    item_to_add = st.text_input(
        "Item to add",
        key="set_add_item",
    )

    if st.button("Add", key="btn_set_add"):
        clean_item_to_add = item_to_add.strip()

        if not clean_item_to_add:
            st.error("The item cannot be empty.")
        elif clean_item_to_add in st.session_state.my_set:
            st.info(
                f"Item '{clean_item_to_add}' already exists. "
                "Sets store unique values only."
            )
        else:
            st.session_state.my_set.add(clean_item_to_add)
            st.success(f"Item '{clean_item_to_add}' was added.")

    st.markdown(
        """
        **Insertion complexity**

        | Case | Complexity | Reason |
        |---|---:|---|
        | Average | O(1) | Python usually inserts directly using the value hash. |
        | Worst | O(n) | Rare hash collision scenarios may require extra checks. |
        """
    )

    st.divider()

    st.subheader("Search for an item")
    item_to_query = st.text_input(
        "Item to search",
        key="set_query_item",
    )

    if st.button("Search", key="btn_set_query"):
        clean_item_to_query = item_to_query.strip()

        if not clean_item_to_query:
            st.warning("Enter an item before searching.")
        elif clean_item_to_query in st.session_state.my_set:
            st.info(f"Item '{clean_item_to_query}' was found in the set.")
        else:
            st.warning(f"Item '{clean_item_to_query}' was not found in the set.")

    st.markdown(
        """
        **Search complexity**

        ```python
        "apple" in my_set
        ```

        Average case: **O(1)**.  
        Worst case: **O(n)**.
        """
    )

    st.divider()

    st.subheader("Edit an item by remove and add")
    st.write(
        "A set does not support direct editing by index. "
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
        clean_item_to_remove = item_to_remove.strip()
        clean_new_item_to_add = new_item_to_add.strip()

        if not clean_item_to_remove:
            st.error("The item to remove cannot be empty.")
        elif not clean_new_item_to_add:
            st.error("The new item cannot be empty.")
        elif clean_item_to_remove not in st.session_state.my_set:
            st.warning(f"Item '{clean_item_to_remove}' was not found.")
        else:
            st.session_state.my_set.remove(clean_item_to_remove)
            st.session_state.my_set.add(clean_new_item_to_add)

            st.success(
                f"Item '{clean_item_to_remove}' was removed and "
                f"'{clean_new_item_to_add}' was added."
            )

    st.markdown(
        """
        **Edit complexity**

        A set item is edited with two operations:

        ```text
        remove old item + add new item
        ```

        Average case:

        ```text
        O(1) + O(1) = O(1)
        ```

        Worst case:

        ```text
        O(n) + O(n) = O(n)
        ```
        """
    )

    st.divider()

    st.subheader("Common set operations")

    st.code(
        """
my_set = {"apple", "banana", "orange"}

my_set.add("grape")              # Add item
my_set.remove("apple")           # Remove item, error if missing
my_set.discard("apple")          # Remove item safely
"banana" in my_set               # Search item
len(my_set)                       # Count items
my_set.clear()                    # Clear all items

set_a | set_b                     # Union
set_a & set_b                     # Intersection
set_a - set_b                     # Difference
set_a ^ set_b                     # Symmetric difference
set_a.issubset(set_b)             # Check subset
set_a.issuperset(set_b)           # Check superset
        """.strip(),
        language="python",
    )

    st.markdown(
        """
        ### Set vs list

        | Operation | List | Set |
        |---|---:|---:|
        | Search | O(n) | O(1) average |
        | Insert at end / add | O(1) average | O(1) average |
        | Remove by value | O(n) | O(1) average |
        | Allows duplicates | Yes | No |

        A set is usually better when the main question is:

        > Does this item exist?
        """
    )


if __name__ == "__main__":
    render()