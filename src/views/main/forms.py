from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired, length, Email, Length, Regexp, ValidationError


class LoginForm(FlaskForm):
    username = StringField('მომხმარებელი', validators=[DataRequired()])
    password = PasswordField('პაროლი', validators=[DataRequired(), length(min=8, max=64)])
    submit = SubmitField("შესვლა")



class ContactForm(FlaskForm):
    first_name = StringField(
        'სახელი',
        validators=[
            DataRequired(message="შეავსეთ ველი"),
            Length(min=2, max=50, message="სახელი უნდა იყოს 2-დან 50 სიმბოლომდე"),
            Regexp(r'^[A-Za-zა-ჰ]+$', message="მხოლოდ ასოებია ნებადართული")
        ]
    )
    last_name = StringField(
        'გვარი',
        validators=[
            DataRequired(message="შეავსეთ ველი"),
            Length(min=2, max=50, message="გვარი უნდა იყოს 2-დან 50 სიმბოლომდე"),
            Regexp(r'^[A-Za-zა-ჰ]+$', message="მხოლოდ ასოებია ნებადართული")
        ]
    )
    subject = StringField(
        'თემა/სათაური',
        validators=[
            DataRequired(message="შეავსეთ ველი"),
            Length(min=3, max=100, message="სათაური უნდა შეიცავდეს 3-დან 100 სიმბოლომდე")
        ]
    )
    text = TextAreaField(
        'შეტყობინება/ტექსტი',
        validators=[DataRequired(message="შეიყვანეთ შეტყობინება/ტექსტი")]
    )
    email = StringField(
        'ელ. ფოსტა',
        validators=[
            DataRequired(message="შეავსეთ ველი"),
            Length(min=5, max=50, message="ელ. ფოსტა უნდა შეიცავდეს 5-დან 50 სიმბოლომდე"),
            Email(message="ელ. ფოსტა უნდა შეიცავდეს '@' სიმბოლოს")
        ]
    )
    submit = SubmitField('გაგზავნა')



