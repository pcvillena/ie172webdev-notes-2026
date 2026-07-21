
import pandas as pd
import psycopg2


def getdblocation():
    db = psycopg2.connect(
        host='localhost', 
        database='ie172sampledb', 
        user='postgres', 
        port=5432, 
        password='password', 
    )

    return db


def modifyDB(sql, values):
    db = getdblocation()

    # We create a cursor object
    # Cursor - a mechanism used to manipulate db objects on a per-row basis
    # In this case, a cursor is used to add/edit each row
    cursor = db.cursor()

    # Execute the sql code with the cursor value
    cursor.execute(sql, values)

    # Make the changes to the db persistent
    db.commit()
    # Close the connection (so nobody else can use it)
    db.close()


def getDataFromDB(sql, values, dfcolumns):
    # ARGUMENTS
    # sql -- sql query with placeholders (%s)
    # values -- values for the placeholders
    # dfcolumns -- column names for the output

    db = getdblocation()
    cur = db.cursor()
    cur.execute(sql, values)
    rows = pd.DataFrame(cur.fetchall(), columns=dfcolumns)
    db.close()
    return rows