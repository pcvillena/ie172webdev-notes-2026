import apps.dbconnect as db
from datetime import datetime

def addfewgenres():
    # We use the function modifydatabase() -- it has 2 arguments
    # The first argument is the sql code, where we use a placeholder %s
    # The second argument is ALWAYS a list of values to replace the %s in the sql code

    sqlcode1 = """ INSERT INTO genres (
        genre_name
    )
    VALUES (%s)"""
    # note that even if genre_modified_date and genre_delete_ind have
    # NOT NULL constraints, we do not need to specify their values because
    # they have DEFAULT values

    db.modifydatabase(sqlcode1, ['Action'])


    # this is an alternative to the scripts above
    # we provide the values of the fields with default values regardless
    sqlcode2 = """ INSERT INTO genres (
        genre_name,
        genre_modified_date, 
        genre_delete_ind
    )
    VALUES (%s, %s, %s)"""
    db.modifydatabase(sqlcode2, ['Horror', datetime.now(), False])

    # Just some feedback that the code succeeded
    print('done!')
    

# addfewgenres()

# querydatafromdatabase(sql, values, dfcolumns)
sql = 'SELECT * FROM genres'
values = []
colnames = ['id', 'name', 'mod_on', 'del_ind']

print(db.querydatafromdatabase(sql, values, colnames))



sql_resetgenres = """
    TRUNCATE TABLE genres RESTART IDENTITY CASCADE
"""
db.modifydatabase(sql_resetgenres, [])  
addfewgenres()
