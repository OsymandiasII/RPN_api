from flask import Flask

import sqlite3 as db

app = Flask(__name__)

# Perform all database operations
# All function follow the same pattern :
#   - SQl query
#   - Get the cursor and execute the query with the data/task provided
#   - Return data (either a bool, the id of the stack, or the data inserted)

class DB_Service:

    def __init__(self):
        self.conn = db.connect('rpm.db')


    def create_new_stack(self, data):
        sql = 'INSERT INTO Operations (name, operation) VALUES(?, ?)'
        cur = self.conn.cursor()
        cur.execute(sql, data)
        self.conn.commit()
        return cur.lastrowid

    def insert_new_value(self, task):
        sql = ' UPDATE Operations SET operation = ? WHERE id = ?'
        cur = self.conn.cursor()
        cur.execute(sql, task)
        self.conn.commit()
        return True

    def list_stacks(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM Operations")
        data = cur.fetchall()
        return data

    def get_stack(self, stack_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM Operations WHERE id = " + str(stack_id))
        data = cur.fetchall()
        return data

    def delete_stack(self, stack_id):
        sql = ' DELETE FROM Operations WHERE id = ?'
        cur = self.conn.cursor()
        cur.execute(sql, (stack_id,))
        self.conn.commit()
        return True

    def update_stack_name(self, task):
        sql = ' UPDATE Operations SET name = ? WHERE id = ?'
        cur = self.conn.cursor()
        cur.execute(sql, task)
        self.conn.commit()
        return True
