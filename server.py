"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/register')
# displays a form that asks for username and password
def register():
    """Display registration form"""

    return render_template("registration.html")


@app.route('/verify-register', methods=["POST"])
def verify_register():
    """Checks if username exists; 
    if not, creates new user in the database."""

    username = request.form.get("username")
    password = request.form.get("password")

    #username is user object
    user_object = User.query.filter_by(email=username).first()

    # if the user doesn't exist, add to db
    if user_object == None:
        new_user = User(email=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("Thanks for registering!")

    else:
        flash("You're already registered!")

    return redirect('/login')
    

@app.route('/login')
def login():
    """Dispay login form"""

    return render_template("login.html")

@app.route('/verify-login', methods=["POST"])
def verify_login():

    username = request.form.get("username")
    password = request.form.get("password")

    user_object = User.query.filter_by(email=username).first()

    #if username exists in database
    if user_object:

        #if given password matches database password for username
        if password == user_object.password:

            # adding to session {"user_id":the actual user id}
            session["user_id"] = user_object.user_id
            print session

            # Add Flash message: "Logged in" on base.html
            flash("Thanks for logging in!")

            #redirect to homepage
            return redirect('/')

        #if password doesn't match
        else:
            flash("Incorrect password. Please try again.")

            #message password is incorrect
            return redirect('/login')

    else:
        flash("You're not registered. Please register here")

        #redirect to registration page
        return redirect('/register')


@app.route('/logout')
def logout():

    del session['user_id']
    print session

    flash("You've been logged out.")
    return redirect('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
