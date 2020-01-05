from flask import Flask, render_template, request, redirect, flash, session
from config import db
from models import User, Idea
from sqlalchemy.sql import func, desc
from config import EMAIL_REGEX, password_reg, bcrypt


def index():
    admin = User.query.filter_by(admin_status = 1).all()
    if not admin:
        print("admin created")
        admin_pw_hash = bcrypt.generate_password_hash("admin")
        User.create_admin(admin_pw_hash)
    return render_template("login_registration.html")

def new_acc():
    is_valid = True
    name_err = 0
    if not request.form['fname'].isalpha() or not len(request.form['fname']) >= 2:
        is_valid = False
        name_err = 1
        flash("Names can contain only letters and be at least two characters", "registration")
    if not request.form['lname'].isalpha() or not len(request.form['lname']) >= 2:
        is_valid = False
        if name_err == 1:
            flash("Names can contain only letters and be at least two characters", "registration")
    if not password_reg.match(request.form["pass"]):
        is_valid = False
        flash("Password should be at least 5 characters, have one number, one uppercase and one lowercase letter, and one symbol", "registration")
    if not EMAIL_REGEX.match(request.form["email"]):
        is_valid = False
        flash("Invalid Email Address", "registration")
    if request.form["pass"] != request.form["confirmpass"]:
        is_valid = False
        flash("Passwords do not match", "registration")
    if is_valid:
        pw_hash = bcrypt.generate_password_hash(request.form["pass"])
        new_user = User(
                f_name= request.form["fname"],
                l_name= request.form["lname"],
                email = request.form["email"],
                admin_status = 0,
                password = pw_hash)
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = {
                "first": new_user.f_name,
                "last": new_user.l_name,
                "email":new_user.email,
                "id": new_user.user_id}
        print(session["user_id"])
        print("Account creation successful!")
        return redirect("/userpage")
    return redirect("/")

def reg_fname():
    is_valid = True
    if not request.form['fname'].isalpha() or not len(request.form['fname']) >= 2:
        is_valid = False
    return render_template("partials/reg_error.html", fname_val=is_valid)

def reg_lname():
    is_valid = True
    if not request.form['lname'].isalpha() or not len(request.form['lname']) >= 2:
        is_valid = False
    return render_template("partials/reg_error.html", lname_val=is_valid)    

def reg_email_check():
    email_format = True
    if not EMAIL_REGEX.match(request.form["email"]):
        email_format = False
        return render_template("partials/reg_error.html", email_format=email_format)
    email_exists = False
    user = User.query.filter_by(email=request.form["email"]).all()
    if user:
        email_exists = True
        return render_template("partials/reg_error.html", email_exists = email_exists)
    if email_format == True and email_exists == False:
        return render_template("partials/reg_error.html", email_exists = email_exists)# email_format=email_format, 

def reg_pw():
    pw_check = True
    if not password_reg.match(request.form["pass"]):
        pw_check = False
    return render_template("partials/reg_error.html", pw_check=pw_check)

def reg_pw_match():
    pw_match = False
    if request.form["pass"] == request.form["confirmpass"]:
        pw_match = True
    return render_template("partials/reg_error.html", pw_match = pw_match)

def login():
    user = User.query.filter_by(email=request.form["email"]).all()
    if user:
        hashed_pw = user[0].password
        if bcrypt.check_password_hash(hashed_pw, request.form['pass']):
            session["user_id"] = {
                "first": user[0].f_name,
                "last": user[0].l_name,
                "email":user[0].email,
                "id": user[0].user_id}
            print("Login Sucessful")
            print(session["user_id"])
            return redirect("/userpage")
        else:
            flash("Invalid Password", "login")
            return redirect("/")
    else:
        flash("Email not in Database", "login")
        return redirect("/")

def logout():
    session.clear()
    return redirect("/")

def userprofile(user_id):
    if "user_id" not in session:
        return redirect("/logout")
    view_user = User.query.get(user_id)
    current_user = User.query.get(session["user_id"]["id"])
    return render_template ("profile.html", user=view_user, cur_user = current_user)

