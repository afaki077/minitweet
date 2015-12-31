from flask.ext.wtf import Form
from wtforms import TextAreaField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class PublishForm(Form):
    post_title = StringField(
            'post_title', validators=[DataRequired(), Length(min=5, max=50)]
    )
    textarea = TextAreaField(
            "textarea", validators=[DataRequired(), Length(min=5, max=300)]
    )


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class SignUpForm(Form):
    username = StringField(
        'username',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(), EqualTo('password', message='Passwords must match.')
        ]
    )
