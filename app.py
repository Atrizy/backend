import tweets as tw
import signup as su
import follow as fol
import comments as cm
from flask import Flask, request, Response
import json
import dbinteractions as db
import sys

app = Flask(__name__)

@app.post("/api/comments")
def insert_comment():
    try:
        login_token = request.json['login_token']
        content = request.json['content']
        success, id = cm.insert_comment(login_token, content)
        if(success):
            comment_json = json.dumps({
                "login_token":login_token,
                "content": content,
                "id": id
            }, default=str)
            return Response(comment_json, mimetype="application/json", status=201)
        else:
            return Response("Invalid comment format", mimetype="plain/text", status=400)
    except KeyError:
        return Response("Invalid username or content", mimetype="plain/text", status=422)
    except:
        return Response("Please try again later", mimetype="plain/text", status=501)


@app.post("/api/follows")
def follow_user():
    try:
        login_token = request.json['login_token']
        follow_id = request.json['follow_id']
        success = fol.follow_user(follow_id, login_token)
        if(success):
            return Response(status=204)
        else:
            return Response("Please try again", mimetype="plain/text", status=400)
    except:
        return Response("Something went horribly wrong please call someone", mimetype="plain/text", status=500)

@app.post("/api/post")
def insert_post():
    try:
        login_token = request.json['login_token']
        content = request.json['content']
        success, id = tw.insert_post(login_token, content)
        if(success):
            post_json = json.dumps({
                "login_token":login_token,
                "content": content,
                "id": id
            }, default=str)
            return Response(post_json, mimetype="application/json", status=201)
        else:
            return Response("Invalid tweet", mimetype="plain/text", status=400)
    except KeyError:
        return Response("Invalid username or content", mimetype="plain/text", status=422)
    except:
        return Response("Please try again later", mimetype="plain/text", status=501)

@app.post("/api/users")
def create_user():
    try:
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']
        bio = request.json['bio']
        dob = request.json['dob']
        pfp = request.json.get('pfp')
        profile_banner = request.json.get("profile_banner")
        success, id, login_token = su.signup(email, username, password, bio, dob, pfp, profile_banner)
        if(success):
            user_json = json.dumps({
                "user_id": id,
                "email": email,
                "username": username,
                "bio": bio,
                "dob": dob,
                "pfp": pfp,
                "profile_banner": profile_banner,
                "login_token": login_token
            })
            return Response(user_json, mimetype="application/json", status=200)
        else:
            return Response("Please try again", mimetype="plain/text", status=400)
    except:
        return Response("Something went horribly wrong please call someone", mimetype="plain/text", status=500)


@app.get("/api/post")
def get_blog_post():
    try:
        success, post = tw.get_all_posts()
        if(success):
            posts_json = json.dumps(post, default=str)
            return Response(posts_json, mimetype="application/json", status=200)
        else:
            return Response("Please try again", mimetype="plain/text", status=400)
    except:
        return Response("Sorry Please try again", mimetype="plain/text", status=500)


if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("You must pass a mode to run this python script, either 'testing' or 'production'")
    exit()

if(mode == "testing"):
    print("Running in testing mode")
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
elif(mode =="production"):
    print("Running in production mode")
    import bjoern # type: ignore
    bjoern.run(app, "0.0.0.0", 5000)
else:
    print("Please run with either testing or production. Example: ")
    print("python app.py production")