import mariadb as db
import dbinteractions as dbi

def create_user_id(follow_id, user_id):
    success = False
    id = None
    conn, cursor = dbi.connect_db()
    try:
        cursor.execute("INSERT INTO user_session(follow_id, user_id) VALUES(?,?)", [follow_id, user_id])
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
            id = cursor.lastrowid
    except db.ProgrammingError:
        print("There is an error with the SQL")
    except db.OperationalError:
        print("There was an issue with the DB")
    except:
        print("Something went wrong")
    dbi.disconnect_db(conn, cursor)
    return success, id


