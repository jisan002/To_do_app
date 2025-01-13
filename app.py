import streamlit as st
import json
import os

# File to store tasks
TASK_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            try:
                tasks = json.load(file)
                # Ensure tasks have the correct structure
                if isinstance(tasks, list) and all("task" in t and "completed" in t for t in tasks):
                    return tasks
            except json.JSONDecodeError:
                st.error("Error loading tasks. Resetting task file.")
    return []  # Default empty task list

# Save tasks to file
def save_tasks(tasks):
    try:
        with open(TASK_FILE, "w") as file:
            json.dump(tasks, file)
    except Exception as e:
        st.error(f"Error saving tasks: {e}")

# Streamlit App
def main():
    st.title("📝 To-Do App by Jisan")

    # Initialize session state for tasks
    if "tasks" not in st.session_state:
        st.session_state["tasks"] = load_tasks()

    # Add a new task
    new_task = st.text_input("Add a new task:")
    if st.button("Add Task"):
        if new_task.strip():
            st.session_state["tasks"].append({"task": new_task.strip(), "completed": False})
            save_tasks(st.session_state["tasks"])
            st.success(f"Task '{new_task}' added!")
        else:
            st.error("Please enter a valid task.")

    # Display tasks
    st.subheader("Your Tasks:")
    for i, task in enumerate(st.session_state["tasks"]):
        col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
        with col1:
            if st.checkbox("", value=task["completed"], key=f"complete-{i}"):
                task["completed"] = not task["completed"]
                save_tasks(st.session_state["tasks"])
        with col2:
            task_text = f"~~{task['task']}~~" if task["completed"] else task["task"]
            st.write(task_text)
        with col3:
            if st.button("❌", key=f"del-{i}"):
                st.session_state["tasks"].pop(i)
                save_tasks(st.session_state["tasks"])
                st.experimental_rerun()

if __name__ == "__main__":
    main()
