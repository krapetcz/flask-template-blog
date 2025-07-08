from flask import Flask, render_template, redirect, url_for, request, flash
from flask import session
from config import Config
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from datetime import datetime
from werkzeug.utils import secure_filename
from models import db, User, Article, Image
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import uuid
import click

import sys

# App initialization
app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
db.init_app(app)
load_dotenv()

# Flask login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "You must be logged in to access this page."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# home screen
@app.route("/", endpoint="home")
def home():
    """
    Render the homepage with a list of all articles, sorted by creation date (newest first).
    """
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template("home.html", articles=articles)

@app.route("/article/<int:article_id>")
def article(article_id):
    """
    Display a specific article by its ID. If not found, return a 404 error.
    """
    article = Article.query.get_or_404(article_id)
    return render_template("article.html", article=article)

#login
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Render the login page and handle login form submission.
    On successful login, redirect to the user dashboard.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid login data.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    """
    Log out the current user and redirect to the login page.
    """
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    """
    Display the current user's dashboard with a list of their own articles.
    User must be logged in to access this page.
    """
    articles = Article.query.filter_by(user_id=current_user.id).order_by(Article.created_at.desc()).all()
    return render_template("dashboard.html", articles=articles)

@app.route("/article/new", methods=["GET", "POST"])
@login_required
def create_article():
    """
    Render the article creation form and handle new article submissions.
    If an image is provided, it is saved and linked to the article.
    """
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        image_file = request.files.get("image")

        if image_file and image_file.filename != "":
            print("Image will be saved:", image_file.filename)
        else:
            print("No image selected.")

        article = Article(title=title, content=content, author=current_user)

        db.session.add(article)
        db.session.commit()

        if image_file and image_file.filename != "":
            original_name = secure_filename(image_file.filename)
            unique_prefix = uuid.uuid4().hex
            filename = f"{unique_prefix}_{original_name}"

            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)

            image = Image(filename=f"uploads/{filename}", article_id=article.id)
            db.session.add(image)
            db.session.commit()

        flash("Article has been published.", "success")
        return redirect(url_for("dashboard"))

    return render_template("create_article.html", article=None)

@app.route("/article/<int:article_id>/edit", methods=["GET", "POST"])
@login_required
def edit_article(article_id):
    """
    Render the article editing form and handle updates to the article and its image.
    Only the article's author can edit it.
    """
    article = Article.query.get_or_404(article_id)
    if article.author != current_user:
        flash("You are not authorized.", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        article.title = request.form["title"]
        article.content = request.form["content"]
        image_file = request.files.get("image")
        if image_file and image_file.filename != "":
            original_name = secure_filename(image_file.filename)
            unique_prefix = uuid.uuid4().hex
            filename = f"{unique_prefix}_{original_name}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)

            image = Image(filename=f"uploads/{filename}", article_id=article.id)
            db.session.add(image)
        db.session.commit()
        flash("Article has been changed.", "success")
        return redirect(url_for("dashboard"))

    return render_template("create_article.html", article=article)

@app.route("/article/<int:article_id>/delete", methods=["GET", "POST"])
@login_required
def delete_article(article_id):
    """
    Delete the specified article if the current user is the author.
    Redirect back to the dashboard.
    """
    article = Article.query.get_or_404(article_id)
    if article.author != current_user:
        flash("You are not authorized.", "danger")
        return redirect(url_for("dashboard"))

    db.session.delete(article)
    db.session.commit()
    flash("Article has been deleted.", "info")
    return redirect(url_for("dashboard"))

@app.route('/user_management')
@login_required
def user_management():
    """
    Display the user management panel with a list of all registered users.
    Only accessible to logged-in users.
    """
    print("User administration access granted.")
    users = User.query.all()
    return render_template('user_management.html', users=users)


@app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    """
    Render the form to create a new user and handle user registration.
    Checks for duplicate usernames before creating a new account.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('create_user'))

        # hash password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("User has been created!", "success")
        return redirect(url_for('user_management'))

    return render_template('user_form.html')

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """
    Render the form to edit an existing user's credentials.
    Prevents changing to a duplicate username.
    """
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        new_username = request.form.get('username')
        new_password = request.form.get('password')

        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user and existing_user.id != user.id:
            flash('This username is already taken.', 'danger')
            return redirect(url_for('edit_user', user_id=user.id))

        user.username = new_username
        if new_password:
            user.password = generate_password_hash(new_password, method='pbkdf2:sha256')

        db.session.commit()
        flash('User has been updated.', 'success')
        return redirect(url_for('user_management'))

    return render_template('user_form.html', user=user)

@app.route("/delete_user/<int:user_id>", methods=["GET", "POST"])
@login_required
def delete_user(user_id):
    """
    Delete the specified user account.
    Prevents users from deleting their own account.
    """
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("You cannot delete yourself.", "danger")
        return redirect(url_for("user_management"))

    db.session.delete(user)
    db.session.commit()
    flash("User has been deleted.", "info")
    return redirect(url_for("user_management"))


@app.errorhandler(404)
def page_not_found(e):
    """
    Custom 404 error handler that renders a friendly error page.
    """
    return render_template("404.html"), 404

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)


@app.cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user(username, password):
    """
    Command-line utility to create a new user from the terminal.
    Usage: flask create-user USERNAME PASSWORD
    """
    from werkzeug.security import generate_password_hash

    if User.query.filter_by(username=username).first():
        print(f"User '{username}' already exists.")
        return

    user = User(username=username, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    print(f"User '{username}' has been created.")
