import streamlit as st
import json

# File to store tasks
TASK_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    try:
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
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
        if new_task:
            tasks.append({"task": new_task, "completed": False})
            save_tasks(tasks)
            st.success(f"Task '{new_task}' added!")
        else:
            st.error("Please enter a task.")
    
    # Display tasks
    st.subheader("Your Tasks:")
    for i, task in enumerate(tasks):
        col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
        with col1:
            if st.checkbox("", key=i):
                tasks[i]["completed"] = True
        with col2:
            task_text = f"~~{task['task']}~~" if task["completed"] else task["task"]
            st.write(task_text)
        with col3:
            if st.button("❌", key=f"del-{i}"):
                tasks.pop(i)
                save_tasks(tasks)
                st.experimental_rerun()
    
    # Save updated tasks
    save_tasks(tasks)

if __name__ == "__main__":
    main()
