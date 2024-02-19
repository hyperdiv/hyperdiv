import pytest
import os
import tempfile
from ..sqlite import sql, sqlite, sqlite_tx, retry, migrate


@retry
def insert_user_1(db_path, name, age):
    with sqlite(db_path) as (_, cursor):
        cursor.execute("insert into Users (name, age) values (?, ?)", (name, age))


@retry
def insert_user_2(db_path, name, age, role):
    with sqlite_tx(db_path) as (_, cursor):
        cursor.execute(
            "insert into Users (name, age, role) values (?, ?, ?)", (name, age, role)
        )


@retry
def select_users_1(db_path):
    with sqlite(db_path) as (_, cursor):
        cursor.execute("select name, age from Users")
        return cursor.fetchall()


@retry
def select_users_2(db_path):
    with sqlite_tx(db_path) as (_, cursor):
        cursor.execute("select name, age, role from Users")
        return cursor.fetchall()


@retry
def failed_insert_user_2(db_path, name, age, role):
    with sqlite_tx(db_path) as (_, cursor):
        cursor.execute(
            "insert into Users (name, age, role) values (?, ?, ?)", (name, age, role)
        )
        raise Exception("Failure")


def test_sqlite():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        db_path = f.name

    migrations = [sql("create table Users (name, age)")]

    migrate(db_path, migrations)
    # Migrating again does nothing
    migrate(db_path, migrations)

    insert_user_1(db_path, "Steve", 40)
    insert_user_1(db_path, "Andy", 32)

    users = select_users_1(db_path)
    assert users == [{"name": "Steve", "age": 40}, {"name": "Andy", "age": 32}]

    migrations += [sql("alter table Users add column role")]
    migrate(db_path, migrations)

    insert_user_2(db_path, "Mary", 23, "Manager")
    insert_user_2(db_path, "Joe", 38, "Engineer")

    users = select_users_2(db_path)
    assert users == [
        {"name": "Steve", "age": 40, "role": None},
        {"name": "Andy", "age": 32, "role": None},
        {"name": "Mary", "age": 23, "role": "Manager"},
        {"name": "Joe", "age": 38, "role": "Engineer"},
    ]

    with pytest.raises(Exception):
        failed_insert_user_2(db_path, "Jimmy", 50, "Manager")

    # The inserted record got rolled back
    assert select_users_2(db_path) == users

    os.remove(db_path)
