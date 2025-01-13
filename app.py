import streamlit as st
import json
import os

# File to store tasks
TASK_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file)

# Streamlit App
def main():
    st.title("📝 To-Do App by Jisan")
    
    # Load tasks
    tasks = load_tasks()
    
    # Add a new task
    new_task = st.text_input("Add a new task:")
    if st.button("Add Task"):
        if new_task.strip():
            tasks.append({"task": new_task.strip(), "completed": False})
            save_tasks(tasks)
            st.success(f"Task '{new_task}' added!")
            st.experimental_rerun()  # Refresh the UI
        else:
            st.error("Please enter a valid task.")
    
    # Display tasks
    st.subheader("Your Tasks:")
    for i, task in enumerate(tasks):
        col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
        with col1:
            if st.checkbox("", value=task["completed"], key=f"complete-{i}"):
                tasks[i]["completed"] = not task["completed"]
                save_tasks(tasks)
        with col2:
            task_text = f"~~{task['task']}~~" if task["completed"] else task["task"]
            st.write(task_text)
        with col3:
            if st.button("❌", key=f"del-{i}"):
                tasks.pop(i)
                save_tasks(tasks)
                st.experimental_rerun()  # Refresh the UI

    # Save updated tasks (although we are already doing this after task deletion)
    save_tasks(tasks)

if __name__ == "__main__":
    main()
