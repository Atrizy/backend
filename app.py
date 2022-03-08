from sre_constants import SUCCESS
import tweets as tw
import signup as su
import login as log
import follow as fol
import comments as cm
import likes as lk
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

@app.post("/api/user_login")
def login():
    try:
        email = request.json['email']
        password = request.json['password']
        success, id, login_token = log.login_user(email, password)
        if(success):
            user_json = json.dumps({
                "user_id": id,
                "email": email,
                "password": password,
                "login_token": login_token
            })
            return Response(user_json, mimetype="application/json", status=200)
        else:
            return Response("Please try again", mimetype="plain/text", status=400)
    except:
        return Response("Something went horribly wrong please call someone", mimetype="plain/text", status=500)

@app.get("/api/comment_likes")
def get_comments_likes():
    try:
        comment_id = request.args["comment_id"]
        success, post = lk.get_comment_like(comment_id)
        if(success):
            comment_likes_json = json.dumps(post, default=str)
            return Response(comment_likes_json, mimetype="application/json", status=200)
        else:
            return Response("Please try again", mimetype="plain/text", status=400)
    except:
        return Response("Sorry Please try again", mimetype="plain/text", status=500)

@app.get("/api/tweet_likes")
def get_tweet_likes():
    try:
        tweet_id = request.args["tweet_id"]
        success, post = lk.get_tweet_like(tweet_id)
        if(success):
            tweet_likes_json = json.dumps(post, default=str)
            return Response(tweet_likes_json, mimetype="application/json", status=200)
        else:
            return Response("Please try again", mimetype="plain/text", status=400)
    except:
        return Response("Sorry Please try again", mimetype="plain/text", status=500)

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

@app.patch("/api/users")
def patch_user_profile():
    try:
        email = request.json['email']
        username = request.json['username']
        bio = request.json['bio']
        dob = request.json['dob']
        pfp = request.json.get('pfp')
        profile_banner = request.json.get("profile_banner")
        login_token = request.json["login_token"]
        success = su.patch_user_info(login_token, email, username, bio, dob, pfp, profile_banner)
        if(success):
            return Response(mimetype="application/json", status=200)
        else:
            return Response("Please try again", mimetype="plain/text", status=400)
    except:
        return Response("Sorry Please try again", mimetype="plain/text", status=500)

@app.patch("/api/post")
def patch_tweet_information():
    try:
        id = request.json["id"]
        content = request.json["content"]
        login_token = request.json["login_token"]
        success = tw.patch_tweet_info(login_token, content, id)
        if(success):
            return Response(mimetype="application/json", status=200)
        else:
            return Response("Please try again", mimetype="plain/text", status=400)
    except:
        return Response("Sorry Please try again", mimetype="plain/text", status=500)

@app.patch("/api/comments")
def patch_comment_information():
    try:
        id = request.json["id"]
        content = request.json["content"]
        login_token = request.json["login_token"]
        success = cm.patch_comment_info(login_token, content, id)
        if(success):
            return Response(mimetype="application/json", status=200)
        else:
            return Response("Please try again", mimetype="plain/text", status=400)
    except:
        return Response("Sorry Please try again", mimetype="plain/text", status=500)

@app.delete("/api/follows")
def delete_follow():
    try:
        login_token = request.json["login_token"]
        unfollowed_user = request.json["followed_user_id"]
        success = fol.unfollow_user(login_token, unfollowed_user)
        if(success):
            return Response(mimetype="application/json", status=200)
        else:
            return Response("Please try again", mimetype="plain/text", status=400)
    except:
        return Response("Sorry Please try again", mimetype="plain/text", status=500)

@app.delete("/api/post")
def delete_tweet():
    try:
        login_token = request.json["login_token"]
        id = request.json["id"]
        success = tw.delete_tweet(login_token, id)
        if(success):
            return Response(mimetype="application/json", status=200)
        else:
            return Response("Please try again", mimetype="plain/text", status=400)
    except:
        return Response("Sorry Please try again", mimetype="plain/text", status=500)

@app.delete("/api/comments")
def delete_comment():
    try:
        login_token = request.json["login_token"]
        id = request.json["id"]
        success = cm.delete_comment(login_token, id)
        if(success):
            return Response(mimetype="application/json", status=200)
        else:
            return Response("Please try again", mimetype="plain/text", status=400)
    except:
        return Response("Sorry Please try again", mimetype="plain/text", status=500)

@app.delete("/api/tweet_likes")
def delete_tweet_like():
    try:
        login_token = request.json["login_token"]
        id = request.json["id"]
        tweet_id = request.json["tweet_id"]
        success = lk.delete_tweet_like(login_token, id, tweet_id)
        if(success):
            return Response(mimetype="application/json", status=200)
        else:
            return Response("Please try again", mimetype="plain/text", status=400)
    except:
        return Response("Sorry Please try again", mimetype="plain/text", status=500)

@app.delete("/api/comment_likes")
def delete_comment_like():
    try:
        login_token = request.json["login_token"]
        id = request.json["id"]
        comment_id = request.json["comment_id"]
        success = lk.delete_comment_like(login_token, id, comment_id)
        if(success):
            return Response(mimetype="application/json", status=200)
        else:
            return Response("Please try again", mimetype="plain/text", status=400)
    except:
        return Response("Sorry Please try again", mimetype="plain/text", status=500)

@app.delete("/api/users")
def delete_user():
    try:
        login_token = request.json["login_token"]
        success = log.delete_user(login_token)
        if(success):
            return Response(mimetype="application/json", status=200)
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