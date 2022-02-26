import mariadb as db
import dbinteractions as dbi

def insert_post(content, user_id):
    success = False
    id = None
    conn, cursor = dbi.connect_db()
    try:
        cursor.execute("INSERT INTO tweet(content, user_id) VALUES(?,?)", [content, user_id])
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


def get_all_posts():
    success = False
    posts = []
    conn, cursor = dbi.connect_db()
    try:
        cursor.execute(
            "select users.username, tweet.content, tweet.created_at, tweet.id from users inner join tweet on users.id = tweet.user_id")
        posts = cursor.fetchall()
        success = True
    except db.ProgrammingError:
        print("There is an error with the SQL")
    except db.OperationalError:
        print("There was an issue with the DB")
    except:
        print("Something went wrong")
    dbi.disconnect_db(conn, cursor)
    return success, posts