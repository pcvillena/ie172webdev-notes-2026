import dbconnect as db


def addGenres(genre_name):
    sqlcode = """
        INSERT INTO genres (
            genre_name
        )
        VALUES (%s)
    """
    # I do not have to insert values for the other columns, 
    # they already take default values -- see auto-values
    
    values = [genre_name]
    # This value genre_name will replace the %s in sqlcode
    
    db.modifyDB(sqlcode, values)
    

def getGenresTable():
    sqlcode = """SELECT genre_id, genre_name, genre_modified_on
    FROM genres
    WHERE NOT genre_delete_ind
    ORDER BY 2"""    

    values = [] # we do not have any %s in the SQL
    cols = ['id', 'name', 'modified_on'] # these are column names for the table
   
    # the table is stored in variable genres_db as a dataframe 
    genres_db = db.getDataFromDB(sqlcode, values, cols)
    
    return genres_db


def clearGenres():
    db.modifyDB(
        "TRUNCATE TABLE genres RESTART IDENTITY CASCADE"
    )
    


if __name__ == '__main__':
    # Add genres to the db
    new_genres = ['Action', 'Drama', 'Horror']

    for genre in new_genres:
        addGenres(genre)

    # Check the contents of the genre table
    print(getGenresTable())
    

    



    

    