from mariadb import connect
from src.models.user import User
from src.models.task import Task
from uuid import UUID


class MariaManager:
    def __init__(self, us, pwd, db):
        self.connection = connect(
            user=us,
            password=pwd,
            host="mariadb",
            port=3306,
            database=db,
        )

        cursor = self.connection.cursor(named_tuple=True)
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS user (id VARCHAR(255) NOT NULL PRIMARY KEY,password VARCHAR(255) NOT NULL)"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS task (id VARCHAR(255) PRIMARY KEY,user VARCHAR(255) NOT NULL,text VARCHAR(501) NOT NULL,created_at VARCHAR(100) NOT NULL,updated_at VARCHAR(100) NOT NULL,checked BOOLEAN NOT NULL,important BOOLEAN NOT NULL,FOREIGN KEY (user) REFERENCES user(id))"
        )
        cursor.close()

    def get_users(self) -> list[User]:
        cursor = self.connection.cursor(named_tuple=True)
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        cursor.close()
        return users

    def create_user(self, user: User) -> User | None:
        cursor = self.connection.cursor(named_tuple=True)
        cursor.execute(
            "INSERT INTO user(id, password) VALUES(%s, %s)", (user.id, user.password)
        )
        self.connection.commit()
        cursor.close()
        return user

    def update_user(self, user: User) -> User | None:
        cursor = self.connection.cursor(named_tuple=True)
        cursor.execute(
            "UPDATE user SET password = %s WHERE id = %s", (user.password, user.id)
        )
        self.connection.commit()
        cursor.close()
        return user

    def delete_user(self, id: str) -> User | None:
        cursor = self.connection.cursor(named_tuple=True)
        cursor.execute("DELETE FROM user WHERE id = %s", (id))
        self.connection.commit()
        cursor.execute("DELETE FROM task WHERE user = %s", (id))
        cursor.close()
        return User

    def get_tasks(self) -> list[Task]:
        cursor = self.connection.cursor(named_tuple=True)
        cursor.execute("SELECT * FROM task")
        tasks = cursor.fetchall()
        cursor.close()
        return tasks

    def create_task(self, task: Task) -> Task | None:
        cursor = self.connection.cursor(named_tuple=True)
        cursor.execute(
            "INSERT INTO task(id, user, text, created_at, updated_at, checked, important) VALUES(%s, %s, %s, %s, %s, %s, %s)",
            (
                str(task.id),
                task.user,
                task.text,
                task.created_at,
                task.updated_at,
                task.checked,
                task.important,
            ),
        )
        self.connection.commit()
        cursor.close()
        return task

    def update_task(self, task: Task) -> Task | None:
        cursor = self.connection.cursor(named_tuple=True)
        cursor.execute(
            "UPDATE task SET user = %s, text = %s created_at = %s updated_at = %s checked = %s important = %s WHERE id = %s",
            (
                task.user,
                task.text,
                task.created_at,
                task.updated_at,
                task.checked,
                task.important,
                str(task.id),
            ),
        )
        self.connection.commit()
        cursor.close()
        return task

    def delete_task(self, id: UUID) -> Task | None:
        cursor = self.connection.cursor(named_tuple=True)
        cursor.execute("DELETE FROM task WHERE id = %s", (id))
        self.connection.commit()
        cursor.close()
        return Task

    def get_tasks_by_user(self, user: str) -> list[Task]:
        cursor = self.connection.cursor(named_tuple=True)
        cursor.execute("SELECT * FROM task WHERE user = %s", (user))
        tasks = cursor.fetchall()
        cursor.close()
        return tasks
