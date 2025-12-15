class TaskController:
    def __init__(self):
        self.tasks = []

    def add_task(self, title):
        self.tasks.append({"title": title, "completed": False})

    def delete_task(self, index):
        del self.tasks[index]

    def toggle_status(self, index):
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]

    def update_task(self, index, new_title):
        self.tasks[index]["title"] = new_title