def editprofile():
    id = request.form["user_id"]
    if int(id) != session["user_id"]["id"]:
        return redirect ("/logout")
    user = User.query.get(id)
    # if request.form["email"] != session["user_id"]["email"]:
    #     if not EMAIL_REGEX.match(request.form["email"]):
    #         flash("Invalid Email Address", "update_profile")
    #     else:
    #         user.email = request.form["email"]
    #         print("email changed")
    #         session["user_id"] = {
    #             "first": user.f_name,
    #             "last": user.l_name,
    #             "email":request.form["email"],
    #             "id": user.user_id}
    #         flash("Email Updated", "update_profile")
    if request.form["profile"] and request.form["profile"] != user.profile:
        if len(request.form["profile"]) > 1600:
            flash("Profile must be less than 1600 characters", "update_profile")
        if request.form["profile"] == " ":
            user.profile = None
        else:
            user.profile = request.form["profile"]
            print("profile changed")
            flash("Profile Updated", "update_profile")
    db.session.commit()
    return redirect(f"/userprofile/{id}")

def editpassword():
    id = request.form["user_id"]
    if int(id) != session["user_id"]["id"]:
        return redirect ("/logout")
    user = User.query.get(id)
    hashed_pw = user.password
    if bcrypt.check_password_hash(hashed_pw, request.form['current_pass']):
        if not password_reg.match(request.form["new_pass"]):
            flash("Password should be at least 5 characters, have one number, one uppercase and one lowercase letter, and one symbol", "update_pass")
        if request.form["new_pass"] != request.form["confirm_pass"]:
            flash("Passwords do not match", "update_pass")
        else:
            new_pw_hash = bcrypt.generate_password_hash(request.form["new_pass"])
            user.password = new_pw_hash
            db.session.commit()
            flash("Password changed!", "update_pass")
    else:
        flash("Incorrect Password", "update_pass")
    return redirect(f"/userprofile/{id}")

def userpage():
    if "user_id" not in session:
        return redirect("/")
    user_data = User.query.filter_by(user_id = session["user_id"]["id"]).all()
    idea_data = Idea.query.order_by(desc(Idea.created_at)).join(User).all()

    return render_template("userpage.html", user_data = user_data[0], idea_data= idea_data)

    # # for feed
    # mysql = connectToMySQL("tweets")
    # query = "SELECT following FROM followers where follower = %(user_id)s"
    # data = {"user_id": session["user_id"]}

    # feed_tweets = []
    # ids_following = mysql.query_db(query, data)
    # for tweet in tweets:
    #     if tweet['author'] in [following["following"] for following in ids_following]:
    #         feed_tweets.append(tweet)

    # # for displaying total like count
    # mysql = connectToMySQL("tweets")
    # query = "SELECT tweet_like, COUNT(tweet_like) as like_count FROM user_likes GROUP BY tweet_like"
    # like_count = mysql.query_db(query)

    # for the timestamps
    # td = 0 to prevent errors when no tweets in database and no td to return
    # td =0
    # default func.now() using UTC time zone and not converting. It's bad.
    # for tweet in tweet_data:
    #     td = datetime_cur - tweet.created_at
    #     print(datetime.now())
    #     print(tweet.created_at)
    #     if td.days > 0:
    #         tweet["time_since_days"] = td.days
    #     else:
    #         if td.seconds == 0:
    #             tweet["time_now"] = 1
    #         if td.seconds < 60:
    #             tweet["time_since_seconds"] = td.seconds
    #         if td.seconds <= 3599:
    #             tweet["time_since_minutes"] = round(td.seconds / 60)
            # if td.seconds > 3599:
            #     tweet["time_since_hours"] = round (td.seconds / 3600)

def create_idea():
    if "user_id" not in session:
        return redirect("/")
    is_valid = True
    if not request.form["idea_content"]:
        is_valid = False
        flash("You cannot post an empty idea.")
    if len(request.form["idea_content"]) > 255:
        flash("Ideas must be less than 255 characters.")
        is_valid = False
    
    if is_valid:
        new_idea = Idea(
                    content=request.form["idea_content"],
                    author_id = session["user_id"]["id"])
        db.session.add(new_idea)
        db.session.commit()
        flash("Idea saved!")
        user_data = User.query.filter_by(user_id = session["user_id"]["id"]).all()
        idea_data = Idea.query.order_by(desc(Idea.created_at)).join(User).all()
        return render_template("/partials/idea_feed.html", user_data = user_data[0], idea_data= idea_data)

