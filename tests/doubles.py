class FakeUserRepository:
    def __init__(self):
        self.users_by_username = {}

    def add(self, user):
        self.users_by_username[user.username] = user

    def get_by_username(self, username):
        return self.users_by_username.get(username)


class FakeTaskRepository:
    def __init__(self):
        self.tasks = {}

    def add(self, task):
        self.tasks[task.id] = task

    def get(self, task_id):
        return self.tasks.get(task_id)

    def list_by_owner(self, owner_id):
        return [
            task for task in self.tasks.values() if task.owner_id == owner_id
        ]

    def update(self, task):
        self.tasks[task.id] = task

    def delete(self, task_id):
        self.tasks.pop(task_id, None)


class SpyReminderSender:
    def __init__(self):
        self.sent_reminders = []

    def send_reminder_created(self, user, task):
        self.sent_reminders.append((user, task))


class FailingReminderSender:
    def send_reminder_created(self, user, task):
        raise RuntimeError("external reminder system failed")
