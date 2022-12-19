from flask import redirect, url_for, render_template, flash, request
from main.models import User, Post, Comment,Like
from main import app, db
from PIL import Image
from main.form import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, SearchForm 
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
bcrypt = Bcrypt(app)

app.jinja_env.globals.update(clever_function=SearchForm)

@app.route("/")
@app.route("/home")

def home():

    posts= Post.query.all()

    return render_template("home.html",posts=posts)




@app.route("/register", methods=["POST","GET"])

def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
        
        

    return render_template("register.html",form = form ) 



@app.route("/login", methods= ["POST","GET"])

def login():
    form= LoginForm()
    user = User.query.filter_by(username=form.username.data).first()

    if user and user.password == form.password.data: 
        login_user(user)
        return redirect(url_for("home"))

    

    return render_template("login.html",form=form)


@app.route("/post",methods=["POST","GET"])

def post():
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            hex = secrets.token_hex(8)
            test, f_ext = os.path.splitext(form.picture.data.filename)
            picture_fn = hex+f_ext
            picture_path = os.path.join(app.root_path,"static/assets",picture_fn)
            pic = Image.open(form.picture.data)
            pic.save(picture_path)

            post = Post(title=form.title.data,content=form.content.data,author=current_user,img=picture_fn,priv=form.priv.data)
            db.session.add(post)
            db.session.commit()

            return redirect(url_for("home"))

    return render_template("post.html",form=form)

