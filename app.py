import streamlit as st
import time
import pandas as pd
from datetime import datetime

def main():
    st.title("Personalized Study Timer and Task Tracker")

    # Task list in session state
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    
    if "completed_tasks" not in st.session_state:
        st.session_state.completed_tasks = []

    if "productivity_log" not in st.session_state:
        st.session_state.productivity_log = []

    # Add new task
    with st.form("task_form"):
        task_name = st.text_input("Enter a task:")
        task_duration = st.number_input("Estimated duration (minutes):", min_value=1, step=1)
        submitted = st.form_submit_button("Add Task")

        if submitted and task_name:
            st.session_state.tasks.append({"name": task_name, "duration": task_duration, "completed": False, "started": False})
            st.success(f"Task '{task_name}' added!")

    # Display tasks
    st.header("Task List")
    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.write(f"**{task['name']}** - {task['duration']} minutes")
        with col2:
            if not task['started']:
                if st.button(f"Start", key=f"start_{i}"):
                    task['started'] = True
                    task['start_time'] = datetime.now()
                    st.experimental_rerun()
        with col3:
            if task['started'] and not task['completed']:
                if st.button(f"Mark as Completed", key=f"complete_{i}"):
                    task['completed'] = True
                    task['end_time'] = datetime.now()
                    st.session_state.completed_tasks.append(task)
                    st.session_state.productivity_log.append({
                        "task_name": task['name'],
                        "start_time": task['start_time'],
                        "end_time": task['end_time'],
                        "duration": task['duration']
                    })
                    st.session_state.tasks.pop(i)
                    st.experimental_rerun()
        with col4:
            if st.button(f"Remove", key=f"remove_{i}"):
                st.session_state.tasks.pop(i)
                st.experimental_rerun()

    # Show progress
    st.header("Progress")
    total_tasks = len(st.session_state.tasks) + len(st.session_state.completed_tasks)
    if total_tasks > 0:
        completed = len(st.session_state.completed_tasks)
        st.progress(completed / total_tasks)
        st.write(f"**{completed}/{total_tasks} tasks completed**")
    else:
        st.write("No tasks available. Add a task to get started!")

    # Show productivity chart (Completed tasks vs Total tasks)
    if total_tasks > 0:
        st.header("Productivity Analysis")
        progress_data = {"Completed Tasks": len(st.session_state.completed_tasks), "Total Tasks": total_tasks}
        progress_df = pd.DataFrame(list(progress_data.items()), columns=["Status", "Count"])
        st.bar_chart(progress_df.set_index("Status").sort_values(by="Count", ascending=False), use_container_width=True)
    
    # Show productivity log
    if st.session_state.productivity_log:
        st.write("**Productivity Log:**", pd.DataFrame(st.session_state.productivity_log))

    # Start timer when task is started
    for i, task in enumerate(st.session_state.tasks):
        if task["started"] and not task["completed"]:
            run_timer(task["name"], task["duration"], i)


def run_timer(task_name, duration, task_index):
    st.subheader(f"Task: {task_name}")
    placeholder = st.empty()
    total_seconds = duration * 60
    for i in range(total_seconds, -1, -1):
        mins, secs = divmod(i, 60)
        placeholder.markdown(f"### ⏳ {mins:02d}:{secs:02d}")
        time.sleep(1)  # Simulate real-time countdown
        if i == 0:
            st.success(f"Task '{task_name}' completed!")
            st.session_state.tasks[task_index]["completed"] = True
            st.experimental_rerun()  # Refresh to update progress and chart
    time.sleep(1)

if __name__ == "__main__":
    main()
