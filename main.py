import streamlit as st

# Each imported module represents one independent Streamlit page/demo.
# Keeping each demo in its own file makes the project easier to maintain,
# test, and expand as the application grows.
import app_dictionary
import app_list
import app_ordered_list
import app_set
import app_binary_tree_parser

# For having documentation on th fly
import documentation
import documentation_v2


# Unit testing
import unit_test_dictionary
import unit_test_binary_tree

# Central page registry.
#
# The keys are the labels shown to the user in the sidebar.
# The values are the render functions that build each page.
#
# This pattern avoids multiple if/elif statements and makes it easy
# to add new pages later. To add another demo, import its module and
# register it here.
PAGES = {
    "Dictionary": app_dictionary.render,
    "Set": app_set.render,
    "List": app_list.render,
    "Ordered list": app_ordered_list.render,
    "Binary Tree Parser": app_binary_tree_parser.render,
    "Tests: Dictionary": unit_test_dictionary.render,
    "Tests: Binary Tree": unit_test_binary_tree.render,
    "Documentation": documentation.render,
    "Documentation V2": documentation_v2.render,
}


def main() -> None:
    """
    Main entry point for the Streamlit application.

    This function is responsible for:
    1. Configuring the Streamlit page.
    2. Building the sidebar navigation.
    3. Rendering the selected data structure demo.
    """

    # Configure global page settings.
    #
    # set_page_config should be called before rendering other Streamlit
    # elements. It controls browser tab title, layout behavior, and other
    # page-level options.
    st.set_page_config(
        page_title="Data Structure Demos",
        layout="centered",
    )

    # Sidebar title shown above the navigation menu.
    # The sidebar is useful for app-wide controls because it remains
    # separate from the main content area.
    st.sidebar.title("Data Structures")

    # Radio button used as the navigation control.
    #
    # options=list(PAGES.keys()) means the available choices come directly
    # from the page registry above. This keeps the UI synchronized with
    # the registered pages.
    #
    # key="selected_page" gives this widget a stable internal identifier.
    # This helps Streamlit track the widget state across reruns and avoids
    # duplicate widget key errors when the app grows.
    selected_page = st.sidebar.radio(
        "Choose a demo",
        options=list(PAGES.keys()),
        key="selected_page",
    )

    # Visual separator in the sidebar.
    # This improves readability by separating navigation from helper text.
    st.sidebar.markdown("---")

    # Small helper text for the user.
    # caption is less visually dominant than normal markdown text.
    st.sidebar.caption("Use the sidebar to switch demos with one click.")

    # Render the selected page.
    #
    # PAGES[selected_page] returns the function associated with the selected
    # sidebar option. The final () executes that function.
    #
    # Example:
    # If selected_page == "Dictionary",
    # then PAGES[selected_page] is app_dictionary.render,
    # so this line runs app_dictionary.render().
    PAGES[selected_page]()


# Python execution guard.
#
# This ensures main() only runs when this file is executed directly.
# It prevents the app from starting automatically if this file is imported
# by another module, test file, or tool.
if __name__ == "__main__":
    main()