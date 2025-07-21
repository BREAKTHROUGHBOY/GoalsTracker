from task_manager19725 import Task

tasks = []
import json
def load_tasks(filename="data_saver.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            for item in data:
                task = Task(
                    task_name=item['task_name'],
                    status=item['status'],
                    task_id=item['task_id']
                    )
                tasks.append(task)
        print("> Tasks loaded from file successfully!")
    except FileNotFoundError:
        print("> No saved data found.")
load_tasks()
for t in tasks:
    print(t)


import uuid
from datetime import datetime
from tabulate import tabulate

class Goal:
    def __init__(self, title, description, category, priority, deadline):
        self.goal_id = str(uuid.uuid4())[:8]  # shortened UUID
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.deadline = deadline
        self.created_at = datetime.now()
        self.status = "In Progress"
        self.milestones = []
        self.tasks_linked = []

    def __str__(self):
        return (
            f"\n\033[1m=== Goal ID: {self.goal_id} ===\033[0m\n"
            f"\033[94mTitle:\033[0m {self.title}\n"
            f"\003[94mDescription: \033[0m {self.description}\n"
            f"\003[94mPriority: \033[0m {self.priority}\n"
            f"\033[94mCategory:\033[0m {self.category}\n"
            f"\033[94mDeadline:\033[0m {self.deadline}\n"
            f"\033[94mStatus:\033[0m {self.status}\n"
            f"\033[94mMilestones:\033[0m {self.milestones}\n"
            f"\033[94mLinked Tasks:\033[0m {self.tasks_linked}\n"
        )

    def to_dict(self):
        return {
            "goal_id": self.goal_id,
            "title": self.title,
            "description" : self.description,
            "category": self.category,
            "priority": self.priority,
            "deadline": self.deadline,
            "created_at": self.created_at.strftime("%d-%m-%Y %H:%M:%S"),
            "status": self.status,
            "milestones": self.milestones,
            "linked_tasks": self.tasks_linked,
        }


class GoalTracker:
    def __init__(self):
        self.goals = []

    def add_goal(self, title, description, category, priority, deadline):
        new_goal = Goal(title=title, description=description, priority=priority, category=category, deadline=deadline)
        self.goals.append(new_goal)
        print(f"\n\033[92m✔ Goal '{title}' added successfully with ID {new_goal.goal_id}\033[0m")

    def delete_goal(self, id_or_title):
        for goal in self.goals:
            if goal.goal_id == id_or_title or goal.title == id_or_title:
                self.goals.remove(goal)
                print(f"\033[91m✘ Goal '{goal.title}' deleted successfully.\033[0m")
                return
        print("\033[91m> No matching goal found!\033[0m")

    def view_goals_summary(self):
        if not self.goals:
            print("\033[90m> No goals to display.\033[0m")
            return
        table = [[g.goal_id, g.title, g.status, g.deadline] for g in self.goals]
        headers = ["Goal ID", "Title", "Status", "Deadline"]
        print("\n\033[1m\033[4mYour Goals Summary:\033[0m")
        print(tabulate(table, headers, tablefmt="fancy_grid"))

    def view_goal_by_id(self, id_or_title):
        for goal in self.goals:
            if goal.goal_id == id_or_title or goal.title == id_or_title:
                print(goal)
                return
        print("\033[91m> No matching goal found!\033[0m")

    def link_tasks(self, goal_id, task_id):
        for goal in self.goals:
            if goal.goal_id == goal_id:
                if task_id not in goal.tasks_linked:
                    goal.tasks_linked.append(task_id)
                    print(f"\033[92m✔ Task ID {task_id} linked to Goal ID {goal_id}\033[0m")
                else:
                    print(f"\033[93m! Task ID {task_id} is already linked.\033[0m")
                return
        print("\033[91m> No matching goal found!\033[0m")

    def check_linked_tasks(self, id_or_title):
        for goal in self.goals:
            if goal.goal_id == id_or_title or goal.title == id_or_title:
                print(f"\n\033[1mLinked Tasks for Goal '{goal.title}':\033[0m")
                if not goal.tasks_linked:
                    print("→ None")
                    return
                for tid in goal.tasks_linked:
                    task = self.get_task_by_id(tid)
                    if task:
                        print(f"  → \033[94m{task.task_name}\033[0m (ID: {task.task_id}, Status: {task.status})")
                    else:
                        print(f"  → Task ID {tid} not found in global task list.")
                return
        print("\033[91m> No matching goal found!\033[0m")

    def delete_linked_task(self, id_or_title, task_id):
        for goal in self.goals:
            if goal.goal_id == id_or_title or goal.title == id_or_title:
                if task_id in goal.tasks_linked:
                    goal.tasks_linked.remove(task_id)
                    print(f"\033[91m✘ Task ID {task_id} removed from Goal '{goal.title}'\033[0m")
                    return
                else:
                    print(f"\033[93m! Task ID {task_id} is not linked with Goal '{goal.title}'\033[0m")
        print("\033[91m> No matching goal found!\033[0m")

    def get_task_by_id(self, task_id):
        for task in tasks:
            if task.task_id == task_id:
                return task
        return None

    def add_milestone(self, id_or_title, milestones=[]):
        for goal in self.goals:
            if goal.goal_id == id_or_title or goal.title == id_or_title:
                goal.milestones.extend(m for m in milestones)
                print("\n🚀 Milestones Added Successfully:")
                print(f"- Goal: {goal.title}")
                print("- Milestones Added:")
                for m in milestones:
                    print(f"   → {m}")
                return
        print(f"⚠️ No Goal Found with '{id_or_title}'")

    def delete_milestones(self, id_or_title, milestone):
        for goal in self.goals:
            if goal.goal_id == id_or_title or goal.title == id_or_title:
                if milestone in goal.milestones:
                    goal.milestones.remove(milestone)
                    print("\n🗑️ Milestone Deleted Successfully:")
                    print(f"- Milestone: {milestone}")
                    print(f"- From Goal: {goal.title}")
                    return
                else:
                    print(f"❌ Milestone '{milestone}' Not Found in Goal '{goal.title}'")
                    return
        print("⚠️ No Matching Goal Found!")

    def mark_completed(self, id_or_title):
        for goal in self.goals:
            if goal.goal_id == id_or_title or goal.title == id_or_title:
                goal.status = "completed"
                print("\n✅ Goal Marked as Completed:")
                print(f"- Goal Title: {goal.title}")
                print("🎉 Congratulations on completing this goal! Keep pushing forward, Champion!")
                return
        print(f"⚠️ No Goal Found with '{id_or_title}'")

    
    def save_tasks(self, filename="goals_data_saver.json"):
        if not self.goals:
            print("\033[91m[×] No Goals to save.\033[0m")  # Bright Red
            return
        with open(filename, "w") as f:
            json.dump([goal.to_dict() for goal in self.goals], f, indent=4)
        print("\033[92m[✓] Goals saved successfully to:\033[0m \033[96m" + filename + "\033[0m")

    def load_tasks(self, filename="goals_data_saver.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                for item in data:
                    goal = Goal(
                        goal_id=item["goal_id"],
                        title=item["title"],
                        description=item["description"],
                        category=item["category"],
                        priority=item["priority"],
                        deadline=item["deadline"],
                        created_at=item["created_at"],
                        status=item["status"],
                        milestones=item["milestones"],
                        linked_tasks=item["linked_tasks"]
                    )
                    self.goals.append(goal)
            print("\033[94m[✓] Goals loaded successfully from:\033[0m \033[96m" + filename + "\033[0m")
        except FileNotFoundError:
            print("\033[93m[!] No saved goal data found in file:\033[0m \033[90m" + filename + "\033[0m")


if __name__ == "__main__":
    tracker = GoalTracker()
    tracker.load_tasks()

    def show_menu():
        print("\n\033[1m\033[94m=== Goal Tracker Menu ===\033[0m")
        print("1. Add Goal")
        print("2. View All Goals")
        print("3. View Goal by ID or Title")
        print("4. Delete Goal")
        print("5. Add Milestones")
        print("6. Delete Milestone")
        print("7. Link Task to Goal")
        print("8. Check Linked Tasks")
        print("9. Delete Linked Task")
        print("10. Mark Goal as Completed")
        print("11. Save Goals")
        print("0. Exit")

    while True:
        show_menu()
        choice = input("\n\033[96mEnter your choice: \033[0m")

        if choice == "1":
            print("\n\033[92m--- Add New Goal ---\033[0m")
            title = input("Title: ")
            description = input("Description: ")
            category = input("Category: ")
            priority = input("Priority (Low/Medium/High): ")
            deadline = input("Deadline (DD-MM-YYYY): ")
            tracker.add_goal(title, description, category, priority, deadline)

        elif choice == "2":
            tracker.view_goals_summary()

        elif choice == "3":
            id_or_title = input("Enter Goal ID or Title: ")
            tracker.view_goal_by_id(id_or_title)

        elif choice == "4":
            id_or_title = input("Enter Goal ID or Title to delete: ")
            tracker.delete_goal(id_or_title)

        elif choice == "5":
            id_or_title = input("Enter Goal ID or Title to add milestones: ")
            milestones = input("Enter milestones (comma-separated): ").split(",")
            tracker.add_milestone(id_or_title, [m.strip() for m in milestones])

        elif choice == "6":
            id_or_title = input("Enter Goal ID or Title: ")
            milestone = input("Enter milestone to delete: ")
            tracker.delete_milestones(id_or_title, milestone.strip())

        elif choice == "7":
            tracker.view_goals_summary()
            goal_id = input("Enter Goal ID to link a task: ")
            task_id = input("Enter Task ID to link: ")
            tracker.link_tasks(goal_id, task_id)

        elif choice == "8":
            id_or_title = input("Enter Goal ID or Title to check linked tasks: ")
            tracker.check_linked_tasks(id_or_title)

        elif choice == "9":
            id_or_title = input("Enter Goal ID or Title: ")
            task_id = input("Enter Task ID to remove: ")
            tracker.delete_linked_task(id_or_title, task_id)

        elif choice == "10":
            id_or_title = input("Enter Goal ID or Title to mark as completed: ")
            tracker.mark_completed(id_or_title)

        elif choice == "11":
            tracker.save_tasks()

        elif choice == "0":
            print("\n\033[91mExiting Goal Tracker. Goodbye, Leader!\033[0m")
            break

        else:
            print("\033[91mInvalid choice. Please try again.\033[0m")
