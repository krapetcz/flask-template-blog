
# Flask Template Blog

This is a simple blog application built with Flask. It allows user registration, login, article creation with image upload, and user management via a web interface. It is designed as a learning project or as a boilerplate for small Flask-based content platforms.

## Features

- User registration and authentication
- Secure password hashing using Werkzeug
- Admin dashboard for creating, editing, and deleting articles
- Image upload support for articles
- User management (create, edit, delete users)
- Flash messaging for user feedback
- Basic error handling (custom 404 page)
- Uses SQLite as the database
- Structured code: models, templates, configuration, CLI

## Technologies Used

- Python 3
- Flask
- Flask-Login
- SQLAlchemy
- SQLite
- HTML/CSS
- Jinja2
- Dotenv

## Installation

1. Clone the repository:

```bash
git clone https://github.com/krapetcz/flask-template-blog.git
cd flask-template-blog
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables (optional):

Create a `.env` file in the root directory:

```
SECRET_KEY=your_secret_key
```

If omitted, a fallback secret key will be used.

5. Run the app:

```bash
flask run
```

The app will be available at `http://localhost:5000`.

## CLI User Creation

You can create users via command line:

```bash
flask create-user <username> <password>
```

## Folder Structure

```
.
├── static/
│   └── style.css
│   └── uploads/
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── dashboard.html
│   ├── article.html
│   ├── create_article.html
│   ├── user_form.html
│   ├── user_management.html
│   └── 404.html
├── models.py
├── config.py
├── app.py
└── .gitignore
```

## License

This project is provided for educational and personal use. No warranty or liability is implied.
