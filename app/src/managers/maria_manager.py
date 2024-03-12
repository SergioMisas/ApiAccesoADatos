from mariadb import connect


def get_mariadb_connection():
    return connect(
        user="root",
        password="example",
        host="mariadb",
        database="example",
    )
