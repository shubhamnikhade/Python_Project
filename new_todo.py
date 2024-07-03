import os

class Todo_Item:
    priority_options = ["High", "Medium", "Low"]

    def __init__(self, task: str, priority: str = None, done: bool = False):
        if type(task) == str:
            if task:
                self.task = task
            else:
                raise Exception("Task should not be empty")
        else:
            raise Exception("Task needs to be a string")

        if type(done) == bool:
            self.done = done
        else:
            raise Exception("Done argument needs to be a boolean")

        if priority:
            if priority in Todo_Item.priority_options:
                self.priority = priority
            else:
                raise Exception(
                    f"priority setting should be one of {Todo_Item.priority_options}")
        else:
            self.priority = None

    def __str__(self):
        return f'[{"x" if self.done else "o"}] - {self.priority if self.priority else "None"} : {self.task}'

    def finish(self):
        self.done = True

    def raise_priority(self):
        if not self.priority:
            return

        if self.priority == "Low":
            self.priority = "Medium"
        if self.priority == "Medium":
            self.priority = "High"


class Todo_List:
    def __init__(self, owner: str, todo_list: list = []):
        for item in todo_list:
            if type(item) != Todo_Item:
                raise Exception(f"Expected Todo Item got {type(item)}")

        self.todo_items = todo_list

        if type(owner) == str:
            if owner:
                self.owner = owner
            else:
                raise Exception("Owner name should not be empty")
        else:
            raise Exception("Owner name needs to be a string")

    def __str__(self):
        output = f"{self.owner}'s ToDo List\n"
        for item in self.todo_items:
            output += str(item) + "\n"
        return output

    def info(self):
        pending_tasks = {"High": 0, "Medium": 0, "Low": 0}
        finished_tasks = 0

        for item in self.todo_items:
            if item.done:
                finished_tasks += 1
            else:
                if item.priority:
                    pending_tasks[item.priority] += 1

        pending_summary = ", ".join(
            [f"{priority} - {count}" for priority, count in pending_tasks.items()])

        print(f"{self.owner}'s Todo list\n\nPending Tasks: {len(self.todo_items) - finished_tasks} \n{pending_summary}\nFinished Tasks: {finished_tasks}\n------------")

    def add_todo_item(self, todo_item):
        if type(todo_item) == Todo_Item:
            self.todo_items.append(todo_item)
        else:
            raise Exception(
                f"ToDo item must be of datatype Todo_Item not {type(todo_item)}")

    def create_todo_item(self, task: str, priority: str = None, done: bool = False):
        item = Todo_Item(task, priority, done)
        self.todo_items.append(item)

    def search_todo_item(self, query):
        output = []
        for item in self.todo_items:
            if query.lower() in item.task.lower():
                output.append(item)
        return output

    def list_todo_items(self, priority: str = "All", done: bool = None, sort: bool = False):
        output1 = []
        for item in self.todo_items:
            if (done == True) and (item.done == True):
                output1.append(item)
            elif (done == False) and (item.done == False):
                output1.append(item)
            elif (done == None):
                output1.append(item)

        output2 = []
        if priority == "All":
            output2 = output1
        else:
            for item in output1:
                if priority == item.priority:
                    output2.append(item)

        if sort:
            priority_dict = {
                "High": [],
                "Medium": [],
                "Low": [],
                None: [],
                "Finished": []
            }
            for item in output2:
                if item.done:
                    priority_dict["Finished"].append(item)
                else:
                    priority_dict[item.priority].append(item)

            output3 = priority_dict["High"] + priority_dict["Medium"] + priority_dict["Low"] + priority_dict[None] + priority_dict["Finished"]
        else:
            output3 = output2

        return output3

    def finish_todo_item(self, number):
        if 0 <= number < len(self.todo_items):
            self.todo_items[number].finish()
        else:
            print("Invalid task number")

    def delete_todo_item(self, number):
        if 0 <= number < len(self.todo_items):
            del self.todo_items[number]
        else:
            print("Invalid task number")

    def edit_todo_item(self, number, new_task=None, new_priority=None):
        if 0 <= number < len(self.todo_items):
            if new_task:
                self.todo_items[number].task = new_task
            if new_priority and new_priority in Todo_Item.priority_options:
                self.todo_items[number].priority = new_priority
        else:
            print("Invalid task number")

sample_items = [
    Todo_Item("Task 1", "High"),
    Todo_Item("Task 4", "Medium"),
    Todo_Item("Task 6", "Low", done=True),
    Todo_Item("Task 3", "High"),
    Todo_Item("Task 7", "Low", done=True),
    Todo_Item("Task 2", "High"),
    Todo_Item("Task 5", "Medium", done=True),
    Todo_Item("Task 11"),
    Todo_Item("Task 12", done=True),
    Todo_Item("Task 8", "Low"),
    Todo_Item("Task 9"),
    Todo_Item("Task 10", done=True),
]

