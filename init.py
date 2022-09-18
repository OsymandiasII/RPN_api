from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3 as db


app = Flask(__name__)



def create_app():

    #Add conf here

    #Setup the api blueprint
    from api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    # Connect to db
    conn = db.connect('rpm.db')

    # Create table if it doesn't exist in db
    op_table = """ CREATE TABLE IF NOT EXISTS Operations (
                                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                        name TEXT,
                                        operation TEXT,
                                        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                                    );"""

    if conn is not None:
        # create projects table
        c = conn.cursor()
        c.execute(op_table)

    else:
        print("Error! cannot create the database connection.")

    conn.close()

    CORS(app)

    return app



app=create_app()
