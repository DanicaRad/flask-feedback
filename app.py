from crypt import methods
from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import AddUserForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Winnie"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension

connect_db(app)

@app.route('/')
def redirect_home_to_register():
    """redirects home route to register route"""

    return redirect('/register')

@app.route('/register', methods=['POST', 'GET'])
def show_register_form():
    """Shows form to register"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        email = form.email.data
        f_name = form.first_name.data
        l_name = form.last_name.data

        user = User.register(username, pwd, email, f_name, l_name)
        db.session.add(user)
        db.session.commit()

        session['username'] = user.username

        return redirect(f'/users/{user.username}')

    return render_template('users/form.html', form=form, action="register")

@app.route('/login', methods=['GET', 'POST'])
def show_login_form():
    """Show and handle login form"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            session["username"] = user.username
            return redirect(f'/users/{user.username}')

        elif User.query.get(form.username.data):
            form.password.errors = ["Invalid password."]
        else: 
            form.username.errors =["Invalid username."]

    return render_template('users/form.html', form=form, action="login")

@app.route('/users/<username>')
def user_profile(username):
    """Show user details, if logged in"""

    user = User.query.get(username)

    if "username" not in session:
        flash("You must be logged in to view!", "alert alert-danger")
        return redirect("/")

    else:
        return render_template('users/user.html', user=user)

@app.route('/logout')
def logout():
    """Logout route"""

    session.pop("username")

    return redirect('/')

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Deletes user"""

    if session['username'] == username:
        user = User.query.get(username)
        db.session.delete(user)
        db.session.commit()

        session.pop(username)

        flash("User Account Deleted.", "alert alert-warning")
        return redirect('/')
    else:
        flash(f"You must be logged in to {username} account to delete this user.", "alert alert-danger")

        return redirect(f'/users/{username}')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """Show form to add feedback, handle form submission"""

    if session['username'] == username:
        form = FeedbackForm()
        user = User.query.get(username)

        if form.validate_on_submit():
            feedback = Feedback(
                title=form.title.data,
                content=form.content.data,
                username=username
            )

            db.session.add(feedback)
            db.session.commit()

            return redirect(f'/users/{user.username}')
        
        return render_template('feedback.html', form=form, username=username, action=[f"/users/{ username }/feedback/add", "Add"])

    else:
        flash(f"You must be logged in as {username} to add feedback", "alert alert-danger")
        return redirect(f'/users/{username}')

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    """Show form to edit feedback, handle form submission"""

    feedback = Feedback.query.get_or_404(feedback_id)
    if session['username'] == feedback.username:
        form =  FeedbackForm()

        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data

            db.session.add(feedback)
            db.session.commit()

            flash("Feedback updated!", "alert alert-success")
            return redirect(f'/users/{feedback.username}')

        form.title.data = feedback.title
        form.content.data = feedback.content

        return render_template('feedback.html', form=form, username=feedback.username, action=[f"/feedback/{ feedback.id }/update", "Update"])

    flash(f"Only {feedback.username} can update this feedback.")
    return redirect(f'/users/{feedback.username}')

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """Delete single feedback"""

    feedback = Feedback.query.get_or_404(feedback_id)

    if session["username"] == feedback.username:
        db.session.delete(feedback)
        db.session.commit()

        flash("Feedback deleted.", "alert alert-secondary")
        return redirect(f'/users/{feedback.username}')

    flash("Not authorized to delete feedback")
    return redirect(f'/users/{feedback.username}')