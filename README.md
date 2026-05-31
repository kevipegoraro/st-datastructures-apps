# Streamlit Data Structure Demos

This project provides a main Streamlit application (`main.py`) that serves as a menu to navigate between four individual Streamlit applications. Each sub-application demonstrates the use of a specific Python data structure (dictionary, set, list, and an ordered list simulating a tree) and explains the time complexity (O(n)) of its basic operations (insertion, query, editing).

## Project Structure

- `main.py`: The main entry point, providing a menu to select other applications.
- `app_dictionary.py`: Demonstrates dictionary operations.
- `app_set.py`: Demonstrates set operations.
- `app_list.py`: Demonstrates list (common array) operations.
- `app_ordered_list.py`: Demonstrates operations on an ordered list, simulating a tree structure with binary search.
- `requirements.txt`: Lists all necessary Python dependencies.

## How to Run

1.  **Save the files:**
    *   Save `main.py` in your project directory.
    *   Save `app_dictionary.py`, `app_set.py`, `app_list.py`, and `app_ordered_list.py` in the **same directory** as `main.py`.
    *   Save `requirements.txt` in the same directory.

2.  **Open your terminal or command prompt.**

cretae venv and open the venv
python -m venv venv
source venv/bin/activate

3.  **Navigate to your project directory:**
    ```bash
    cd path/to/your/project
    ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the main Streamlit application:**
    ```bash
    streamlit run main.py
    ```
deactivate # for ausing the venv.
6.  Your web browser should automatically open to the Streamlit application, where you can choose which data structure demo to explore. Each demo includes a "Back to Main Menu" button to return to the selection screen.



Explanation of main.py:

st.session_state.current_app: This is crucial for managing which app is currently active. It stores the name of the Python file (without .py extension) that should be displayed.
set_app(app_name) function: A simple helper to update st.session_state.current_app.
main_menu() function: This function defines the content of your main menu, presenting buttons for each app. When a button is clicked, set_app() is called.
Conditional Logic (if st.session_state.current_app == 'main_menu':):
If current_app is 'main_menu', it calls main_menu() to display the selection screen.
Otherwise, it means an app has been selected.
Dynamic Import and Execution:
importlib.import_module(st.session_state.current_app): This line attempts to import the Python module corresponding to the selected app name (e.g., app_dictionary).
"Back to Main Menu" Button: This button is added before the content of the sub-app. When clicked, it sets current_app back to 'main_menu' and uses st.experimental_rerun() to immediately refresh the page and display the main menu.
with open(f"{st.session_state.current_app}.py", "r") as f: exec(f.read()): This is a way to execute the Streamlit code directly from the selected app file. When Streamlit runs a script, it executes it from top to bottom. By using exec(f.read()), we're effectively telling Streamlit to run the content of that specific app file within the context of main.py. This is a common pattern for simple multi-page Streamlit apps.
This setup allows you to easily navigate between your different data structure demonstrations while keeping the code for each demo separate and modular.


Choosing the right data structure is crucial for efficient programming, and each of the four discussed—dictionaries, sets, lists, and ordered lists (simulating trees)—excels in different scenarios. Dictionaries are ideal when you need fast lookups, insertions, and updates based on unique keys, making them perfect for mapping relationships, caching, or representing objects with named properties. Sets are best utilized when you primarily care about the presence or absence of unique elements and need to perform quick membership tests, union, intersection, or difference operations, such as filtering duplicates or managing unique tags. Lists (arrays) are versatile for ordered collections where element order matters, and you frequently add items to the end or access elements by their numerical index; however, searching for a specific value or inserting/deleting in the middle can be less efficient. Finally, ordered lists (simulating trees with binary search) are advantageous when you need to maintain a sorted collection and perform efficient searches (O(log n)), but they incur a higher cost for insertions and deletions (O(n)) compared to actual tree structures because elements must be shifted to maintain order.