
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from cs50 import SQL
# To configure email server parameters
from decouple import config
from datetime import datetime
import os

project_root = os.path.dirname(os.path.realpath('__file__'))
template_path = os.path.join(project_root, 'app/templates')
static_path = os.path.join(project_root, 'app/static')
app = Flask(__name__, template_folder=template_path, static_folder=static_path)

Application = app

# Configure SQLite database and Flask application
db = SQL("sqlite:///jb.db")
app = Flask(__name__)

# Ensure that templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure SQLAlchemy for Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/jacquesdutoit/Desktop/joybrews/joybrews/blog.db'
dbalc = SQLAlchemy(app)

# Configure a database model for the blogposts to be saved into
class Blogpost(dbalc.Model):
    id = dbalc.Column(dbalc.Integer, primary_key=True)
    title = dbalc.Column(dbalc.String(50))
    subtitle = dbalc.Column(dbalc.String(50))
    author = dbalc.Column(dbalc.String(20))
    date_posted = dbalc.Column(dbalc.DateTime)
    content = dbalc.Column(dbalc.Text)

# Configure email server parameters
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']='465'
app.config['MAIL_USERNAME']=config('MAIL_ADDRESS')
app.config['MAIL_PASSWORD']=config('MAIL_PASSWORD')
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

# Create an instance of the Mail class
mail = Mail(app)

# Get the data from the form fields and write it to the db
@app.route("/", methods=["GET", "POST"])
def getform():
    # If the user reaches this route via GET then just render_remplate index
    if request.method == "GET":
        latest = Blogpost.query.order_by(Blogpost.id.desc()).first()

        return render_template("index.html", latest=latest)

    # If the user completes the contact form and submits, then record it in the database and send an email to Joybrews
    if request.method == "POST":
        # Retrieve the info from the form
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        query = request.form.get('textarea')
        
        # Get the current date
        timestamp = db.execute("SELECT datetime()")
        timestamp = timestamp[0]["datetime()"]

        # Mail the contact form information
        msg = Message('Enquiry', sender='jjdttesting@gmail.com', recipients=['jjdttesting@gmail.com'], reply_to=email)
        msg.body = ('From: ' + name + ' ' + surname + '\n\n' + query)
        mail.send(msg)

        # Write the entry into the database
        db.execute('INSERT INTO jb (name, surname, email, query, timestamp) VALUES (?,?,?,?,?)', name, surname, email, query, timestamp)
        return redirect("/")


# Creating the route for COFFEEMOMENTS
@app.route("/coffeemoments")
def coffeemoments():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template("coffeemoments.html", posts=posts)

# Creating the route for POST
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()

    return render_template("post.html", post=post)

# Create an 'invisible' link ADDPOST, to write and add blogs for the website
@app.route("/addpost", methods=["GET", "POST"])
def addpost():
    # If request method is GET then just dispay the page
    if request.method == "GET":
        return render_template("addpost.html")
    
    # If request method is POST then save the blogpost to the database and display on the site
    if request.method == "POST":
        if request.form.get('submit1', None) == 'watch':
            content = request.form['content']
            return render_template("preview.html", content=content)

        elif request.form.get('submit1', None) == 'commit':
            title = request.form['title']
            subtitle = request.form['subtitle']
            author = request.form['author']
            content = request.form['content']

            post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())

            dbalc.session.add(post)
            dbalc.session.commit()

            return redirect(url_for('coffeemoments'))

if __name__ == "__main__":
    app.run(debug=True)