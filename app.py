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
                return json.load(file)
            except json.JSONDecodeError:
                return []  # Return an empty list if the file is invalid
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file)

# Streamlit App
def main():
    st.title("📝 To-Do App by Jisan")

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
    if st.session_state.tasks:  # Check if tasks exist
        for i, task in enumerate(st.session_state.tasks):
            col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
            with col1:
                if st.checkbox("", value=task["completed"], key=f"complete-{i}"):
                    st.session_state.tasks[i]["completed"] = not task["completed"]
                    save_tasks(st.session_state.tasks)
            with col2:
                task_text = f"~~{task['task']}~~" if task["completed"] else task["task"]
                st.write(task_text)
            with col3:
                # Custom logic to safely delete a task
                if st.button("❌", key=f"del-{i}"):
                    # Mark task for deletion
                    delete_task(i)

    else:
        st.write("No tasks yet. Add a new task above.")

    # Save updated tasks
    save_tasks(st.session_state.tasks)


# Function to delete a task
def delete_task(index):
    try:
        st.session_state.tasks.pop(index)  # Remove the task
        save_tasks(st.session_state.tasks)  # Save updated tasks
        st.experimental_rerun()  # Refresh UI to reflect changes
    except IndexError:
        st.error("Error: Task index out of range.")

if __name__ == "__main__":
    main()
