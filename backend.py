import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.ttk import Treeview, Notebook, Style
import datetime
import json
import os

class ReminderApp:
    def __init__(self, root):
        self.tasks = []
        # Define a custom file path for saving tasks
        self.file_directory = "C:/Users/Garys/.vscode/Pyhton/reminder"
        self.file_path = os.path.join(self.file_directory, "tasks.json")

        # Ensure the directory exists
        if not os.path.exists(self.file_directory):
            os.makedirs(self.file_directory)

        self.root = root
        self.root.title("Student Reminder App")
        self.style = Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", font=("Arial", 10), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#D3D3D3")
        self.load_tasks()
        self.create_welcome_page()

    def load_tasks(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                self.tasks = json.load(file)
                # Convert date strings back to datetime objects
                for task in self.tasks:
                    task["due_date"] = datetime.datetime.strptime(task["due_date"], "%Y-%m-%d %H:%M")

    def save_tasks(self):
        with open(self.file_path, "w") as file:
            # Convert datetime objects to strings for JSON serialization
            tasks_to_save = [{"task": task["task"], "due_date": task["due_date"].strftime("%Y-%m-%d %H:%M"), "priority": task["priority"]} for task in self.tasks]
            json.dump(tasks_to_save, file)

    def create_welcome_page(self):
        self.welcome_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.welcome_frame.pack(fill="both", expand=True)

        tk.Label(self.welcome_frame, text="Welcome to the Student Reminder App!", bg="#f0f8ff", font=("Arial", 20, "bold"), pady=20).pack()
        tk.Label(self.welcome_frame, text="Manage your tasks, schedules, and more.", bg="#f0f8ff", font=("Arial", 14)).pack(pady=10)

        start_button = tk.Button(self.welcome_frame, text="Get Started", command=self.start_application, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        start_button.pack(pady=20)

    def start_application(self):
        self.welcome_frame.destroy()
        self.create_widgets()

    def create_widgets(self):
        self.notebook = Notebook(self.root)
        self.notebook.pack(pady=10, expand=True, fill="both")

        self.task_tab = tk.Frame(self.notebook, bg="#f0f8ff")
        self.schedule_tab = tk.Frame(self.notebook, bg="#f5f5dc")
        self.report_tab = tk.Frame(self.notebook, bg="#f0fff0")  # New Report Tab

        self.notebook.add(self.task_tab, text="Tasks")
        self.notebook.add(self.schedule_tab, text="Schedule")
        self.notebook.add(self.report_tab, text="Reports")  # Add Report Tab

        self.create_task_tab()
        self.create_schedule_tab()
        self.create_report_tab()  # Create Report Tab

    def create_task_tab(self):
        frame = tk.Frame(self.task_tab, bg="#f0f8ff")
        frame.pack(pady=10, fill="x")
        tk.Label(frame, text="Task Name:", bg="#f0f8ff", font=("Arial", 12)).grid(row=0, column=0, padx=5, sticky="w")
        self.task_name_entry = tk.Entry(frame, width=30, font=("Arial", 10))
        self.task_name_entry.grid(row=0, column=1, padx=5, sticky="w")
        tk.Label(frame, text="Due Date (YYYY-MM-DD HH:MM):", bg="#f0f8ff", font=("Arial", 12)).grid(row=1, column=0, padx=5, sticky="w")
        self.due_date_entry = tk.Entry(frame, width=30, font=("Arial", 10))
        self.due_date_entry.grid(row=1, column=1, padx=5, sticky="w")
        add_task_btn = tk.Button(frame, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        add_task_btn.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

        self.tree = Treeview(self.task_tab, columns=("#1", "#2", "#3"), show="headings", height=10)  # Added Priority Column
        self.tree.heading("#1", text="Task")
        self.tree.heading("#2", text="Due Date")
        self.tree.heading("#3", text="Priority")  # Priority Heading
        self.tree.column("#1", width=200)
        self.tree.column("#2", width=150)
        self.tree.column("#3", width=100)  # Priority Column Width
        self.tree.pack(pady=10, fill="both", expand=True)

        btn_frame = tk.Frame(self.task_tab, bg="#f0f8ff")
        btn_frame.pack(pady=5, fill="x")
        remove_task_btn = tk.Button(btn_frame, text="Remove Task", command=self.remove_task, bg="#FF5733", fg="white", font=("Arial", 10, "bold"))
        remove_task_btn.grid(row=0, column=0, padx=5, sticky="ew")
        check_reminders_btn = tk.Button(btn_frame, text="Check Reminders", command=self.check_reminders, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        check_reminders_btn.grid(row=0, column=1, padx=5, sticky="ew")
        self.update_task_list()

    def create_schedule_tab(self):
        self.schedule_frame = tk.Frame(self.schedule_tab, bg="#f5f5dc")
        self.schedule_frame.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Label(self.schedule_frame, text="[Daily Schedule]", bg="#f5f5dc", font=("Arial", 14, "bold"), pady=10).pack()
        self.schedule_display = tk.Text(self.schedule_frame, height=20, wrap="word", font=("Arial", 10))
        self.schedule_display.pack(fill="both", expand=True)
        update_schedule_btn = tk.Button(self.schedule_tab, text="Update Schedule", command=self.create_daily_schedule, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        update_schedule_btn.pack(pady=5, fill="x")

    def create_report_tab(self):
        tk.Label(self.report_tab, text="Task Report", bg="#f0fff0", font=("Arial", 14, "bold"), pady=10).pack()
        self.report_display = tk.Text(self.report_tab, height=20, wrap="word", font=("Arial", 10))
        self.report_display.pack(fill="both", expand=True)
        generate_report_btn = tk.Button(self.report_tab, text="Generate Report", command=self.generate_report, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        generate_report_btn.pack(pady=5, fill="x")

    def add_task(self):
        task_name = self.task_name_entry.get().strip()
        due_date_str = self.due_date_entry.get().strip()
        if not task_name:
            messagebox.showerror("Error", "Task name cannot be empty.")
            return
        try:
            due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
            if due_date < datetime.datetime.now():
                messagebox.showerror("Error", "Due date cannot be in the past.")
                return
            priority = simpledialog.askstring("Priority", "Enter task priority (High, Medium, Low):") or "Low"  # Add Priority Input
            self.tasks.append({"task": task_name, "due_date": due_date, "priority": priority})
            self.save_tasks()
            self.update_task_list()
            self.task_name_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD HH:MM.")

    def update_task_list(self):
        self.tree.delete(*self.tree.get_children())
        for task in self.tasks:
            self.tree.insert("", tk.END, values=(task["task"], task["due_date"].strftime("%Y-%m-%d %H:%M"), task["priority"]))

    def remove_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No task selected.")
            return
        for item in selected_item:
            index = self.tree.index(item)
            self.tasks.pop(index)
        self.save_tasks()
        self.update_task_list()

    def check_reminders(self):
        current_time = datetime.datetime.now()
        due_soon = [task for task in self.tasks if 0 <= (task["due_date"] - current_time).total_seconds() <= 3600]
        if due_soon:
            reminders = "\n".join([f"{task['task']} (Due: {task['due_date'].strftime('%Y-%m-%d %H:%M')})" for task in due_soon])
            messagebox.showinfo("Upcoming Reminders", f"Tasks due soon:\n{reminders}")
        else:
            messagebox.showinfo("No Reminders", "No tasks are due within the next hour.")

    def create_daily_schedule(self):
        schedule = []
        start_time = datetime.datetime.combine(datetime.date.today(), datetime.time(6, 0))
        end_time = datetime.datetime.combine(datetime.date.today(), datetime.time(22, 0))
        current_time = start_time
        while current_time <= end_time:
            schedule.append(current_time.strftime("%I:%M %p"))
            current_time += datetime.timedelta(hours=1)
        display_text = ""
        for idx, time_slot in enumerate(schedule, start=1):
            task_name = self.tasks[idx - 1]["task"] if idx <= len(self.tasks) else "[Empty]"
            display_text += f"{time_slot}: {task_name}\n"
        self.schedule_display.delete(1.0, tk.END)
        self.schedule_display.insert(tk.END, display_text)

    def generate_report(self):
        self.report_display.delete(1.0, tk.END)
        if not self.tasks:
            self.report_display.insert(tk.END, "No tasks available to generate a report.")
            return
        report_text = "Task Report\n" + "="*50 + "\n"
        for task in self.tasks:
            report_text += (f"Task: {task['task']}\nDue Date: {task['due_date'].strftime('%Y-%m-%d %H:%M')}\nPriority: {task['priority']}\n" + "-"*50 + "\n")
        self.report_display.insert(tk.END, report_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()
