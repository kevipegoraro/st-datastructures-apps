import streamlit as st

import app_dictionary
import app_list
import app_ordered_list
import app_set


PAGES = {
    "Dictionary": app_dictionary.render,
    "Set": app_set.render,
    "List": app_list.render,
    "Ordered list": app_ordered_list.render,
}


def main() -> None:
    st.set_page_config(
        page_title="Data Structure Demos",
        layout="centered",
    )

    st.sidebar.title("Data Structures")
    selected_page = st.sidebar.radio(
        "Choose a demo",
        options=list(PAGES.keys()),
        key="selected_page",
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Use the sidebar to switch demos with one click.")

    PAGES[selected_page]()


if __name__ == "__main__":
    main()