def delete_idea(idea_id):
    if "user_id" not in session:
        return redirect("/")
    delete_idea = Idea.query.get(idea_id)
    print(delete_idea.content)
    if delete_idea.author.user_id == session["user_id"]["id"]:
        delete_idea.author.user_ideas.remove(delete_idea)
        db.session.commit()
    clean_empty = Idea.query.filter_by(author_id=None).all()
    for clean in clean_empty:
        db.session.delete(clean)
        db.session.commit()
    user_data = User.query.filter_by(user_id = session["user_id"]["id"]).all()
    idea_data = Idea.query.order_by(desc(Idea.created_at)).join(User).all()
    return render_template("partials/idea_feed.html", user_data = user_data[0], idea_data= idea_data)
    # return redirect("/userpage")

def edit_page(idea_id):
    if "user_id" not in session:
        return redirect("/")
    idea_content = Idea.query.get(idea_id)
    if not idea_content.author_id == session["user_id"]["id"]:
        return redirect("/userpage")
    return render_template("/edit.html", idea_content= idea_content)

def edit_idea(idea_id):
    idea_content = Idea.query.get(idea_id)
    updated_idea = request.form["idea_edit"]
    is_valid = True
    if not updated_idea:
        is_valid = False
        flash("You cannot post an empty idea.")
    if len(updated_idea) > 255:
        flash("Ideas must be less than 255 characters.")
        is_valid = False
    if updated_idea == idea_content.content:
        is_valid = False
        flash("You didn't edit your idea! Hit 'GO Back' if you changed your mind")
    if is_valid:
        idea_content.content = updated_idea
        db.session.commit()
        flash("Idea Updated!")
    return redirect("/edit_idea/{}".format(idea_id))

def like(idea_id):
    if "user_id" not in session:
        return redirect("/")    
    liked_idea = Idea.query.get(idea_id)
    current_user = User.query.get(session["user_id"]["id"])
    current_user.liked_idea.append(liked_idea)
    user_data = User.query.filter_by(user_id = session["user_id"]["id"]).all()
    idea_data = Idea.query.order_by(desc(Idea.created_at)).join(User).all()
    db.session.commit()
    return render_template("partials/idea_feed.html", user_data = user_data[0], idea_data= idea_data)

def unlike(idea_id):
    if "user_id" not in session:
        return redirect("/") 
    liked_idea = Idea.query.get(idea_id)
    current_user = User.query.get(session["user_id"]["id"])
    current_user.liked_idea.remove(liked_idea)    
    user_data = User.query.filter_by(user_id = session["user_id"]["id"]).all()
    idea_data = Idea.query.order_by(desc(Idea.created_at)).join(User).all()
    db.session.commit()
    return render_template("partials/idea_feed.html", user_data = user_data[0], idea_data= idea_data)

def details(idea_id):
    idea_data = Idea.query.get(idea_id)
    return render_template("details.html", idea = idea_data)

def users():
    if "user_id" not in session:
        return redirect("/")
    current_user = User.query.get(session["user_id"]["id"])
    user_list = User.query.all()

    return render_template("users.html", user_list = user_list, current_user=current_user)

def add_friend(user_id):
    current_user = User.query.get(session["user_id"]["id"])
    friend_request = User.query.get(user_id)
    friend_request.friends.append(current_user)
    db.session.commit()
    return redirect("/users")

def remove_friend(user_id):
    if "user_id" not in session:
        return redirect("/")
    current_user = User.query.get(session["user_id"]["id"])
    friend_to_remove = User.query.get(user_id)
    friend_to_remove.friends.remove(current_user)
    current_user.friends.remove(friend_to_remove)
    db.session.commit()
    return redirect("/users")

def refresh_feed():
    user_data = User.query.filter_by(user_id = session["user_id"]["id"]).all()
    idea_data = Idea.query.order_by(desc(Idea.created_at)).join(User).all()
    return render_template("partials/idea_feed.html", user_data = user_data[0], idea_data= idea_data)