import json
import os
from datetime import datetime
from pathlib import Path

class TodoApp:
    def __init__(self, storage_file='tasks.json'):
        """
        Initialize To-Do app with file-based storage.
        
        Args:
            storage_file: JSON file path for storing tasks
        """
        self.storage_file = storage_file
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """
        Load tasks from JSON file.
        
        Returns:
            List of task dictionaries
        """
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_tasks(self):
        """
        Save tasks to JSON file.
        """
        with open(self.storage_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
        print(f"✓ Tasks saved to {self.storage_file}")

    def add_task(self, title, priority='medium', due_date=None):
        """
        Add a new task.
        
        Args:
            title: Task title
            priority: Priority level (low, medium, high)
            due_date: Due date in YYYY-MM-DD format
        """
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'priority': priority,
            'completed': False,
            'created_at': datetime.now().isoformat(),
            'due_date': due_date
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"✓ Task added: {title}")
        return task

    def complete_task(self, task_id):
        """
        Mark task as completed.
        
        Args:
            task_id: ID of task to complete
        """
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                self.save_tasks()
                print(f"✓ Task completed: {task['title']}")
                return
        print(f"✗ Task not found")

    def delete_task(self, task_id):
        """
        Delete a task.
        
        Args:
            task_id: ID of task to delete
        """
        self.tasks = [t for t in self.tasks if t['id'] != task_id]
        self.save_tasks()
        print(f"✓ Task deleted")

    def get_all_tasks(self):
        """
        Get all tasks.
        
        Returns:
            List of all tasks
        """
        return self.tasks

    def get_pending_tasks(self):
        """
        Get incomplete tasks.
        
        Returns:
            List of pending tasks
        """
        return [t for t in self.tasks if not t['completed']]

    def get_completed_tasks(self):
        """
        Get completed tasks.
        
        Returns:
            List of completed tasks
        """
        return [t for t in self.tasks if t['completed']]

    def get_tasks_by_priority(self, priority):
        """
        Get tasks by priority level.
        
        Args:
            priority: Priority level (low, medium, high)
            
        Returns:
            List of tasks with specified priority
        """
        return [t for t in self.tasks if t['priority'] == priority and not t['completed']]

    def display_tasks(self, tasks=None):
        """
        Display tasks in formatted table.
        
        Args:
            tasks: List of tasks to display (default: all tasks)
        """
        if tasks is None:
            tasks = self.tasks

        if not tasks:
            print("No tasks found.")
            return

        print("\n" + "="*80)
        print(f"{'ID':<4} {'Title':<30} {'Priority':<10} {'Status':<12} {'Due Date':<12}")
        print("="*80)
        for task in tasks:
            status = "✓ Done" if task['completed'] else "⏳ Pending"
            due = task.get('due_date', 'N/A')
            print(f"{task['id']:<4} {task['title']:<30} {task['priority']:<10} {status:<12} {due:<12}")
        print("="*80 + "\n")

    def interactive_menu(self):
        """
        Display interactive menu for managing tasks.
        """
        while True:
            print("\n📝 TO-DO LIST APPLICATION")
            print("1. Add task")
            print("2. View all tasks")
            print("3. View pending tasks")
            print("4. View completed tasks")
            print("5. Complete task")
            print("6. Delete task")
            print("7. Filter by priority")
            print("8. Exit")
            
            choice = input("\nSelect option (1-8): ").strip()
            
            if choice == '1':
                title = input("Task title: ").strip()
                priority = input("Priority (low/medium/high) [medium]: ").strip() or 'medium'
                due_date = input("Due date (YYYY-MM-DD) [optional]: ").strip() or None
                self.add_task(title, priority, due_date)
            
            elif choice == '2':
                self.display_tasks()
            
            elif choice == '3':
                self.display_tasks(self.get_pending_tasks())
            
            elif choice == '4':
                self.display_tasks(self.get_completed_tasks())
            
            elif choice == '5':
                self.display_tasks(self.get_pending_tasks())
                try:
                    task_id = int(input("Enter task ID to complete: "))
                    self.complete_task(task_id)
                except ValueError:
                    print("Invalid ID")
            
            elif choice == '6':
                self.display_tasks()
                try:
                    task_id = int(input("Enter task ID to delete: "))
                    self.delete_task(task_id)
                except ValueError:
                    print("Invalid ID")
            
            elif choice == '7':
                priority = input("Filter by priority (low/medium/high): ").strip()
                self.display_tasks(self.get_tasks_by_priority(priority))
            
            elif choice == '8':
                print("Goodbye!")
                break
            
            else:
                print("Invalid option")


if __name__ == "__main__":
    app = TodoApp()
    app.interactive_menu()
