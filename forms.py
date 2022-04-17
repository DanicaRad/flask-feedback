from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, EmailField
from wtforms_alchemy import model_form_factory, Unique, ModelForm
from models import db, User, Feedback
from wtforms.validators import InputRequired, Length, Email

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_sesssion(self):
        return db.session


class AddUserForm(ModelForm):
    """Form for adding user to db"""

    class Meta:
        model = User
        include_primary_keys = True
        Unique(User.email)

# class AddUserForm(FlaskForm):
#     """Form for adding user to db"""

    # username = StringField("Username",
    #                         validators=[InputRequired(message='Input Required'),
    #                         Length(min=1, max=20,
    #                         message='Must be 20 characters or less')])

    # password = PasswordField("Password",
    #                         validators=[InputRequired('Input Required')])

    # email = EmailField("Email",
    #                     validators=[InputRequired('Input Required'), Email()])

    # first_name = StringField("First Name",
    #                         validators=[InputRequired('Input Required'),
    #                         Length(min=1, max=30,
    #                         message='Must be 30 characters or less')])

    # last_name = StringField("Last Name",
    #                         validators=[InputRequired('Input Required'),
    #                         Length(min=1, max=30,
    #                         message='Must be 30 characters or less')])
                            

class LoginForm(FlaskForm):
    """Form for user login"""

    username = StringField("Username", validators=[InputRequired(message='Username Required')])

    password = PasswordField("Password", validators=[InputRequired(message="Password Required")])


class FeedbackForm(FlaskForm):
    """Form to add feedback"""

    title = StringField("Title", 
                        validators=[InputRequired(message='Title is required'),
                        Length(min=1, max=100,
                        message='Must be 100 characters or less')])

    content = TextAreaField("Content",
                            validators=[InputRequired(message="Content is required")])

