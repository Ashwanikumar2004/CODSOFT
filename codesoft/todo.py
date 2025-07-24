import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

FILENAME = "tasks.json"

class Task:
    def __init__(self, title, due_date=None, priority="Normal", completed=False):
        self.title = title
        self.due_date = due_date
        self.priority = priority
        self.completed = completed

    def to_dict(self):
        return {
            "title": self.title,
            "due_date": self.due_date,
            "priority": self.priority,
            "completed": self.completed
        }

    def __str__(self):
        status = "✓" if self.completed else "✗"
        return f"{self.title} | Due: {self.due_date or 'N/A'} | Priority: {self.priority} | Done: {status}"

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.tasks = []

        self.listbox = tk.Listbox(root, width=70)
        self.listbox.pack(pady=10)

        self.add_btn = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_btn.pack(fill="x")

        self.done_btn = tk.Button(root, text="Mark as Done", command=self.mark_done)
        self.done_btn.pack(fill="x")

        self.delete_btn = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_btn.pack(fill="x")

        self.save_btn = tk.Button(root, text="Save Tasks", command=self.save_tasks)
        self.save_btn.pack(fill="x")

        self.load_tasks()

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            self.listbox.insert(tk.END, str(task))

    def add_task(self):
        title = simpledialog.askstring("Add Task", "Task Title:")
        if not title:
            return
        due = simpledialog.askstring("Due Date", "Enter due date (optional):")
        priority = simpledialog.askstring("Priority", "Priority (Low/Normal/High):", initialvalue="Normal")
        task = Task(title, due, priority)
        self.tasks.append(task)
        self.refresh_listbox()

    def mark_done(self):
        try:
            idx = self.listbox.curselection()[0]
            self.tasks[idx].completed = True
            self.refresh_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to mark as done.")

    def delete_task(self):
        try:
            idx = self.listbox.curselection()[0]
            del self.tasks[idx]
            self.refresh_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def save_tasks(self):
        with open(FILENAME, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)
        messagebox.showinfo("Saved", "Tasks saved successfully!")

    def load_tasks(self):
        if os.path.exists(FILENAME):
            with open(FILENAME, "r") as f:
                data = json.load(f)
                for item in data:
                    self.tasks.append(Task(**item))
        self.refresh_listbox()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
