import sqlite3
from functools import wraps


def dict_factory(cursor, row):
    """Row factory that returns dicts mapping column name to column value,
    as opposed to the default factory, which returns tuples.
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class sqlite(object):
    """Non-transaction/autocommit context. Use:

    with sqlite(db_path) as (_, cursor):
        cursor.execute('select foo from bar')
        rows = cursor.fetchall()
        ...

    """

    def __init__(self, db, timeout=0.4):
        self.db = db
        self.timeout = timeout
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db, timeout=self.timeout)
        self.conn.row_factory = dict_factory
        self.conn.isolation_level = None
        self.cursor = self.conn.cursor()
        return self.conn, self.cursor

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.cursor.close()
        self.conn.close()


class sqlite_tx(sqlite):
    """Transactional context. Use:

    with sqlite_tx(db_path) as (_, cursor):
        cursor.execute('select foo from bar')
        rows = cursor.fetchall()
        ...

    The body of the `with` block is executed inside a sqlite
    transaction. If an exception is raised in the body, the
    transaction is rolled back.
    """

    def __enter__(self):
        conn, cursor = super().__enter__()
        cursor.execute("begin exclusive transaction")
        return conn, cursor

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            self.cursor.execute("commit")
        else:
            self.cursor.execute("rollback")
        super().__exit__(exc_type, exc_value, exc_tb)


def retry(fn):
    # These errors can happen randomly due to contention and it's safe
    # to retry when they happen.
    errors = ("database is locked", "disk I/O error")

    @wraps(fn)
    def fn_wrapper(*args, **kwargs):
        while True:
            try:
                return fn(*args, **kwargs)
            except sqlite3.OperationalError as e:
                if str(e) not in errors:
                    raise

    return fn_wrapper


def migrate(db_path, migrations):
    """A migration is a function that takes a cursor and uses it to modify
    the db in some way. `migrations` is a list of such functions.
    """
    with sqlite_tx(db_path) as (_, cursor):
        # If the _Migration table doesn't exist, create it.
        try:
            cursor.execute("select * from _Migration")
            table_exists = True
        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                table_exists = False
            else:
                raise

        if not table_exists:
            cursor.execute("create table _Migration (migration_id integer not null)")
            cursor.execute("insert into _Migration (migration_id) values (?)", (0,))

        # The migration_id indicates the number/position in the
        # migrations list of the most recent migration applied. We
        # apply the rest of the migrations in the list, if any.

        cursor.execute("select migration_id from _Migration")
        rows = cursor.fetchall()
        migration_id = rows[0]["migration_id"]

        if len(migrations) < migration_id:
            raise Exception("The migration list got smaller.")

        migrations_to_apply = migrations[migration_id:]
        print(f"Applying {len(migrations_to_apply)} migrations.")
        for migration in migrations_to_apply:
            migration(cursor)
            cursor.execute("update _Migration set migration_id = migration_id + 1")


def sql(sql_text):
    """This function can be used as the most basic way to define a migration. E.g.,
    migration = sql("drop table Foo")
    """
    return lambda cursor: cursor.execute(sql_text)
