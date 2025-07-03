from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    role = SelectField("Role", choices=[("PUBLISHER", "Publisher"), ("VISITOR", "Visitor")], validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Enter a valid email address")])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
