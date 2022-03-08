import mariadb as db
import dbinteractions as dbi
import hashlib
import secrets

def create_salt():
    return secrets.token_urlsafe(10)

def create_login_token():
    return secrets.token_urlsafe(70)

def signup(email, username, password, bio, dob, pfp, profile_banner):
    success = False
    id = None
    conn, cursor = dbi.connect_db()
    salt = create_salt()
    login_token = create_login_token()    
    password = salt + password
    password = hashlib.sha512(password.encode()).hexdigest()
    try:
        cursor.execute("INSERT INTO user(email, username, password, bio, dob, pfp, profile_banner, salt) VALUES(?,?,?,?,?,?,?,?)", [email, username, password, bio, dob, pfp, profile_banner, salt])
        conn.commit()
        if(cursor.rowcount == 1):
            id = cursor.lastrowid
            cursor.execute("INSERT INTO user_session(user_id, login_token) VALUES(?,?)", [id, login_token])
            conn.commit()
            success = True
    except db.ProgrammingError:
        print("There is an error with the SQL")
    except db.OperationalError:
        print("There was an issue with the DB")
    except:
        print("Something went wrong")
    dbi.disconnect_db(conn, cursor)
    return success, id, login_token

def patch_user_info(login_token, email, username, bio, dob, pfp, profile_banner):
    success = False
    conn, cursor = dbi.connect_db()
    cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [login_token])
    user = cursor.fetchone()
    try:
        cursor.execute("SELECT user_id FROM user_session WHERE login_token=?", [login_token])
        user = cursor.fetchone()
        cursor.execute("UPDATE users SET email=? WHERE id=?", [email, user[0]])
        cursor.execute("UPDATE users SET username=? WHERE id=?", [username, user[0]])
        cursor.execute("UPDATE users SET bio=? WHERE id=?", [bio, user[0]])
        cursor.execute("UPDATE users SET dob=? WHERE id=?", [dob, user[0]])
        if(pfp != None ):
            cursor.execute("UPDATE users SET pfp=? WHERE id=?", [pfp, user[0]])
        if(profile_banner != None):
            cursor.execute("UPDATE users SET profile_banner=? WHERE id=?", [profile_banner, user[0]])
        conn.commit()
        success = True       
    except db.ProgrammingError:
        print("There is an error with the SQL")
    except db.OperationalError:
        print("There was an issue with the DB")
    except:
        print("Something went wrong")
    dbi.disconnect_db(conn, cursor)
    return success  

