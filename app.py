
from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
from cs50 import SQL
from decouple import config


# Configure SQLite database and Flask application
db = SQL("sqlite:///jb.db")
app = Flask(__name__)

# Ensure that templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

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
        return render_template("index.html")

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
        msg = Message('Enquiry', sender='jjdttesting@gmail.com', recipients=['jmventer.befocused@gmail.com'], reply_to=email)
        msg.body = ('From: ' + name + ' ' + surname + '\n\n' + query)
        mail.send(msg)

        # Write the entry into the database
        db.execute('INSERT INTO jb (name, surname, email, query, timestamp) VALUES (?,?,?,?,?)', name, surname, email, query, timestamp)
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)