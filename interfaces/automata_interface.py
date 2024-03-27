import sqlite3
from sqlite3 import Error


class AutomataInterface:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.conn: sqlite3.Connection
        self.create_connection()

    def create_connection(self):
        """create a database connection to the SQLite database specified by db_file
        :return: Connection object or None
        """
        try:
            self.conn = sqlite3.connect("database/automata.db")
            self.create_table()
        except Error as e:
            print(e)

    def create_table(self):
        """create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
                """CREATE TABLE IF NOT EXISTS automata(
            regex TEXT NOT NULL PRIMARY KEY,
            nfa TEXT NOT NULL,
            dfa TEXT NOT NULL)"""
            )

        except Error as e:
            print(e)

    def insert_automata(self, automata):
        """
        Create a new project into the projects table
        :param conn:
        :param project:
        :return: project id
        """
        try:
            sql = """ INSERT INTO automata(regex,nfa,dfa)
                      VALUES(?,?,?) """
            cur = self.conn.cursor()
            cur.execute(sql, automata)
            self.conn.commit()
        except Error as e:
            print(e)

    def select_automata(self, regex):
        """
        Query tasks by priority
        :param conn: the Connection object
        :param priority:
        :return:
        """

        try:
            cur = self.conn.cursor()
            cur.execute("SELECT nfa, dfa FROM automata WHERE regex=?", (regex,))

            return cur.fetchall()
        except Error as e:
            print(e)
