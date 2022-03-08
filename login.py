import mariadb as db
import dbinteractions as dbi
import secrets
import hashlib

def create_login_token():
    return secrets.token_urlsafe(70)

def login_user(email, password):
    success = False
    id = None
    conn, cursor = dbi.connect_db()
    cursor.execute("SELECT salt FROM users WHERE email=?", [email])
    salt = cursor.fetchone()
    login_token = create_login_token()
    password = salt[0] + password
    password = hashlib.sha512(password.encode()).hexdigest()
    cursor.execute("SELECT id, email, username, bio, dob, pfp, profile_banner FROM users WHERE email=? AND password=?" [email, password])
    user = cursor.fetchone()
    try:
        if(cursor.rowcount == 1):
            cursor.execute("INSERT INTO user_session(user_id, login_token) VALUES(?,?)", [user[0], login_token])
            success = True
            id = cursor.lastrowid
    except db.ProgrammingError:
        print("There is an error with the SQL")
    except db.OperationalError:
        print("There was an issue with the DB")
    except:
        print("Something went wrong")
    dbi.disconnect_db(conn, cursor)
    return success, id, user, login_token, email

def delete_user(login_token):
    success = False
    conn, cursor = dbi.connect_db()
    try:
        cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [login_token])
        user = cursor.fetchone()
        cursor.execute("DELETE FROM users WHERE id=?", [user[0]] )
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