sample_todo = Todo_List("Sample Person", sample_items)

def save_todo_list(todo_list):
    if not os.path.exists("./todo_data"):
        os.makedirs("./todo_data")
    with open(f"./todo_data/{todo_list.owner.lower()}.txt", "w") as f:
        lines = []
        for item in todo_list.todo_items:
            priority = item.priority if item.priority else "None"
            done = "True" if item.done else "False"
            task = item.task.replace(",", " ")
            line = ",".join([priority, done, task])
            lines.append(line)
        f.write("\n".join(lines))

def load_todo_list(owner_name):
    PATH = f"./todo_data/{owner_name.lower()}.txt"
    if os.path.exists(PATH):
        with open(PATH, "r") as f:
            todo_data = f.readlines()
            todo_items = []
            for line in todo_data:
                line = line.strip()
                priority, done, task = line.split(",")
                done = done == "True"
                priority = None if priority == "None" else priority
                todo_item = Todo_Item(task, priority, done)
                todo_items.append(todo_item)
            return Todo_List(owner_name, todo_items)
    return Todo_List(owner_name)

def main():
    print("Welcome to TODO APP")
    owner_name = input("Hello, Please enter your name: ").strip()
    while not owner_name:
        print("Owner Name can't be empty...")
        owner_name = input("Hello, Please enter your name: ").strip()

    user_list = load_todo_list(owner_name)
    print(f"Welcome {'Back' if user_list.todo_items else ''} {owner_name} to our TODO app")

    while True:
        print("""\n\nWhat do you want to do?
        
        1. Create a new task
        2. View existing tasks
        3. Mark a task as done
        4. Edit an old task
        5. Delete a task
        6. Exit
        """)
        choice = input("Enter a number (1-6): ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= 6):
            print("Choice must be a valid number between 1-6")
            continue

        choice = int(choice)
        if choice == 6:
            save_todo_list(user_list)
            print("Saving and exiting...")
            break
        elif choice == 1:
            task = input("Task: ").strip()
            while not task:
                print("Task must not be empty!")
                task = input("Task: ").strip()

            priority = input("Priority (High/Medium/Low or leave empty): ").strip().title()
            if priority not in Todo_Item.priority_options:
                priority = None

            done = input("Done? (y/N): ").strip().lower() in ['y', 'yes']
            created_item = Todo_Item(task, priority, done)
            user_list.add_todo_item(created_item)
            print("\nNew task created")
            print(created_item)
            save_todo_list(user_list)
        elif choice == 2:
            if not user_list.todo_items:
                print("No tasks available.")
            else:
                for i, item in enumerate(user_list.todo_items, 1):
                    status = "Done" if item.done else "Not Done"
                    print(f"{i}. {item.task} - Priority: {item.priority} - Status: {status}")
        elif choice == 3:
            if not user_list.todo_items:
                print("No tasks available.")
            else:
                for i, item in enumerate(user_list.todo_items, 1):
                    status = "Done" if item.done else "Not Done"
                    print(f"{i}. {item.task} - Priority: {item.priority} - Status: {status}")
                task_num = input("Enter task number to mark as done: ").strip()
                if task_num.isdigit() and 1 <= int(task_num) <= len(user_list.todo_items):
                    user_list.finish_todo_item(int(task_num) - 1)
                    print("Task marked as done.")
                    save_todo_list(user_list)
                else:
                    print("Invalid task number")
        elif choice == 4:
            if not user_list.todo_items:
                print("No tasks available.")
            else:
                for i, item in enumerate(user_list.todo_items, 1):
                    status = "Done" if item.done else "Not Done"
                    print(f"{i}. {item.task} - Priority: {item.priority} - Status: {status}")
                task_num = input("Enter task number to edit: ").strip()
                if task_num.isdigit() and 1 <= int(task_num) <= len(user_list.todo_items):
                    task_num = int(task_num) - 1
                    new_task = input("Enter new task description (leave blank to keep current): ").strip()
                    new_priority = input("Enter new priority (High/Medium/Low or leave blank to keep current): ").strip().title()
                    if new_priority and new_priority not in Todo_Item.priority_options:
                        new_priority = None
                    user_list.edit_todo_item(task_num, new_task, new_priority)
                    print("Task edited.")
                    save_todo_list(user_list)
                else:
                    print("Invalid task number")
        elif choice == 5:
            if not user_list.todo_items:
                print("No tasks available.")
            else:
                for i, item in enumerate(user_list.todo_items, 1):
                    status = "Done" if item.done else "Not Done"
                    print(f"{i}. {item.task} - Priority: {item.priority} - Status: {status}")
                task_num = input("Enter task number to delete: ").strip()
                if task_num.isdigit() and 1 <= int(task_num) <= len(user_list.todo_items):
                    user_list.delete_todo_item(int(task_num) - 1)
                    print("Task deleted.")
                    save_todo_list(user_list)
                else:
                    print("Invalid task number")

if __name__ == "__main__":
    main()



# Sure, here's a detailed explanation of the code:

# ### Overview
# This code implements a command-line TODO application that allows users to create, view, edit, delete, and mark tasks as done. The tasks are saved to and loaded from text files based on the user's name.

# ### Classes and Functions

# #### `Todo_Item` Class
# This class represents an individual task in the TODO list.
# - **Attributes:**
#   - `task`: The description of the task.
#   - `priority`: The priority of the task, which can be "High", "Medium", "Low", or `None`.
#   - `done`: A boolean indicating whether the task is completed.
# - **Methods:**
#   - `__init__(self, task, priority=None, done=False)`: Initializes the task with a description, optional priority, and completion status.
#   - `__str__(self)`: Returns a string representation of the task.
#   - `finish(self)`: Marks the task as done.
#   - `raise_priority(self)`: Increases the task's priority.

# #### `Todo_List` Class
# This class represents a list of TODO items for a specific user.
# - **Attributes:**
#   - `owner`: The name of the list owner.
#   - `todo_items`: A list of `Todo_Item` objects.
# - **Methods:**
#   - `__init__(self, owner, todo_list=[])`: Initializes the list with an owner's name and optional list of tasks.
#   - `__str__(self)`: Returns a string representation of the entire TODO list.
#   - `info(self)`: Prints a summary of the pending and finished tasks.
#   - `add_todo_item(self, todo_item)`: Adds a `Todo_Item` to the list.
#   - `create_todo_item(self, task, priority=None, done=False)`: Creates a new `Todo_Item` and adds it to the list.
#   - `search_todo_item(self, query)`: Searches for tasks that match the query.
#   - `list_todo_items(self, priority="All", done=None, sort=False)`: Lists tasks based on priority, completion status, and sorting.
#   - `finish_todo_item(self, number)`: Marks a task as done.
#   - `delete_todo_item(self, number)`: Deletes a task.
#   - `edit_todo_item(self, number, new_task=None, new_priority=None)`: Edits a task.

# ### File I/O Functions

# #### `save_todo_list(todo_list)`
# This function saves the tasks in a `Todo_List` object to a text file named after the owner's name in the `./todo_data` directory.
# - **Arguments:**
#   - `todo_list`: The `Todo_List` object to be saved.
# - **Logic:**
#   - Creates the `./todo_data` directory if it doesn't exist.
#   - Writes each task to the owner's text file, converting the task attributes to strings.

# #### `load_todo_list(owner_name)`
# This function loads tasks from a text file named after the owner and returns a `Todo_List` object.
# - **Arguments:**
#   - `owner_name`: The name of the list owner.
# - **Logic:**
#   - Reads the text file corresponding to the owner's name.
#   - Converts each line in the file to a `Todo_Item` object and adds it to the `Todo_List`.
#   - Returns a `Todo_List` object.

# ### Main Function

# #### `main()`
# This is the main function that runs the TODO application.
# - **Logic:**
#   - Greets the user and asks for their name.
#   - Loads the user's TODO list from a file or creates a new one.
#   - Presents a menu with options to create, view, mark as done, edit, delete tasks, or exit.
#   - Handles user input and calls the appropriate methods on the `Todo_List` object.
#   - Saves the TODO list to a file upon exiting.

# #### Detailed Menu Options:
# 1. **Create a new task:**
#    - Prompts the user for a task description.
#    - Optionally prompts for a priority and completion status.
#    - Creates a new `Todo_Item` and adds it to the user's `Todo_List`.
#    - Saves the updated list to a file.

# 2. **View existing tasks:**
#    - Lists all tasks with their descriptions, priorities, and completion statuses.

# 3. **Mark a task as done:**
#    - Lists all tasks.
#    - Prompts the user to enter the number of the task to mark as done.
#    - Marks the selected task as done and saves the updated list to a file.

# 4. **Edit an old task:**
#    - Lists all tasks.
#    - Prompts the user to enter the number of the task to edit.
#    - Prompts for new task description and priority (if provided, it updates the task).
#    - Saves the updated list to a file.

# 5. **Delete a task:**
#    - Lists all tasks.
#    - Prompts the user to enter the number of the task to delete.
#    - Deletes the selected task and saves the updated list to a file.

# 6. **Exit:**
#    - Saves the user's TODO list to a file and exits the program.

# ### Example Usage
# - Run the script.
# - Enter your name.
# - Follow the prompts to add, view, edit, mark as done, or delete tasks.
# - The tasks are saved to a text file named after your name in the `./todo_data` directory.

# This single-file TODO app is simple and efficient, utilizing object-oriented principles and file I/O to manage tasks.

