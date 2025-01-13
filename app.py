import streamlit as st
import json
import os

# File to store tasks
TASK_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    """Loads tasks from the JSON file.

    Returns:
        list: A list of dictionaries, where each dictionary represents a task 
             with keys "task" (string) and "completed" (boolean).
    """
    if os.path.exists(TASK_FILE):
        try:
            with open(TASK_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            st.warning("Error loading tasks: Invalid JSON file. Creating a new one.")
            return []  # Create an empty list if the file is invalid
    return []

# Save tasks to file
def save_tasks(tasks):
    """Saves the list of tasks to the JSON file."""
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)  # Indent for better readability

# Streamlit App
def main():
    st.title("📝 To-Do App")

    # Session state for tasks
    if "tasks" not in st.session_state:
        st.session_state.tasks = load_tasks()

    # Add a new task
    new_task = st.text_input("Add a new task:")
    if st.button("Add Task"):
        if new_task.strip():
            st.session_state.tasks.append({"task": new_task.strip(), "completed": False})
            save_tasks(st.session_state.tasks)
            st.success(f"Task '{new_task}' added!")
        else:
            st.error("Please enter a valid task.")

    # Display tasks
    st.subheader("Your Tasks:")
    if st.session_state.tasks:
        for i, task in enumerate(st.session_state.tasks):
            col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
            with col1:
                completed = task.get("completed", False)  # Handle missing "completed" key
                if st.checkbox("", value=completed, key=f"complete-{i}"):
                    st.session_state.tasks[i]["completed"] = not completed
                    save_tasks(st.session_state.tasks)
            with col2:
                task_text = f"~~{task['task']}~~" if completed else task['task'] 
                st.write(task_text) 
            with col3:
                if st.button("❌", key=f"del-{i}"):
                    del st.session_state.tasks[i]  # Delete task directly from list
                    save_tasks(st.session_state.tasks)  # Save updated tasks

    else:
        st.write("No tasks yet. Add a new task above.")

if __name__ == "__main__":
    main()
